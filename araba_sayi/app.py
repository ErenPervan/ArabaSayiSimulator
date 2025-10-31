from typing import Optional, List
import cv2

from .config import AppConfig, COCO_CLASS_NAME_TO_ID
from .tracker import YoloByteTrack
from .counter import LineCrossCounter
from .visualizer import draw_overlays


def _init_writer_if_needed(writer, frame, output_path: Optional[str], fps: float):
    if writer is not None or not output_path:
        return writer
    height, width = frame.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps if fps > 0 else 30.0, (width, height))
    return writer


def run(config: AppConfig) -> int:
    # Prepare tracker
    tracker = YoloByteTrack(config.detection.model_path)

    # Prepare counter
    counter = LineCrossCounter(
        line_y=config.counting.line_position,
        tolerance_px=config.counting.tolerance_px,
    )

    # For name resolution (labels)
    id_to_name = {v: k for k, v in COCO_CLASS_NAME_TO_ID.items()}

    # Determine FPS via cv2.VideoCapture (for writer)
    cap = cv2.VideoCapture(config.source)
    fps = cap.get(cv2.CAP_PROP_FPS) if cap.isOpened() else 30.0
    if cap.isOpened():
        cap.release()

    writer = None

    frame_idx = 0
    try:
        for pkt in tracker.stream_track(
            source=config.source,
            conf=config.detection.confidence_threshold,
            class_ids=config.detection.class_ids(),
        ):
            frame = pkt["frame"]
            detections = pkt["detections"]

            # Enrich detections with class names for visualization
            for d in detections:
                cls_id = d.get("class_id", -1)
                d["class_name"] = id_to_name.get(cls_id, str(cls_id))

            # Update counter
            counter.update(detections)

            # Draw overlays
            draw_overlays(
                frame,
                detections,
                counter.total_count,
                config.counting.line_position,
                bbox_color_bgr=config.viz.bbox_color_bgr,
                line_color_bgr=config.viz.line_color_bgr,
            )

            # Writer
            writer = _init_writer_if_needed(writer, frame, config.output_path, fps)
            if writer is not None:
                writer.write(frame)

            # Display
            if config.viz.show_window:
                cv2.imshow(config.viz.window_name, frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            frame_idx += 1
            if config.max_frames is not None and frame_idx >= config.max_frames:
                break
    finally:
        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()

    return counter.total_count


