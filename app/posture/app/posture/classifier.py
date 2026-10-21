"""Classify basic sitting posture from MediaPipe landmarks."""

import math


class PostureClassifier:
    GOOD = "Good"
    SLOUCHING = "Slouching"
    UNKNOWN = "Unknown"

    def __init__(
        self,
        head_offset_threshold=0.08,
        torso_angle_threshold=15.0,
        visibility_threshold=0.5,
    ):
        self.head_offset_threshold = head_offset_threshold
        self.torso_angle_threshold = torso_angle_threshold
        self.visibility_threshold = visibility_threshold

    @staticmethod
    def _landmark_ids():
        """MediaPipe Pose landmark indices."""
        return {
            "nose": 0,
            "left_shoulder": 11,
            "right_shoulder": 12,
            "left_hip": 23,
            "right_hip": 24,
        }

    def classify(self, landmarks):
        """Return a dictionary describing the estimated posture."""
        if landmarks is None:
            return {
                "status": self.UNKNOWN,
                "reason": "No pose detected",
                "head_offset": None,
                "torso_angle": None,
            }

        ids = self._landmark_ids()

        required = [
            landmarks[ids[name]]
            for name in (
                "nose",
                "left_shoulder",
                "right_shoulder",
                "left_hip",
                "right_hip",
            )
        ]

        if any(
            getattr(point, "visibility", 1.0)
            < self.visibility_threshold
            for point in required
        ):
            return {
                "status": self.UNKNOWN,
                "reason": "Body landmarks are not sufficiently visible",
                "head_offset": None,
                "torso_angle": None,
            }

        nose = landmarks[ids["nose"]]
        left_shoulder = landmarks[ids["left_shoulder"]]
        right_shoulder = landmarks[ids["right_shoulder"]]
        left_hip = landmarks[ids["left_hip"]]
        right_hip = landmarks[ids["right_hip"]]

        shoulder_x = (
            left_shoulder.x + right_shoulder.x
        ) / 2
        shoulder_y = (
            left_shoulder.y + right_shoulder.y
        ) / 2

        hip_x = (left_hip.x + right_hip.x) / 2
        hip_y = (left_hip.y + right_hip.y) / 2

        head_offset = abs(nose.x - shoulder_x)

        dx = hip_x - shoulder_x
        dy = hip_y - shoulder_y

        if abs(dy) < 1e-6:
            return {
                "status": self.UNKNOWN,
                "reason": "Torso alignment cannot be estimated",
                "head_offset": round(head_offset, 4),
                "torso_angle": None,
            }

        torso_angle = abs(
            math.degrees(math.atan2(dx, dy))
        )

        slouching = (
            head_offset > self.head_offset_threshold
            or torso_angle > self.torso_angle_threshold
        )

        return {
            "status": (
                self.SLOUCHING if slouching else self.GOOD
            ),
            "reason": "Threshold-based estimate",
            "head_offset": round(head_offset, 4),
            "torso_angle": round(torso_angle, 2),
        }
