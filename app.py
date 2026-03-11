from __future__ import annotations

import argparse
import time
from pathlib import Path

import cv2

from src.detector import HandDetector
from src.drawer import draw_detection_result, draw_fps, draw_status_bar
from src.utils import save_frame


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
    parser.add_argument(
        "--image",
        type=str,
        help="Run inference on a single image instead of webcam.",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output image path for --image mode. Default: outputs/<input_name>_result.png",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    detector = HandDetector(
        max_num_hands=args.max_hands,
        min_detection_confidence=args.min_detection_confidence,
        min_tracking_confidence=args.min_tracking_confidence,
    )

    try:
        if args.image:
            run_image_mode(detector, args.image, args.output)
        else:
            run_camera_mode(detector, args)
    finally:
        detector.close()


def run_camera_mode(detector: HandDetector, args: argparse.Namespace) -> None:
    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera {args.camera}.")

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
            if key == ord("s"):
                saved_path = save_frame(annotated)
                print(f"Saved screenshot: {saved_path}")
            if key in (27, ord("q")):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


def run_image_mode(
    detector: HandDetector,
    image_path: str,
    output_path: str | None,
) -> None:
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")

    detections = detector.detect(image)
    annotated = draw_detection_result(image, detections)

    resolved_output = _resolve_output_path(image_path, output_path)
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(resolved_output), annotated)

    print(f"Detections: {len(detections)}")
    for index, detection in enumerate(detections, start=1):
        print(
            f"[{index}] {detection.label} | "
            f"gesture={detection.gesture_name} | "
            f"fingers={detection.fingers_extended}"
        )
    print(f"Saved result image: {resolved_output}")


def _resolve_output_path(image_path: str, output_path: str | None) -> Path:
    if output_path:
        return Path(output_path)

    source = Path(image_path)
    return Path("outputs") / f"{source.stem}_result{source.suffix or '.png'}"


if __name__ == "__main__":
    main()
