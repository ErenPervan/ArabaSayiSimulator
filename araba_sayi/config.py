from dataclasses import dataclass, field
from typing import List, Dict, Optional


# Default COCO class index mapping used by YOLOv8
COCO_CLASS_NAME_TO_ID: Dict[str, int] = {
    "person": 0,
    "bicycle": 1,
    "car": 2,
    "motorcycle": 3,
    "airplane": 4,
    "bus": 5,
    "train": 6,
    "truck": 7,
    "boat": 8,
    "traffic light": 9,
    "fire hydrant": 10,
    "stop sign": 11,
    "parking meter": 12,
    "bench": 13,
    "bird": 14,
    "cat": 15,
    "dog": 16,
    "horse": 17,
    "sheep": 18,
    "cow": 19,
    "elephant": 20,
    "bear": 21,
    "zebra": 22,
    "giraffe": 23,
    "backpack": 24,
    "umbrella": 25,
    "handbag": 26,
    "tie": 27,
    "suitcase": 28,
    "frisbee": 29,
    "skis": 30,
    "snowboard": 31,
    "sports ball": 32,
    "kite": 33,
    "baseball bat": 34,
    "baseball glove": 35,
    "skateboard": 36,
    "surfboard": 37,
    "tennis racket": 38,
    "bottle": 39,
    "wine glass": 40,
    "cup": 41,
    "fork": 42,
    "knife": 43,
    "spoon": 44,
    "bowl": 45,
    "banana": 46,
    "apple": 47,
    "sandwich": 48,
    "orange": 49,
    "broccoli": 50,
    "carrot": 51,
    "hot dog": 52,
    "pizza": 53,
    "donut": 54,
    "cake": 55,
    "chair": 56,
    "couch": 57,
    "potted plant": 58,
    "bed": 59,
    "dining table": 60,
    "toilet": 61,
    "tv": 62,
    "laptop": 63,
    "mouse": 64,
    "remote": 65,
    "keyboard": 66,
    "cell phone": 67,
    "microwave": 68,
    "oven": 69,
    "toaster": 70,
    "sink": 71,
    "refrigerator": 72,
    "book": 73,
    "clock": 74,
    "vase": 75,
    "scissors": 76,
    "teddy bear": 77,
    "hair drier": 78,
    "toothbrush": 79,
}


@dataclass
class DetectionConfig:
    model_path: str = "yolov8n.pt"
    confidence_threshold: float = 0.60
    target_classes: List[str] = field(default_factory=lambda: ["car", "motorcycle", "bus", "truck","bicycle"])

    def class_ids(self) -> List[int]:
        ids: List[int] = []
        for name in self.target_classes:
            if name not in COCO_CLASS_NAME_TO_ID:
                continue
            ids.append(COCO_CLASS_NAME_TO_ID[name])
        return ids


@dataclass
class CountingConfig:
    axis: str = "Y"
    line_position: int = 360
    tolerance_px: int = 10


@dataclass
class VisualizationConfig:
    bbox_color_bgr: tuple = (0, 255, 0)  # Green
    line_color_bgr: tuple = (0, 0, 255)  # Red
    show_window: bool = True
    window_name: str = "Vehicle Counter"


@dataclass
class AppConfig:
    source: str
    detection: DetectionConfig = field(default_factory=DetectionConfig)
    counting: CountingConfig = field(default_factory=CountingConfig)
    viz: VisualizationConfig = field(default_factory=VisualizationConfig)
    output_path: Optional[str] = None
    max_frames: Optional[int] = None


