from __future__ import annotations

import cv2
import mediapipe as mp

from src.finger_state import evaluate_fingers
from src.gesture_recognition import classify_gesture
from src.models import HandDetection, Landmark


class HandDetector:
    def __init__(
        self,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def detect(self, frame_bgr) -> list[HandDetection]:
        height, width = frame_bgr.shape[:2]
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        results = self._hands.process(frame_rgb)

        if not results.multi_hand_landmarks or not results.multi_handedness:
            return []

        detections: list[HandDetection] = []
        for index, (hand_landmarks, hand_info) in enumerate(
            zip(results.multi_hand_landmarks, results.multi_handedness)
        ):
            label = hand_info.classification[0].label
            score = hand_info.classification[0].score
            normalized_landmarks = [
                (landmark.x, landmark.y, landmark.z)
                for landmark in hand_landmarks.landmark
            ]
            landmarks = _to_pixel_landmarks(
                normalized_landmarks=normalized_landmarks,
                frame_width=width,
                frame_height=height,
            )
            bbox = _compute_bounding_box(landmarks)
            fingers_extended = evaluate_fingers(
                landmarks=landmarks,
                normalized_landmarks=normalized_landmarks,
                handedness_label=label,
            )

            detections.append(
                HandDetection(
                    label=label,
                    score=score,
                    landmarks=landmarks,
                    normalized_landmarks=normalized_landmarks,
                    handedness_index=index,
                    bbox=bbox,
                    fingers_extended=fingers_extended,
                    gesture_name=classify_gesture(
                        landmarks=landmarks,
                        fingers_extended=fingers_extended,
                    ),
                )
            )

        return detections

    def close(self) -> None:
        self._hands.close()


def _to_pixel_landmarks(
    normalized_landmarks: list[tuple[float, float, float]],
    frame_width: int,
    frame_height: int,
) -> list[Landmark]:
    return [
        Landmark(
            x=max(0, min(int(x * frame_width), frame_width - 1)),
            y=max(0, min(int(y * frame_height), frame_height - 1)),
            z=z,
        )
        for x, y, z in normalized_landmarks
    ]


def _compute_bounding_box(landmarks: list[Landmark]) -> tuple[int, int, int, int]:
    x_values = [landmark.x for landmark in landmarks]
    y_values = [landmark.y for landmark in landmarks]
    return min(x_values), min(y_values), max(x_values), max(y_values)
