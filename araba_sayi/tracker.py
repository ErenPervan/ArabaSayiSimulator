from typing import Dict, Generator, List
import numpy as np


try:
    from ultralytics import YOLO
except Exception as exc:  # pragma: no cover - import-time guard
    raise RuntimeError(
        "Ultralytics paketini yükleyin: pip install ultralytics"
    ) from exc


Detection = Dict[str, object]


class YoloByteTrack:
    def __init__(self, model_path: str) -> None:
        self.model = YOLO(model_path)

    def stream_track(
        self,
        source: str,
        conf: float,
        class_ids: List[int],
    ) -> Generator[Dict[str, object], None, None]:
        results_gen = self.model.track(
            source=source,
            stream=True,
            conf=conf,
            classes=class_ids if class_ids else None,
            tracker="bytetrack.yaml",
            verbose=False,
            persist=True,
        )

        for result in results_gen:
            # original frame
            frame = result.orig_img

            detections: List[Detection] = []
            boxes = getattr(result, "boxes", None)
            if boxes is not None and boxes.id is not None:
                ids = boxes.id.cpu().numpy().astype(int)
                xyxy = boxes.xyxy.cpu().numpy()
                confs = boxes.conf.cpu().numpy() if boxes.conf is not None else np.zeros((len(xyxy),), dtype=float)
                clss = boxes.cls.cpu().numpy().astype(int) if boxes.cls is not None else np.full((len(xyxy),), -1, dtype=int)

                for i in range(len(xyxy)):
                    x1, y1, x2, y2 = xyxy[i].tolist()
                    cx = 0.5 * (x1 + x2)
                    cy = 0.5 * (y1 + y2)
                    detections.append(
                        {
                            "track_id": int(ids[i]),
                            "bbox": (x1, y1, x2, y2),
                            "center": (cx, cy),
                            "confidence": float(confs[i]),
                            "class_id": int(clss[i]),
                        }
                    )

            yield {
                "frame": frame,
                "detections": detections,
            }


