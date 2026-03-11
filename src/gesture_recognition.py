from __future__ import annotations

from src.models import Landmark


def classify_gesture(
    landmarks: list[Landmark],
    fingers_extended: dict[str, bool],
) -> str:
    if all(fingers_extended.values()):
        return "Open Palm"

    if not any(fingers_extended.values()):
        return "Fist"

    if _is_thumbs_up(landmarks, fingers_extended):
        return "Thumbs Up"

    if _is_pointing_up(landmarks, fingers_extended):
        return "Pointing Up"

    if _is_v_sign(fingers_extended):
        return "Victory"

    return "Unknown"


def _is_thumbs_up(
    landmarks: list[Landmark],
    fingers_extended: dict[str, bool],
) -> bool:
    folded_others = all(
        not fingers_extended[finger] for finger in ("index", "middle", "ring", "pinky")
    )
    thumb_tip = landmarks[4]
    wrist = landmarks[0]
    return fingers_extended["thumb"] and folded_others and thumb_tip.y < wrist.y


def _is_pointing_up(
    landmarks: list[Landmark],
    fingers_extended: dict[str, bool],
) -> bool:
    index_tip = landmarks[8]
    wrist = landmarks[0]
    return (
        fingers_extended["index"]
        and not fingers_extended["middle"]
        and not fingers_extended["ring"]
        and not fingers_extended["pinky"]
        and index_tip.y < wrist.y
    )


def _is_v_sign(fingers_extended: dict[str, bool]) -> bool:
    return (
        fingers_extended["index"]
        and fingers_extended["middle"]
        and not fingers_extended["ring"]
        and not fingers_extended["pinky"]
    )
