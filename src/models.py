from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple


class Landmark(NamedTuple):
    x: int
    y: int
    z: float


@dataclass
class HandDetection:
    label: str
    score: float
    landmarks: list[Landmark]
    normalized_landmarks: list[tuple[float, float, float]]
    handedness_index: int
    bbox: tuple[int, int, int, int]
    fingers_extended: dict[str, bool]
