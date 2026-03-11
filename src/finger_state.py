from __future__ import annotations

from math import acos, degrees, sqrt

from src.models import Landmark


FINGER_TIPS = {
    "thumb": 4,
    "index": 8,
    "middle": 12,
    "ring": 16,
    "pinky": 20,
}

FINGER_PIPS = {
    "index": 6,
    "middle": 10,
    "ring": 14,
    "pinky": 18,
}

FINGER_DIPS = {
    "index": 7,
    "middle": 11,
    "ring": 15,
    "pinky": 19,
}

FINGER_MCPS = {
    "index": 5,
    "middle": 9,
    "ring": 13,
    "pinky": 17,
}

FINGER_ANGLE_THRESHOLD = 160.0
THUMB_ANGLE_THRESHOLD = 150.0


def evaluate_fingers(
    landmarks: list[Landmark],
    normalized_landmarks: list[tuple[float, float, float]],
    handedness_label: str,
) -> dict[str, bool]:
    states = {
        "thumb": _is_thumb_extended(
            landmarks=landmarks,
            normalized_landmarks=normalized_landmarks,
            handedness_label=handedness_label,
        ),
        "index": _is_finger_extended(landmarks, "index"),
        "middle": _is_finger_extended(landmarks, "middle"),
        "ring": _is_finger_extended(landmarks, "ring"),
        "pinky": _is_finger_extended(landmarks, "pinky"),
    }
    return states


def _is_finger_extended(landmarks: list[Landmark], finger_name: str) -> bool:
    tip_idx = FINGER_TIPS[finger_name]
    dip_idx = FINGER_DIPS[finger_name]
    pip_idx = FINGER_PIPS[finger_name]
    mcp_idx = FINGER_MCPS[finger_name]

    angle = _joint_angle(
        landmarks[mcp_idx],
        landmarks[pip_idx],
        landmarks[dip_idx],
    )
    tip_y = landmarks[tip_idx].y
    pip_y = landmarks[pip_idx].y
    wrist_y = landmarks[0].y

    return angle > FINGER_ANGLE_THRESHOLD and tip_y < pip_y and tip_y < wrist_y


def _is_thumb_extended(
    landmarks: list[Landmark],
    normalized_landmarks: list[tuple[float, float, float]],
    handedness_label: str,
) -> bool:
    thumb_angle = _joint_angle(landmarks[1], landmarks[2], landmarks[3])
    thumb_tip_x = landmarks[4].x
    thumb_ip_x = landmarks[3].x
    thumb_mcp_x = landmarks[2].x
    thumb_tip_y = normalized_landmarks[4][1]
    index_mcp_y = normalized_landmarks[5][1]

    if handedness_label.lower() == "right":
        horizontal_extension = thumb_tip_x < thumb_ip_x < thumb_mcp_x
    else:
        horizontal_extension = thumb_tip_x > thumb_ip_x > thumb_mcp_x

    return (
        thumb_angle > THUMB_ANGLE_THRESHOLD
        and horizontal_extension
        and abs(thumb_tip_y - index_mcp_y) > 0.02
    )


def _joint_angle(a: Landmark, b: Landmark, c: Landmark) -> float:
    ab = (a.x - b.x, a.y - b.y, a.z - b.z)
    cb = (c.x - b.x, c.y - b.y, c.z - b.z)
    denominator = _vector_norm(ab) * _vector_norm(cb)
    if denominator == 0:
        return 0.0

    cosine = max(-1.0, min(1.0, _dot(ab, cb) / denominator))
    return degrees(acos(cosine))


def _dot(v1: tuple[float, float, float], v2: tuple[float, float, float]) -> float:
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]


def _vector_norm(vector: tuple[float, float, float]) -> float:
    return sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
