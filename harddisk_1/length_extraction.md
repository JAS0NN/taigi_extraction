# 影片時長提取計畫

## 任務目標
計算 `./caption` 和 `./no_caption` 資料夾中每個子資料夾內影片的時長統計數據。資料夾結構為：
- `./caption/{date}/{drama_name}`
- `./no_caption/{drama_name}`

## 計畫步驟

### 步驟 1：環境設置
1. installed

### 步驟 2：開發 Python 腳本
1. **撰寫 Python 程式碼**：創建一個名為 `calculate_video_lengths.py` 的腳本，執行以下操作：
   - 遍歷 `./caption` 和 `./no_caption` 資料夾中的所有子資料夾。
   - 對每個 `.mp4` 檔案，使用 `ffmpeg-python` 提取時長。
   - 按子資料夾（例如 `caption/20250106/市井豪門`）彙總時長。
   - 輸出統計結果到控制台，並可選擇將結果保存到檔案。
2. **程式碼結構**：
   - 函數 `get_video_duration(file_path)`：使用 `ffmpeg.probe` 獲取單個影片的時長。
   - 函數 `scan_directory(base_path)`：掃描資料夾並計算每個子資料夾的總時長。
   - 主程式：調用 `scan_directory` 對 `./caption` 和 `./no_caption` 進行處理，並顯示結果。

### 步驟 3：執行與結果儲存
1. **執行腳本**：在啟用虛擬環境後，使用 `python calculate_video_lengths.py` 執行腳本。
2. **儲存結果**：腳本將結果輸出到控制台，並可選擇將結果寫入到 `video_length_statistics.txt` 檔案中，以便進一步參考。

### 步驟 4：文件記錄
1. **更新 Markdown 文件**：將計畫和執行步驟記錄到 `length_extraction.md` 中，包括環境設置、程式碼片段和執行指令。

## Mermaid 圖表 - 工作流程
```mermaid
graph TD
    A[創建虛擬環境] --> B[安裝 ffmpeg 和 ffmpeg-python]
    B --> C[撰寫 Python 腳本]
    C --> D[執行腳本計算時長]
    D --> E[儲存結果到檔案]
    E --> F[更新 length_extraction.md]