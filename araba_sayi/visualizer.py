from typing import List, Dict, Tuple
import cv2


Detection = Dict[str, object]


def draw_overlays(
    frame,
    detections: List[Detection],
    total_count: int,
    line_y: int,
    class_name_to_count: str = "car",
    show_class_count: bool = True,
    bbox_color_bgr: Tuple[int, int, int] = (0, 255, 0),
    line_color_bgr: Tuple[int, int, int] = (0, 0, 255),
):
    # Draw counting line
    height, width = frame.shape[:2]
    cv2.line(frame, (0, line_y), (width - 1, line_y), line_color_bgr, 2)

    # Draw detections
    for det in detections:
        bbox = det.get("bbox")  # xyxy
        if bbox is None:
            continue

        x1, y1, x2, y2 = [int(v) for v in bbox]
        cv2.rectangle(frame, (x1, y1), (x2, y2), bbox_color_bgr, 2)

        track_id = det.get("track_id")
        cls_name = det.get("class_name")
        conf = det.get("confidence")
        label = f"ID {int(track_id) if track_id is not None else -1} | {cls_name} | {conf:.2f}" if conf is not None else f"ID {int(track_id) if track_id is not None else -1} | {cls_name}"

        # Put label above bbox
        y_text = max(0, y1 - 10)
        cv2.putText(frame, label, (x1, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.5, bbox_color_bgr, 2, cv2.LINE_AA)

    # Draw total counter at top-left
    cv2.putText(
        frame,
        f"Total: {total_count}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    # Draw current in-frame class count (e.g., number of cars)
    if show_class_count and detections is not None:
        # count detections whose class_name matches class_name_to_count (case-insensitive)
        target = class_name_to_count.lower() if class_name_to_count is not None else "car"
        in_frame_count = 0
        for det in detections:
            cls_name = det.get("class_name")
            if cls_name is None:
                continue
            try:
                if str(cls_name).lower() == target:
                    in_frame_count += 1
            except Exception:
                # fallback: skip malformed class_name
                continue

        # Put the class count below the total counter
        cv2.putText(
            frame,
            f"Araba sayisi: {in_frame_count}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (139, 110, 183),
            2,
            cv2.LINE_AA,
        )

    return frame


