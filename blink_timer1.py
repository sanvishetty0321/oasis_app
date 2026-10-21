"""
OASIS - Blink Monitoring + Focus Timer Prototype
------------------------------------------------
Python 3.12 recommended.
Install:
    py -3.12 -m pip install opencv-python mediapipe==0.10.21

Run:
    py -3.12 blink_timer1.py

Features:
- Blink counting
- Approximate recent blink rate
- Prolonged eye-closure cue and one sound per closure event
- Focus timer with start/pause/reset keyboard controls
- Configurable session length and break reminder
- Camera / face status
- Saves session summaries to oasis_sessions.db (no video is saved)

Controls:
    S = start/resume focus session
    P = pause focus session
    R = reset current session
    B = begin a break / mark session as on break
    Q = quit
"""

import cv2
import mediapipe as mp
import time
import sqlite3
import threading
import platform
from datetime import datetime

# Windows notification sound. On other platforms, the fallback is a terminal bell.
try:
    import winsound
except ImportError:
    winsound = None


# -------------------- USER SETTINGS --------------------
EYE_CLOSURE_THRESHOLD_SECONDS = 2.0
STUDY_SESSION_MINUTES = 25
BLINK_RATE_WINDOW_SECONDS = 60
DATABASE_FILE = "oasis_sessions.db"
# -------------------------------------------------------


def play_alert():
    """Play a short alert without blocking the webcam loop."""
    def _play():
        try:
            if winsound is not None:
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            else:
                print("\a", end="", flush=True)
        except Exception:
            print("\a", end="", flush=True)

    threading.Thread(target=_play, daemon=True).start()


def format_time(seconds):
    seconds = max(0, int(seconds))
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        
        return f"{hours:02}:{minutes:02}:{secs:02}"
    return f"{minutes:02}:{secs:02}"


