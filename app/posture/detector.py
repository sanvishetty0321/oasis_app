"""Detect body landmarks from webcam frames."""

import cv2
import mediapipe as mp


class PostureDetector:
    """Detect and draw body landmarks."""

    def __init__(self):
        if not hasattr(mp, "solutions"):
            raise RuntimeError(
                "Install a MediaPipe version that supports "
                "mediapipe.solutions.pose."
            )

        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=0,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def detect(self, frame):
        """Return the annotated frame and detected landmarks."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        landmarks = None

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            self.mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
            )

        return frame, landmarks

    def close(self):
        """Release MediaPipe resources."""
        self.pose.close()
