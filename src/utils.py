from __future__ import annotations

from datetime import datetime
from pathlib import Path

import cv2


def save_frame(frame, output_dir: str = "captures") -> str:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = path / f"hand_tracking_{timestamp}.png"
    cv2.imwrite(str(file_path), frame)
    return str(file_path)
