from __future__ import annotations

import cv2
import mediapipe as mp

from src.models import HandDetection


HAND_CONNECTIONS = mp.solutions.hands.HAND_CONNECTIONS


def draw_detection_result(frame, detections: list[HandDetection]):
    canvas = frame.copy()
    for detection in detections:
        _draw_bounding_box(canvas, detection)
        _draw_landmarks(canvas, detection.landmarks)
        _draw_hand_label(canvas, detection)
        _draw_finger_states(canvas, detection)
    return canvas


def draw_fps(frame, fps: float) -> None:
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )


def draw_status_bar(
    frame,
    camera_index: int,
    hand_count: int,
    mirror_enabled: bool,
) -> None:
    text = (
        f"Camera: {camera_index} | Hands: {hand_count} | "
        f"Mirror: {'On' if mirror_enabled else 'Off'} | Screenshot: S | Exit: Q / Esc"
    )
    height = frame.shape[0]
    cv2.rectangle(frame, (0, height - 32), (frame.shape[1], height), (20, 20, 20), -1)
    cv2.putText(
        frame,
        text,
        (10, height - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )


def _draw_landmarks(frame, landmarks) -> None:
    for start_idx, end_idx in HAND_CONNECTIONS:
        start = (landmarks[start_idx].x, landmarks[start_idx].y)
        end = (landmarks[end_idx].x, landmarks[end_idx].y)
        cv2.line(frame, start, end, (0, 200, 0), 2)

    for idx, point in enumerate(landmarks):
        center = (point.x, point.y)
        cv2.circle(frame, center, 4, (0, 0, 255), -1)
        cv2.putText(
            frame,
            str(idx),
            (point.x + 4, point.y - 4),
            cv2.FONT_HERSHEY_PLAIN,
            0.8,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )


def _draw_hand_label(frame, detection: HandDetection) -> None:
    x1, y1, _, _ = detection.bbox
    anchor = (x1, max(y1 - 12, 20))
    text = f"{detection.label} | {detection.gesture_name} ({detection.score:.2f})"

    cv2.putText(
        frame,
        text,
        anchor,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 200, 0),
        2,
        cv2.LINE_AA,
    )


def _draw_finger_states(frame, detection: HandDetection) -> None:
    x1, _, _, y2 = detection.bbox
    base_x = x1
    base_y = min(y2 + 22, frame.shape[0] - 110)

    for row, (finger_name, is_extended) in enumerate(detection.fingers_extended.items()):
        label = f"{finger_name.capitalize()}: {'Straight' if is_extended else 'Bent'}"
        color = (0, 255, 0) if is_extended else (0, 120, 255)
        cv2.putText(
            frame,
            label,
            (base_x, base_y + row * 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2,
            cv2.LINE_AA,
        )


def _draw_bounding_box(frame, detection: HandDetection) -> None:
    x1, y1, x2, y2 = detection.bbox
    cv2.rectangle(frame, (x1 - 10, y1 - 10), (x2 + 10, y2 + 10), (255, 120, 0), 2)
