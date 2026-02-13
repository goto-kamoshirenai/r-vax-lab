import sys

import cv2
import numpy as np
import torch

from ..base import BaseDetector, DetectionResult
from ..registry import DetectorRegistry
from .config import DeepLSDConfig, DEFAULT_CONFIG

# DeepLSDのパスを追加
sys.path.insert(0, '/opt/DeepLSD')


@DetectorRegistry.register
class DeepLSDDetector(BaseDetector):
    """DeepLSDを使用した深層学習ベースの線分検出器"""

    def __init__(self, config: DeepLSDConfig | None = None):
        self.config = config or DEFAULT_CONFIG
        self._model = None
        self._device = None

    @property
    def name(self) -> str:
        return "DeepLSD"

    @property
    def output_dir(self) -> str:
        return "deeplsd"

    def _get_device(self) -> torch.device:
        """デバイスを取得"""
        if self._device is None:
            if self.config.device:
                self._device = torch.device(self.config.device)
            else:
                self._device = torch.device(
                    'cuda' if torch.cuda.is_available() else 'cpu'
                )
            print(f"[{self.name}] Using device: {self._device}")
        return self._device

    def _load_model(self):
        """モデルをロード（遅延ロード）"""
        if self._model is not None:
            return self._model

        from deeplsd.models.deeplsd_inference import DeepLSD

        device = self._get_device()

        # モデル設定
        model_conf = {
            'detect_lines': self.config.detect_lines,
            'line_detection_params': {
                'merge': self.config.merge_lines,
                'filtering': self.config.filtering,
                'grad_thresh': self.config.grad_thresh,
                'grad_nfa': self.config.grad_nfa,
            }
        }

        # モデルのロード
        self._model = DeepLSD(model_conf).to(device)
        checkpoint = torch.load(self.config.weights_path, map_location=device)
        self._model.load_state_dict(checkpoint['model'])
        self._model.eval()

        print(f"[{self.name}] Model loaded from: {self.config.weights_path}")
        return self._model

    def detect(self, image_path: str) -> DetectionResult:
        # 画像の読み込み
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image not found: {image_path}")

        height, width = img.shape[:2]

        # グレースケール変換
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # モデルのロード
        model = self._load_model()
        device = self._get_device()

        # テンソルに変換
        img_tensor = torch.tensor(
            gray, dtype=torch.float32, device=device
        )[None, None] / 255.0

        # 推論
        with torch.no_grad():
            outputs = model({'image': img_tensor})

        raw_lines = outputs['lines'][0]
        lines = raw_lines.cpu().numpy() if isinstance(raw_lines, torch.Tensor) else np.asarray(raw_lines)

        # DeepLSDは (N, 2, 2) 形式 [[x1,y1],[x2,y2]] で返すので (N, 4) に変換
        if lines.ndim == 3 and lines.shape[1:] == (2, 2):
            lines = lines.reshape(-1, 4)

        return DetectionResult(
            lines=lines,
            image_height=height,
            image_width=width,
        )
