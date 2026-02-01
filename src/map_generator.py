from PIL import Image
import os

def generate_mansion_map_image(file_path):
    # 32x32ピクセルのマップ画像を生成
    # Bakinの「画像からマップ生成」では、色の違いを地形の違いとして認識させられます
    # 例: 黒(0,0,0)は壁/穴、茶色(139,69,19)は床、赤(255,0,0)はイベント配置用など
    
    width, height = 32, 32
    img = Image.new('RGB', (width, height), color=(0, 0, 0)) # 全体は壁(黒)
    pixels = img.load()

    # 廊下を作る (L字型の廊下)
    for x in range(5, 27):
        for y in range(12, 16):
            pixels[x, y] = (139, 69, 19) # 木の床っぽい色
    
    for x in range(22, 26):
        for y in range(16, 28):
            pixels[x, y] = (139, 69, 19)

    # 部屋を作る
    for x in range(6, 12):
        for y in range(16, 22):
            pixels[x, y] = (100, 100, 100) # 石畳っぽい色（個室）

    # 謎のマーク(イベント配置の目印)
    pixels[15, 13] = (255, 0, 0) 

    img.save(file_path)
    print(f"洋館の間取り画像を生成しました: {file_path}")

if __name__ == "__main__":
    output_dir = r"c:\repos\HD2Dmaker\output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    generate_mansion_map_image(os.path.join(output_dir, "mansion_layout.png"))
