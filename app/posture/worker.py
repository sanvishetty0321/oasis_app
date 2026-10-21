"""Background posture monitoring worker for OASIS."""

import cv2
import queue
import threading
import time

from .detector import PostureDetector
from .classifier import PostureClassifier


class PostureWorker:
    """Monitor posture without blocking the dashboard UI."""

    def __init__(
        self,
        event_queue=None,
        camera_index=0,
        slouch_seconds=10,
        preview=True,
    ):
        self.event_queue = (
            event_queue if event_queue is not None
            else queue.Queue(maxsize=100)
        )
        self.camera_index = camera_index
        self.slouch_seconds = slouch_seconds
        self.preview = preview

        self.stop_event = threading.Event()
        self.thread = None

        self._last_status = None
        self._slouch_start = None
        self._alert_sent = False

    def publish(self, event):
        """Publish an event without blocking the worker."""
        try:
            self.event_queue.put_nowait(event)
        except queue.Full:
            # Do not freeze webcam processing if the queue is full.
            pass

    def start(self):
        """Start monitoring in a background thread."""
        if self.thread and self.thread.is_alive():
            return

        self.stop_event.clear()
        self.thread = threading.Thread(
            target=self._run,
            name="OASIS-PostureWorker",
            daemon=True,
        )
        self.thread.start()

    def stop(self):
        """Request the worker to stop."""
        self.stop_event.set()

    def join(self, timeout=None):
        """Wait for the worker thread to finish."""
        if self.thread:
            self.thread.join(timeout)

    def _run(self):
        detector = None
        camera = None

        try:
            detector = PostureDetector()
            classifier = PostureClassifier()

            camera = cv2.VideoCapture(self.camera_index)

            if not camera.isOpened():
                raise RuntimeError(
                    "Cannot open webcam. Check camera permissions "
                    "or try another camera index."
                )

            self.publish({
                "feature": "posture",
                "type": "started",
                "timestamp": time.time(),
            })

            while not self.stop_event.is_set():
                success, frame = camera.read()

                if not success:
                    self.publish({
                        "feature": "posture",
                        "type": "error",
                        "message": "Could not read webcam frame",
                        "timestamp": time.time(),
                    })
                    break

                frame, landmarks = detector.detect(frame)
                result = classifier.classify(landmarks)

                self._update_posture(result)

                if self.preview:
                    self._show_preview(frame, result)

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        self.stop_event.set()

        except Exception as exc:
            self.publish({
                "feature": "posture",
                "type": "error",
                "message": str(exc),
                "timestamp": time.time(),
            })

        finally:
            if camera is not None:
                camera.release()

            if detector is not None:
                detector.close()

            if self.preview:
                cv2.destroyAllWindows()

            self.publish({
                "feature": "posture",
                "type": "stopped",
                "timestamp": time.time(),
            })

    def _update_posture(self, result):
        now = time.monotonic()
        status = result["status"]

        if status != self._last_status:
            self.publish({
                "feature": "posture",
                "type": "status_changed",
                "status": status,
                "details": result,
                "timestamp": time.time(),
            })
            self._last_status = status

        if status == PostureClassifier.SLOUCHING:
            if self._slouch_start is None:
                self._slouch_start = now
                self._alert_sent = False

            duration = now - self._slouch_start

            if (
                duration >= self.slouch_seconds
                and not self._alert_sent
            ):
                self.publish({
                    "feature": "posture",
                    "type": "alert",
                    "status": status,
                    "message": (
                        "Please check your sitting posture."
                    ),
                    "duration_seconds": round(duration, 1),
                    "timestamp": time.time(),
                })
                self._alert_sent = True

        else:
            self._slouch_start = None
            self._alert_sent = False

    @staticmethod
    def _show_preview(frame, result):
        """Display an optional webcam preview."""
        status = result["status"]

        color = (
            (0, 255, 0)
            if status == PostureClassifier.GOOD
            else (0, 0, 255)
        )

        cv2.putText(
            frame,
            f"Posture: {status}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            color,
            2,
        )

        cv2.imshow("OASIS - Posture Detection", frame)


if __name__ == "__main__":
    events = queue.Queue(maxsize=100)

    worker = PostureWorker(
        event_queue=events,
        slouch_seconds=10,
        preview=True,
    )

    worker.start()

    try:
        while worker.thread.is_alive():
            try:
                event = events.get(timeout=0.5)
                print(event)
            except queue.Empty:
                continue
    except KeyboardInterrupt:
        pass
    finally:
        worker.stop()
        worker.join(timeout=3)
