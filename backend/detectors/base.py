from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import cv2
import ezdxf
import numpy as np


@dataclass
class DetectionResult:
    """線分検出の結果を保持するデータクラス"""
    lines: np.ndarray  # shape: (N, 4) - [x1, y1, x2, y2]
    image_height: int
    image_width: int


class BaseDetector(ABC):
    """線分検出器の基底クラス"""

    @property
    @abstractmethod
    def name(self) -> str:
        """検出器の名前"""
        pass

    @property
    @abstractmethod
    def output_dir(self) -> str:
        """出力ディレクトリ名"""
        pass

    @abstractmethod
    def detect(self, image_path: str) -> DetectionResult:
        """
        画像から線分を検出する

        Args:
            image_path: 入力画像のパス

        Returns:
            DetectionResult: 検出結果
        """
        pass

    def save_to_dxf(self, result: DetectionResult, output_path: str) -> None:
        """
        検出結果をDXFファイルに保存する

        Args:
            result: 検出結果
            output_path: 出力ファイルパス
        """
        doc = ezdxf.new(setup=True)
        msp = doc.modelspace()

        for line in result.lines:
            x1, y1, x2, y2 = line
            # 画像座標(左上が原点)からCAD座標(左下が原点)への変換
            start_point = (float(x1), float(result.image_height - y1))
            end_point = (float(x2), float(result.image_height - y2))
            msp.add_line(start_point, end_point)

        # 出力ディレクトリの作成
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        doc.saveas(output_path)

    def process(self, image_path: str, output_path: str) -> DetectionResult:
        """
        画像処理のメインフロー

        Args:
            image_path: 入力画像パス
            output_path: 出力DXFパス

        Returns:
            DetectionResult: 検出結果
        """
        print(f"[{self.name}] Processing: {image_path}")

        result = self.detect(image_path)
        print(f"[{self.name}] Detected {len(result.lines)} line segments.")

        self.save_to_dxf(result, output_path)
        print(f"[{self.name}] Saved to: {output_path}")

        return result
