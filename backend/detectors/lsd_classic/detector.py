import cv2
import numpy as np

from ..base import BaseDetector, DetectionResult
from ..registry import DetectorRegistry
from .config import LSDClassicConfig, DEFAULT_CONFIG


@DetectorRegistry.register
class LSDClassicDetector(BaseDetector):
    """OpenCVの古典的LSD（Line Segment Detector）を使用した検出器"""

    def __init__(self, config: LSDClassicConfig | None = None):
        self.config = config or DEFAULT_CONFIG

    @property
    def name(self) -> str:
        return "LSD Classic"

    @property
    def output_dir(self) -> str:
        return "lsd_classic"

    def detect(self, image_path: str) -> DetectionResult:
        # 画像の読み込み
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image not found: {image_path}")

        height, width = img.shape[:2]

        # グレースケール変換
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # LSD検出器の作成
        lsd = cv2.createLineSegmentDetector(self.config.refine_mode)

        # 線分検出
        lines, widths, precisions, nfa = lsd.detect(gray)

        if lines is None:
            return DetectionResult(
                lines=np.array([]).reshape(0, 4),
                image_height=height,
                image_width=width,
            )

        # shape: (N, 1, 4) -> (N, 4)
        lines = lines.reshape(-1, 4)

        return DetectionResult(
            lines=lines,
            image_height=height,
            image_width=width,
        )
