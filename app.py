from __future__ import annotations

import argparse
import time

import cv2

from src.detector import HandDetector
from src.drawer import draw_detection_result, draw_fps, draw_status_bar


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Real-time MediaPipe hand landmark tracking with finger state output."
    )
    parser.add_argument("--camera", type=int, default=0, help="Camera index. Default: 0")
    parser.add_argument(
        "--width", type=int, default=1280, help="Preferred camera width. Default: 1280"
    )
    parser.add_argument(
        "--height", type=int, default=720, help="Preferred camera height. Default: 720"
    )
    parser.add_argument(
        "--max-hands", type=int, default=2, help="Maximum hands to detect. Default: 2"
    )
    parser.add_argument(
        "--min-detection-confidence",
        type=float,
        default=0.6,
        help="MediaPipe detection confidence threshold. Default: 0.6",
    )
    parser.add_argument(
        "--min-tracking-confidence",
        type=float,
        default=0.5,
        help="MediaPipe tracking confidence threshold. Default: 0.5",
    )
    parser.add_argument(
        "--no-flip",
        action="store_true",
        help="Disable horizontal mirror effect.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera {args.camera}.")

    detector = HandDetector(
        max_num_hands=args.max_hands,
        min_detection_confidence=args.min_detection_confidence,
        min_tracking_confidence=args.min_tracking_confidence,
    )

    window_name = "MediaPipe Hand Tracking"
    prev_time = time.time()

    try:
        while True:
            success, frame = cap.read()
            if not success:
                print("Failed to read frame from webcam.")
                break

            if not args.no_flip:
                frame = cv2.flip(frame, 1)

            detections = detector.detect(frame)
            annotated = draw_detection_result(frame, detections)

            current_time = time.time()
            fps = 1.0 / max(current_time - prev_time, 1e-6)
            prev_time = current_time

            draw_fps(annotated, fps)
            draw_status_bar(
                annotated,
                camera_index=args.camera,
                hand_count=len(detections),
                mirror_enabled=not args.no_flip,
            )

            cv2.imshow(window_name, annotated)

            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
    finally:
        detector.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
