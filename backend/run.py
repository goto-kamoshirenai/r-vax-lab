#!/usr/bin/env python
"""
線分検出の統一実行スクリプト

Usage:
    # 利用可能な検出器を一覧表示
    python run.py --list

    # 特定の検出器で実行
    python run.py --detector lsd_classic
    python run.py --detector deeplsd

    # すべての検出器で実行（比較用）
    python run.py --all

    # カスタム入出力パス
    python run.py --detector deeplsd --input data/input/custom.png --output data/output/custom
"""

import argparse
import sys
from pathlib import Path

# 検出器の登録（インポート時に自動登録される）
from detectors import DetectorRegistry
from detectors.lsd_classic import LSDClassicDetector
from detectors.deeplsd import DeepLSDDetector


def get_default_paths():
    """デフォルトの入出力パスを取得"""
    return {
        'input': Path('data/input/test_drawing.png'),
        'output_base': Path('data/output'),
    }


def run_detector(detector_name: str, input_path: Path, output_base: Path) -> None:
    """指定された検出器を実行"""
    detector = DetectorRegistry.get(detector_name)
    output_path = output_base / detector.output_dir / 'result.dxf'

    detector.process(str(input_path), str(output_path))


def run_all_detectors(input_path: Path, output_base: Path) -> None:
    """すべての検出器を実行して比較"""
    print("=" * 60)
    print("Running all detectors for comparison")
    print("=" * 60)

    results = {}
    for name in DetectorRegistry.list_available():
        print(f"\n{'─' * 40}")
        try:
            detector = DetectorRegistry.get(name)
            output_path = output_base / detector.output_dir / 'result.dxf'
            result = detector.process(str(input_path), str(output_path))
            results[name] = len(result.lines)
        except Exception as e:
            print(f"[{name}] Error: {e}")
            results[name] = None

    # 比較結果の表示
    print(f"\n{'=' * 60}")
    print("Comparison Results")
    print("=" * 60)
    print(f"{'Detector':<20} {'Lines Detected':<15}")
    print("-" * 35)
    for name, count in results.items():
        count_str = str(count) if count is not None else "Error"
        print(f"{name:<20} {count_str:<15}")


def main():
    parser = argparse.ArgumentParser(
        description='Line Segment Detection Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--detector', '-d',
        type=str,
        help='Detector to use (e.g., lsd_classic, deeplsd)'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available detectors'
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Run all available detectors'
    )
    parser.add_argument(
        '--input', '-i',
        type=Path,
        help='Input image path'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output base directory'
    )

    args = parser.parse_args()

    # デフォルトパスの取得
    defaults = get_default_paths()
    input_path = args.input or defaults['input']
    output_base = args.output or defaults['output_base']

    # 利用可能な検出器の一覧表示
    if args.list:
        print("Available detectors:")
        for name in DetectorRegistry.list_available():
            detector = DetectorRegistry.get(name)
            print(f"  - {name}: {detector.name}")
        return

    # 入力ファイルの確認
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        print("Please place your image in data/input/ directory.")
        sys.exit(1)

    # 全検出器で実行
    if args.all:
        run_all_detectors(input_path, output_base)
        return

    # 特定の検出器で実行
    if args.detector:
        try:
            run_detector(args.detector, input_path, output_base)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        return

    # 引数なしの場合はヘルプを表示
    parser.print_help()


if __name__ == '__main__':
    main()
