import cv2
import ezdxf
import numpy as np
import os

def extract_lines_to_dxf(image_path, output_path):
    # 1. 画像の読み込み
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: {image_path} が見つかりません。")
        return

    # 2. 前処理（グレースケール化）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 3. 線分検出 (LSD: Line Segment Detector)
    # 建築図面のようなハッキリした線に強いアルゴリズムです
    lsd = cv2.createLineSegmentDetector(cv2.LSD_REFINE_STD)
    lines, width, prec, nfa = lsd.detect(gray)

    # 4. DXFの作成
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    
    # 画像の高さ（座標変換用）
    height = img.shape[0]

    if lines is not None:
        print(f"Detected {len(lines)} line segments.")
        for line in lines:
            # line[0] には [x1, y1, x2, y2] が格納されている
            x1, y1, x2, y2 = line[0]
            
            # 重要：画像(左上が0)からCAD(左下が0)への座標変換
            # y座標を「高さ - y」で反転させます
            start_point = (x1, height - y1)
            end_point = (x2, height - y2)
            
            # DXFに線を追加
            msp.add_line(start_point, end_point)
    else:
        print("線分が検出されませんでした。")

    # 5. 保存
    doc.saveas(output_path)
    print(f"Success: {output_path} に書き出しました。")

if __name__ == "__main__":
    # パス設定（dataフォルダに画像を置いてください）
    INPUT_IMG = "data/test_drawing.png"
    OUTPUT_DXF = "data/result.dxf"
    
    if not os.path.exists("data"):
        os.makedirs("data")
        
    extract_lines_to_dxf(INPUT_IMG, OUTPUT_DXF)