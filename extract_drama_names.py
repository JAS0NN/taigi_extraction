import csv
import os
import json

def read_drama_names(file_path):
    drama_names = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳過標頭行
        for row in reader:
            if row and len(row) > 0:
                drama_names.add(row[0].strip())
    return drama_names

def main():
    caption_file = 'harddisk_1/caption_drama_duration_statistics.csv'
    no_caption_file = 'harddisk_1/no_caption_drama_duration_statistics.csv'
    
    caption_dramas = read_drama_names(caption_file)
    no_caption_dramas = read_drama_names(no_caption_file)
    
    all_dramas = caption_dramas.union(no_caption_dramas)
    
    print("戲劇名稱集合:")
    for drama in sorted(all_dramas):
        print(drama)
    print(f"\n總共 {len(all_dramas)} 部戲劇")
    
    # 將戲劇名稱存儲到列表並保存到 JSON 檔案
    drama_list = sorted(list(all_dramas))
    with open('drama_names.json', 'w', encoding='utf-8') as f:
        json.dump(drama_list, f, ensure_ascii=False, indent=2)
    print("\n已將戲劇名稱存儲到 drama_names.json 檔案中")

if __name__ == "__main__":
    main()