class SessionDatabase:
    """Stores session summaries only; it does not store camera frames."""

    def __init__(self, filename=DATABASE_FILE):
        self.filename = filename
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.filename)

    def _create_table(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    started_at TEXT NOT NULL,
                    duration_seconds INTEGER NOT NULL,
                    blink_count INTEGER NOT NULL,
                    prolonged_closure_events INTEGER NOT NULL,
                    completed INTEGER NOT NULL
                )
                """
            )

    def save_session(self, started_at, duration, blinks, closure_events, completed):
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO sessions
                (started_at, duration_seconds, blink_count,
                 prolonged_closure_events, completed)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    started_at,
                    int(duration),
                    int(blinks),
                    int(closure_events),
                    1 if completed else 0,
                ),
            )


class BlinkDetector:
    """Uses MediaPipe Face Mesh landmarks to estimate eye closure and count blinks."""

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    def __init__(self, closure_threshold=EYE_CLOSURE_THRESHOLD_SECONDS):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.closure_threshold = float(closure_threshold)
        self.blink_count = 0
        self.eyes_closed = False
        self.eye_closed_start = None
        self.prolonged_closure = False
        self.prolonged_closure_events = 0
        self.blink_timestamps = []
        self.face_detected = False
        self._last_alert_state = False

    @staticmethod
    def _distance(point_a, point_b):
        return (
            (point_a[0] - point_b[0]) ** 2
            + (point_a[1] - point_b[1]) ** 2
        ) ** 0.5

    def _eye_aspect_ratio(self, face, indices, width, height):
        points = [
            (
                int(face.landmark[index].x * width),
                int(face.landmark[index].y * height),
            )
            for index in indices
        ]
        vertical_one = self._distance(points[1], points[5])
        vertical_two = self._distance(points[2], points[4])
        horizontal = self._distance(points[0], points[3])
        if horizontal == 0:
            return 1.0
        return (vertical_one + vertical_two) / (2.0 * horizontal)

    def detect(self, frame):
        """Update detection state for one BGR camera frame."""
        now = time.time()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        self.face_detected = bool(results.multi_face_landmarks)

        if not self.face_detected:
            # Do not infer sleepiness when the face is not visible.
            self.eyes_closed = False
            self.eye_closed_start = None
            self.prolonged_closure = False
            self._last_alert_state = False
            return

        face = results.multi_face_landmarks[0]
        height, width = frame.shape[:2]
        left_ratio = self._eye_aspect_ratio(face, self.LEFT_EYE, width, height)
        right_ratio = self._eye_aspect_ratio(face, self.RIGHT_EYE, width, height)
        eye_ratio = (left_ratio + right_ratio) / 2.0

        # A threshold of 0.20 is a starting point and may need calibration.
        if eye_ratio < 0.20:
            if not self.eyes_closed:
                self.eyes_closed = True
                self.eye_closed_start = now
                self.prolonged_closure = False

            if (
                self.eye_closed_start is not None
                and now - self.eye_closed_start >= self.closure_threshold
                and not self.prolonged_closure
            ):
                self.prolonged_closure = True
                self.prolonged_closure_events += 1
        else:
            if self.eyes_closed:
                # Count a blink only if the closure was not prolonged.
                if not self.prolonged_closure:
                    self.blink_count += 1
                    self.blink_timestamps.append(now)
                self.eyes_closed = False
                self.eye_closed_start = None
                self.prolonged_closure = False
                self._last_alert_state = False

        # Keep only timestamps in the recent rate window.
        cutoff = now - BLINK_RATE_WINDOW_SECONDS
        self.blink_timestamps = [
            stamp for stamp in self.blink_timestamps if stamp >= cutoff
        ]

    def get_recent_blink_rate(self):
        """Return estimated blinks per minute over the recent window."""
        now = time.time()
        cutoff = now - BLINK_RATE_WINDOW_SECONDS
        self.blink_timestamps = [
            stamp for stamp in self.blink_timestamps if stamp >= cutoff
        ]
        return len(self.blink_timestamps)

    def close(self):
        self.face_mesh.close()


class FocusTimer:
    def __init__(self, session_minutes=STUDY_SESSION_MINUTES):
        self.session_seconds = int(session_minutes * 60)
        self.started_at_text = None
        self.start_time = None
        self.elapsed_before_pause = 0.0
        self.running = False
        self.on_break = False
        self.break_alerted = False

    def start(self):
        if not self.running and not self.on_break:
            self.start_time = time.time()
            self.running = True
            if self.started_at_text is None:
                self.started_at_text = datetime.now().isoformat(timespec="seconds")

    def pause(self):
        if self.running:
            self.elapsed_before_pause += time.time() - self.start_time
            self.running = False
            self.start_time = None

    def begin_break(self):
        self.pause()
        self.on_break = True

    def resume_after_break(self):
        self.on_break = False
        self.start()

    def reset(self):
        self.start_time = None
        self.elapsed_before_pause = 0.0
        self.running = False
        self.on_break = False
        self.break_alerted = False
        self.started_at_text = None

    def elapsed(self):
        result = self.elapsed_before_pause
        if self.running and self.start_time is not None:
            result += time.time() - self.start_time
        return int(result)

    def is_session_complete(self):
        return self.elapsed() >= self.session_seconds


def draw_text(frame, text, position, color=(255, 255, 255), scale=0.65, thickness=2):
    cv2.putText(
        frame, text, position, cv2.FONT_HERSHEY_SIMPLEX,
        scale, color, thickness, cv2.LINE_AA
    )


def main():
    database = SessionDatabase()
    detector = BlinkDetector()
    timer = FocusTimer()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Cannot access webcam. Check that it is connected and not being used by another app.")
        detector.close()
        return

    print("OASIS monitoring started.")
    print("Keys: S=start/resume, P=pause, R=reset, B=break, Q=quit")
    saved_for_this_run = False
    session_completed = False
    last_closure_alerted = False

    try:
        while camera.isOpened():
            success, frame = camera.read()
            if not success:
                print("Cannot read from webcam.")
                break

            detector.detect(frame)
            elapsed = timer.elapsed()

            # Play one sound when a new prolonged closure is first detected.
            if detector.prolonged_closure and not last_closure_alerted:
                play_alert()
                last_closure_alerted = True
            elif not detector.prolonged_closure:
                last_closure_alerted = False

            if timer.running and timer.is_session_complete() and not timer.break_alerted:
                timer.pause()
                timer.break_alerted = True
                session_completed = True
                play_alert()

            # UI overlay: the standalone prototype window.
            draw_text(frame, f"Blinks: {detector.blink_count}", (20, 35), (0, 255, 0))
            draw_text(frame, f"Recent blinks/min: {detector.get_recent_blink_rate()}", (20, 65))
            draw_text(frame, f"Focus time: {format_time(elapsed)}", (20, 95))
            draw_text(
                frame,
                f"Session goal: {format_time(timer.session_seconds)}",
                (20, 125),
            )

            if not detector.face_detected:
                draw_text(frame, "Face not detected - adjust camera position", (20, 165), (0, 165, 255), 0.58)
            elif detector.prolonged_closure:
                draw_text(frame, "Possible fatigue cue - consider a break", (20, 165), (0, 0, 255), 0.58)
            elif timer.on_break:
                draw_text(frame, "Break time - press S to resume", (20, 165), (255, 200, 0), 0.58)
            elif session_completed:
                draw_text(frame, "Session goal reached - take a break", (20, 165), (0, 200, 255), 0.58)
            elif timer.running:
                draw_text(frame, "Focus session running", (20, 165), (0, 255, 0), 0.58)
            else:
                draw_text(frame, "Paused - press S to start/resume", (20, 165), (0, 200, 255), 0.58)

            draw_text(frame, "S Start/Resume | P Pause | R Reset | B Break | Q Quit", (20, frame.shape[0] - 20), (255, 255, 255), 0.48, 1)
            cv2.imshow("OASIS - Focus & Blink Prototype", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("s"):
                if timer.on_break:
                    timer.resume_after_break()
                    session_completed = False
                else:
                    timer.start()
                    session_completed = False
            elif key == ord("p"):
                timer.pause()
            elif key == ord("b"):
                timer.begin_break()
                play_alert()
            elif key == ord("r"):
                timer.reset()
                detector.blink_count = 0
                detector.prolonged_closure_events = 0
                detector.blink_timestamps.clear()
                last_closure_alerted = False
                session_completed = False
                saved_for_this_run = False

        # Save one session summary if a session was started during this run.
        if timer.started_at_text is not None and not saved_for_this_run:
            database.save_session(
                timer.started_at_text,
                timer.elapsed(),
                detector.blink_count,
                detector.prolonged_closure_events,
                session_completed,
            )
            saved_for_this_run = True
            print(f"Session summary saved to {DATABASE_FILE}")

        print(f"Total blinks: {detector.blink_count}")
        print(f"Prolonged eye-closure events: {detector.prolonged_closure_events}")
        print(f"Focus time: {format_time(timer.elapsed())}")

    finally:
        camera.release()
        detector.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
