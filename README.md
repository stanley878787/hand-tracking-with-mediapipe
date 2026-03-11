# MediaPipe Hand Tracking AI Project

這是一個使用 `Python + OpenCV + MediaPipe` 建立的即時手部關鍵點偵測專案。  
專案聚焦在手部追蹤與基礎手勢分析，適合用來展示 AI / Computer Vision repo 的完整度。

目前已完成的功能：

- 開啟攝影機並即時讀取畫面
- 偵測單手或雙手
- 繪製 21 個手部關鍵點與骨架連線
- 顯示左右手分類與信心分數
- 判斷五根手指是否伸直
- 顯示 FPS、相機編號與鏡像狀態

## Features

- Real-time webcam hand tracking
- 21 landmarks per detected hand
- Left / Right hand classification
- Finger state analysis for thumb, index, middle, ring, and pinky
- Bounding box, FPS, and runtime status overlay
- Command-line arguments for camera and confidence settings

## Tech Stack

- Python
- OpenCV
- MediaPipe Hands
- NumPy

## Project Structure

```text
hand-tracking-with-mediapipe/
├─ app.py
├─ requirements.txt
├─ README.md
├─ src/
│  ├─ __init__.py
│  ├─ detector.py
│  ├─ drawer.py
│  ├─ finger_state.py
│  └─ models.py
└─ .gitignore
```

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

可選參數：

```bash
python app.py --camera 0 --width 1280 --height 720 --max-hands 2
python app.py --min-detection-confidence 0.7 --min-tracking-confidence 0.6
python app.py --no-flip
```

按 `q` 或 `Esc` 可結束程式。

## Implementation Overview

1. app.py 負責相機初始化、參數處理、主迴圈與畫面顯示。
2. src/models.py 定義 landmark 與 detection 資料結構。
3. src/detector.py 封裝 MediaPipe Hands，輸出 landmarks、邊界框、左右手結果與手指狀態。
4. src/drawer.py 負責畫出骨架、標籤、手指狀態與底部狀態列。
5. src/finger_state.py 使用關節角度與相對位置判斷五根手指是否伸直。

## Finger State Logic

- 食指、中指、無名指、小指：
  - 使用 `MCP-PIP-DIP` 的關節角度判斷是否接近伸直。
  - 再搭配 fingertip 與 PIP、wrist 的相對位置做過濾，降低誤判。
- 拇指：
  - 使用拇指關節角度。
  - 搭配左右手方向做水平延伸判斷。
  - 再加上與食指根部的相對高度，避免拇指貼在掌心時被誤判為伸直。

## Suggested GitHub Topics

- `ai`
- `computer-vision`
- `mediapipe`
- `hand-tracking`
- `opencv`
- `gesture-recognition`

## Next Steps

- 加入手勢辨識，例如 OK、讚、五指張開
- 支援截圖、錄影或輸出影片檔
- 新增圖片輸入模式與批次推論
- 補上單元測試與範例資料
