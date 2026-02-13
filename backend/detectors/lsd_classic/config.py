from dataclasses import dataclass

import cv2


@dataclass
class LSDClassicConfig:
    """古典的LSDの設定"""

    # LSDの精度設定
    # cv2.LSD_REFINE_NONE: 精度低・高速
    # cv2.LSD_REFINE_STD: 標準（デフォルト）
    # cv2.LSD_REFINE_ADV: 精度高・低速
    refine_mode: int = cv2.LSD_REFINE_STD

    # スケールファクター（0.0-1.0、小さいほど高速だが精度低下）
    scale: float = 0.8

    # シグマスケール（ガウシアンフィルタのスケール）
    sigma_scale: float = 0.6

    # 角度許容差（度）
    angle_tolerance: float = 22.5

    # 密度閾値（0.0-1.0）
    density_threshold: float = 0.7

    # NFA閾値（負の値ほど厳しい）
    n_bins: int = 1024


# デフォルト設定
DEFAULT_CONFIG = LSDClassicConfig()

# 高精度設定（処理時間は長くなる）
HIGH_ACCURACY_CONFIG = LSDClassicConfig(
    refine_mode=cv2.LSD_REFINE_ADV,
    scale=1.0,
)

# 高速設定（精度は低下する）
FAST_CONFIG = LSDClassicConfig(
    refine_mode=cv2.LSD_REFINE_NONE,
    scale=0.5,
)
