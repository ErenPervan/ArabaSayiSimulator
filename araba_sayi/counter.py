from dataclasses import dataclass, field
from typing import Dict, Set, Tuple, List


Detection = Dict[str, object]


@dataclass
class LineCrossCounter:
    line_y: int
    tolerance_px: int = 10
    counted_track_ids: Set[int] = field(default_factory=set)
    last_center_y_by_id: Dict[int, float] = field(default_factory=dict)
    total_count: int = 0

    def update(self, detections: List[Detection]) -> None:
        for det in detections:
            track_id = det.get("track_id")
            center = det.get("center")  # (cx, cy)
            if track_id is None or center is None:
                continue

            cy: float = float(center[1])

            # If already counted, skip processing to keep uniqueness invariant
            if track_id in self.counted_track_ids:
                self.last_center_y_by_id[track_id] = cy
                continue

            prev_cy = self.last_center_y_by_id.get(track_id)
            if prev_cy is None:
                self.last_center_y_by_id[track_id] = cy
                continue

            band_min = self.line_y - self.tolerance_px
            band_max = self.line_y + self.tolerance_px

            crossed = (
                (prev_cy < band_min and cy > band_max) or
                (prev_cy > band_max and cy < band_min) or
                # Edge case: stepped exactly into the band and out
                (prev_cy < self.line_y <= cy) or
                (prev_cy > self.line_y >= cy)
            )

            if crossed:
                self.total_count += 1
                self.counted_track_ids.add(track_id)

            self.last_center_y_by_id[track_id] = cy


