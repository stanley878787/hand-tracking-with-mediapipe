# MediaPipe Hand Tracking AI Project

使用 `Python + OpenCV + MediaPipe` 建立的即時手部關鍵點偵測專案。

這個專案可以作為 AI / Computer Vision 課程或 GitHub 作品集的基礎專案，核心功能包含：

- 開啟攝影機並即時讀取畫面
- 偵測單手或雙手
- 繪製 21 個手部關鍵點與骨架連線
- 顯示左右手分類與信心分數
- 判斷五根手指是否伸直
- 顯示基礎手勢名稱
- 按 `S` 儲存目前畫面截圖
- 顯示 FPS、相機編號與鏡像狀態

## Features

- Real-time webcam hand tracking
- 21 landmarks per detected hand
- Left / Right hand classification
- Finger state analysis for thumb, index, middle, ring, and pinky
- Basic gesture recognition: `Open Palm`, `Fist`, `Thumbs Up`, `Pointing Up`, `Victory`
- Bounding box, FPS, and runtime status overlay
- Screenshot capture to local files
- Single-image inference mode with saved output image
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
├─ outputs/
├─ src/
│  ├─ __init__.py
│  ├─ detector.py
│  ├─ drawer.py
│  ├─ finger_state.py
│  ├─ gesture_recognition.py
│  ├─ models.py
│  └─ utils.py
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

快捷鍵：

- `q` 或 `Esc`: 結束程式
- `s`: 將目前畫面儲存到 `captures/`

單張圖片模式：

```bash
python app.py --image input.jpg
python app.py --image input.jpg --output outputs/result.png
```

執行後會：

- 在終端顯示偵測到的手數量
- 列出每隻手的左右手、手勢名稱、五指狀態
- 將標註後的圖片輸出到 `outputs/`

## Implementation Overview

1. [app.py](/c:/Users/User/Desktop/nkust/project/hand-tracking-with-mediapipe/app.py)
   負責相機初始化、命令列參數、主迴圈與畫面顯示。
2. [src/models.py](/c:/Users/User/Desktop/nkust/project/hand-tracking-with-mediapipe/src/models.py)
   定義 landmark 與 detection 的資料結構。
3. [src/detector.py](/c:/Users/User/Desktop/nkust/project/hand-tracking-with-mediapipe/src/detector.py)
   封裝 MediaPipe Hands，輸出 landmarks、bounding box、左右手結果與手指狀態。
4. [src/finger_state.py](/c:/Users/User/Desktop/nkust/project/hand-tracking-with-mediapipe/src/finger_state.py)
   使用關節角度與相對位置判斷五根手指是否伸直。
5. [src/gesture_recognition.py](/c:/Users/User/Desktop/nkust/project/hand-tracking-with-mediapipe/src/gesture_recognition.py)
   根據 landmarks 與手指狀態輸出基礎手勢名稱。
6. [src/drawer.py](/c:/Users/User/Desktop/nkust/project/hand-tracking-with-mediapipe/src/drawer.py)
   負責畫出骨架、標籤、手勢名稱、手指狀態與底部狀態列。
7. [src/utils.py](/c:/Users/User/Desktop/nkust/project/hand-tracking-with-mediapipe/src/utils.py)
   負責截圖儲存等通用工具。

## Finger State Logic

- 食指、中指、無名指、小指：
  - 使用 `MCP-PIP-DIP` 關節角度判斷是否接近伸直。
  - 搭配 fingertip、PIP、wrist 的相對位置做額外過濾，降低誤判。
- 拇指：
  - 使用拇指關節角度。
  - 搭配左右手方向判斷水平伸出方向。
  - 再使用與食指根部的相對高度，避免拇指收進掌心時誤判。

## Suggested GitHub Topics

- `ai`
- `computer-vision`
- `mediapipe`
- `hand-tracking`
- `opencv`
- `gesture-recognition`

## Suggested Commit Split

如果你想增加合理的 commit 數量，可以拆成這幾次：

1. `feat: add MediaPipe hand tracking project skeleton`
2. `feat: add finger state analysis and bounding box overlay`
3. `feat: add basic gesture recognition`
4. `feat: add screenshot capture support`
5. `feat: add single image inference mode`
6. `docs: improve README and project usage instructions`

## Next Steps

- 加入更多手勢，例如 `OK`、`Rock`、`Call Me`
- 支援錄影或輸出影片檔
- 新增批次推論
- 補上單元測試與範例資料
