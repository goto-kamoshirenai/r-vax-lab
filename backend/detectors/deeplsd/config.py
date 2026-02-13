import os
from dataclasses import dataclass, field


@dataclass
class DeepLSDConfig:
    """DeepLSDの設定"""

    # モデルの重みファイルパス
    weights_path: str = field(
        default_factory=lambda: os.environ.get(
            'DEEPLSD_WEIGHTS',
            '/opt/DeepLSD/weights/deeplsd_wireframe.pth'
        )
    )

    # 線分検出を有効にする
    detect_lines: bool = True

    # 線分をマージするか
    merge_lines: bool = False

    # フィルタリングを有効にする
    filtering: bool = True

    # 勾配閾値
    grad_thresh: int = 3

    # 勾配NFA（Number of False Alarms）を使用するか
    grad_nfa: bool = True

    # デバイス（None の場合は自動選択）
    device: str | None = None


# デフォルト設定（室内向け、Wireframeモデル使用）
DEFAULT_CONFIG = DeepLSDConfig()

# 高感度設定（より多くの線分を検出）
HIGH_SENSITIVITY_CONFIG = DeepLSDConfig(
    grad_thresh=2,
    filtering=False,
)

# 厳格設定（ノイズの多い画像向け）
STRICT_CONFIG = DeepLSDConfig(
    grad_thresh=5,
    filtering=True,
    merge_lines=True,
)
