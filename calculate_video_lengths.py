import os
import ffmpeg
from collections import defaultdict
import csv
import json

def get_video_duration(file_path):
    """獲取單個影片檔案的時長（秒）"""
    try:
        probe = ffmpeg.probe(file_path)
        duration = float(probe['format']['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f"無法獲取 {file_path} 的時長: {e.stderr.decode()}")
        return 0

def extract_drama_name(folder_path, base_path):
    """從資料夾路徑中提取連續劇名稱"""
    relative_path = os.path.relpath(folder_path, base_path)
    parts = relative_path.split(os.sep)
    if base_path == './caption' and len(parts) >= 2:
        return parts[1]  # caption/{date}/{drama_name}
    elif base_path == './no_caption' and len(parts) >= 1:
        return parts[0]  # no_caption/{drama_name}
    return relative_path

def scan_directory(base_path, skipped_dramas):
    """掃描資料夾並計算每個子資料夾和連續劇的總時長，跳過已計算的連續劇"""
    folder_durations = defaultdict(float)
    drama_durations = defaultdict(float)
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.mp4'):
                file_path = os.path.join(root, file)
                duration = get_video_duration(file_path)
                if duration > 0:
                    folder_durations[root] += duration
                    drama_name = extract_drama_name(root, base_path)
                    if drama_name not in skipped_dramas:
                        drama_durations[drama_name] += duration
                        print(f"檔案 {file_path} 時長: {duration:.2f} 秒")
                    else:
                        print(f"跳過連續劇 {drama_name} 的檔案 {file_path}")
    
    return folder_durations, drama_durations

def format_duration(seconds):
    """將秒數格式化為小時:分鐘:秒"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def save_to_csv(drama_durations, filename='drama_duration_statistics.csv'):
    """將連續劇時長統計保存到 CSV 檔案"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['連續劇名稱', '總時長 (格式化)', '總秒數', '累計小時數'])
        for drama, duration in drama_durations.items():
            hours = duration / 3600
            writer.writerow([drama, format_duration(duration), f"{duration:.2f}", f"{hours:.2f}"])
    print(f"\n連續劇時長統計已保存到 {filename}")

def main():
    # 讀取已計算的連續劇名稱
    try:
        with open('drama_names.json', 'r', encoding='utf-8') as f:
            skipped_dramas = json.load(f)
        print(f"已從 drama_names.json 讀取 {len(skipped_dramas)} 個連續劇名稱，將跳過這些連續劇的時長計算。")
    except Exception as e:
        print(f"無法讀取 drama_names.json: {e}")
        skipped_dramas = []

    # 掃描 caption 資料夾
    print("掃描 ./caption 資料夾...")
    caption_folder_durations, caption_drama_durations = scan_directory('./caption', skipped_dramas)
    
    # 掃描 no_caption 資料夾
    print("\n掃描 ./no_caption 資料夾...")
    no_caption_folder_durations, no_caption_drama_durations = scan_directory('./no_caption', skipped_dramas)
    
    # 輸出結果
    print("\n=== caption 資料夾時長統計 ===")
    for folder, duration in caption_folder_durations.items():
        print(f"{folder}: {format_duration(duration)} (總秒數: {duration:.2f})")
    
    print("\n=== no_caption 資料夾時長統計 ===")
    for folder, duration in no_caption_folder_durations.items():
        print(f"{folder}: {format_duration(duration)} (總秒數: {duration:.2f})")
    
    print("\n=== caption 連續劇總時長統計 ===")
    for drama, duration in caption_drama_durations.items():
        print(f"{drama}: {format_duration(duration)} (總秒數: {duration:.2f})")
    
    print("\n=== no_caption 連續劇總時長統計 ===")
    for drama, duration in no_caption_drama_durations.items():
        print(f"{drama}: {format_duration(duration)} (總秒數: {duration:.2f})")
    
    # 將結果保存到檔案
    with open('video_length_statistics.txt', 'w', encoding='utf-8') as f:
        f.write("=== caption 資料夾時長統計 ===\n")
        for folder, duration in caption_folder_durations.items():
            f.write(f"{folder}: {format_duration(duration)} (總秒數: {duration:.2f})\n")
        
        f.write("\n=== no_caption 資料夾時長統計 ===\n")
        for folder, duration in no_caption_folder_durations.items():
            f.write(f"{folder}: {format_duration(duration)} (總秒數: {duration:.2f})\n")
        
        f.write("\n=== caption 連續劇總時長統計 ===\n")
        for drama, duration in caption_drama_durations.items():
            f.write(f"{drama}: {format_duration(duration)} (總秒數: {duration:.2f})\n")
        
        f.write("\n=== no_caption 連續劇總時長統計 ===\n")
        for drama, duration in no_caption_drama_durations.items():
            f.write(f"{drama}: {format_duration(duration)} (總秒數: {duration:.2f})\n")
    
    print("\n結果已保存到 video_length_statistics.txt")
    
    # 將連續劇時長分別保存到兩個 CSV 檔案
    save_to_csv(caption_drama_durations, 'caption_drama_duration_statistics.csv')
    save_to_csv(no_caption_drama_durations, 'no_caption_drama_duration_statistics.csv')

if __name__ == "__main__":
    main()