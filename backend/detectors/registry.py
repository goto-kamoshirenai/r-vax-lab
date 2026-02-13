from typing import Type

from .base import BaseDetector


class DetectorRegistry:
    """検出器を管理するレジストリ"""

    _detectors: dict[str, Type[BaseDetector]] = {}

    @classmethod
    def register(cls, detector_class: Type[BaseDetector]) -> Type[BaseDetector]:
        """検出器を登録するデコレータ"""
        instance = detector_class()
        cls._detectors[instance.output_dir] = detector_class
        return detector_class

    @classmethod
    def get(cls, name: str) -> BaseDetector:
        """名前から検出器インスタンスを取得"""
        if name not in cls._detectors:
            available = ', '.join(cls._detectors.keys())
            raise ValueError(f"Unknown detector: {name}. Available: {available}")
        return cls._detectors[name]()

    @classmethod
    def list_available(cls) -> list[str]:
        """利用可能な検出器の一覧を取得"""
        return list(cls._detectors.keys())
