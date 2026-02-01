import os
import uuid

class BakinEventGenerator:
    def __init__(self):
        self.template_start = """Guid\t{guid}
イベント名\t{event_name}
シート\tイベントシート
\tグラフィック\t00000000-0000-0000-0000-000000000000
\t向き\t-1
\t向き固定\tFalse
\t物理\tFalse
\t衝突判定\tTrue
\tイベントと衝突\tTrue
\t移動速度\t0
\t移動頻度\t0
\t移動タイプ\tNONE
\t押せる\tTrue
\tスクリプト
\t\t開始条件\tTALK
\t\t高さ無視\tFalse
\t\t判定拡張\tTrue
"""
        self.template_end = """\tスクリプト終了
シート終了
"""

    def generate_dialogue(self, text, speaker_name=""):
        # speaker_nameはBakin側の設定に依存するが、ここではテキストに含める形式
        display_text = f"【{speaker_name}】\\n{text}" if speaker_name else text
        return f"""\t\tコマンド\tDIALOGUE
\t\t\t文字列\t{display_text}
\t\t\t整数\t2
\t\t\t整数\t0
\t\t\tGuid\t00000000-0000-0000-0000-000000000000
\t\t\t文字列\t
\t\t\tGuid\t00000000-0000-0000-0000-000000000000
\t\t\t文字列\t
\t\t\t整数\t0
\t\t\t整数\t0
\t\t\t整数\t1
\t\t\t整数\t1
\t\t\t整数\t0
\t\t\t整数\t0
\t\t\t文字列\t
\t\t\t文字列\t
\t\tコマンド終了
"""

    def generate_shake(self, duration=0.5, power=1):
        return f"""\t\tコマンド\tSCREEN_SHAKE
\t\t\t小数\t{duration}
\t\t\t整数\t{power}
\t\t\t整数\t1
\t\tコマンド終了
"""

    def generate_plwalk(self, steps=1, direction=0): # 0:上 1:右 2:下 3:左 (Bakinの内部値に合わせる必要があるが一旦仮)
        return f"""\t\tコマンド\tPLWALK
\t\t\t整数\t{direction}
\t\t\t小数\t{steps}
\t\t\t整数\t0
\t\t\t整数\t1
\t\t\t整数\t0
\t\t\t整数\t0
\t\t\t整数\t0
\t\t\t整数\t0
\t\t\t整数\t0
\t\t\t整数\t0
\t\t\t整数\t0
\t\tコマンド終了
"""

    def generate_wait(self, sec=0.5):
        return f"""\t\tコマンド\tWAIT
\t\t\t小数\t{sec}
\t\t\t整数\t0
\t\tコマンド終了
"""

    def generate_flash(self, color=(255, 255, 255), duration=0.2):
        # 画面をフラッシュさせる演出
        r, g, b = color
        return f"""\t\tコマンド\tSCREEN_FLASH
\t\t\t整数\t{r}
\t\t\t整数\t{g}
\t\t\t整数\t{b}
\t\t\t整数\t255
\t\t\t小数\t{duration}
\t\t\t整数\t1
\t\tコマンド終了
"""

    def generate_event(self, event_name, commands):
        guid = str(uuid.uuid4())
        content = self.template_start.format(guid=guid, event_name=event_name)
        for cmd in commands:
            content += cmd
        content += self.template_end
        return content

def create_mansion_drama():
    gen = BakinEventGenerator()
    
    # 洋館ストーリー：落雷と不気味な声、そして逃走
    commands = [
        gen.generate_flash((255, 255, 255), 0.1), # 雷1
        gen.generate_wait(0.1),
        gen.generate_flash((255, 255, 255), 0.3), # 雷2
        gen.generate_dialogue("（ゴロゴロ…ッ！）", "演出"),
        gen.generate_dialogue("お、おい…なんだか不気味な屋敷だな…。", "冒険者"),
        gen.generate_wait(0.8),
        gen.generate_dialogue("……だ……れ……だ……", "？？？"),
        gen.generate_shake(1.0, 3), # 壁が崩れそうな激しい揺れ
        gen.generate_dialogue("ひ、ひぃ！ 誰かいるのか！？", "冒険者"),
        gen.generate_plwalk(2, 2), # 2歩後退
        gen.generate_dialogue("……帰……れ……ッ！", "？？？"),
        gen.generate_flash((200, 0, 0), 0.5), # 赤いフラッシュ
        gen.generate_dialogue("退却だ！ 逃げるぞ！！", "冒険者")
    ]
    
    output_path = r"c:\repos\HD2Dmaker\output\mansion_drama.txt"
    with open(output_path, "w", encoding="utf-16") as f:
        f.write(gen.generate_event("MansionDrama", commands))
    return output_path

if __name__ == "__main__":
    # path = create_omakase_drama() 
    path = create_mansion_drama()
    print(f"『洋館小劇場』ファイルを生成しました！\n場所: {path}")
