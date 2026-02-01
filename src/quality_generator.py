import os
import uuid

class BakinHighQualityGenerator:
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

    def generate_dialogue(self, text, speaker=""):
        # 制御文字 \w[sec] を使って「溜め」を作る
        # テキスト内の「...」を自動的にウェイト付きに変換するなどの処理が可能
        processed_text = text.replace("...", "...\\w[0.5]")
        display_text = f"【{speaker}】\\n{processed_text}" if speaker else processed_text
        
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

    def generate_screen_color(self, r, g, b, power=100, duration=1.0):
        # 画面の色を変える（セピア調、夜っぽくするなど）
        return f"""\t\tコマンド\tSCREEN_COLOR
\t\t\t整数\t{r}
\t\t\t整数\t{g}
\t\t\t整数\t{b}
\t\t\t整数\t{power}
\t\t\t小数\t{duration}
\t\t\t整数\t1
\t\tコマンド終了
"""

    def generate_camera(self, cam_guid, wait=True):
        # 指定したカメラ設定に切り替える（ズームや角度）
        return f"""\t\tコマンド\tCAM_ANIMATION
\t\t\tGuid\t{cam_guid}
\t\t\t整数\t0
\t\t\t整数\t{1 if wait else 0}
\t\tコマンド終了
"""

    def generate_wait(self, sec):
        return f"""\t\tコマンド\tWAIT
\t\t\t小数\t{sec}
\t\t\t整数\t0
\t\tコマンド終了
"""

    def generate_flash(self, r, g, b, duration=0.1):
        return f"""\t\tコマンド\tSCREEN_FLASH
\t\t\t整数\t{r}
\t\t\t整数\t{g}
\t\t\t整数\t{b}
\t\t\t整数\t255
\t\t\t小数\t{duration}
\t\t\t整数\t1
\t\tコマンド終了
"""

    def generate_shake(self, duration=0.5, power=1):
        return f"""\t\tコマンド\tSCREEN_SHAKE
\t\t\t小数\t{duration}
\t\t\t整数\t{power}
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

def produce_high_quality_horror():
    gen = BakinHighQualityGenerator()
    
    # ハイクオリティ・ホラー演出
    # 実際にはBakin側のカメラGuidを指定する必要がありますが、一旦aaa2.txtにいたGuidを借用します
    sample_cam = "4b9b4745-2de4-4236-8e49-ccc6719ef9f8" 
    
    commands = [
        # 1. 夜の雰囲気を出す（画面を青暗くする）
        gen.generate_screen_color(50, 50, 150, 150, 0.5),
        gen.generate_wait(1.0),
        
        # 2. キャラクターの独り言（ウェイト入り）
        gen.generate_dialogue("……おかしい。\\w[0.5]地図ではこの場所のはずだが。", "冒険者"),
        gen.generate_wait(0.5),
        
        # 3. 落雷の予兆
        gen.generate_flash(255, 255, 255, 0.05),
        gen.generate_wait(0.1),
        gen.generate_flash(255, 255, 255, 0.2),
        gen.generate_shake(1.0, 2),
        
        # 4. カメラを寄せる（緊迫感）
        gen.generate_camera(sample_cam, True),
        
        # 5. 決定的なセリフ
        gen.generate_dialogue("……\\w[1.0]うしろになにか……いる？", "冒険者"),
        
        # 6. 赤いフラッシュと同時に振り返る（演出）
        gen.generate_flash(200, 0, 0, 1.0),
        gen.generate_screen_color(255, 0, 0, 100, 0.1),
        gen.generate_dialogue("ぎゃあああああああ！！！！", "冒険者"),
        
        # 7. 画面を真っ暗にして終了
        gen.generate_screen_color(0, 0, 0, 255, 0.5)
    ]
    
    output_path = r"c:\repos\HD2Dmaker\output\high_quality_horror.txt"
    with open(output_path, "w", encoding="utf-16") as f:
        f.write(gen.generate_event("HighQualityHorror", commands))
    return output_path

if __name__ == "__main__":
    path = produce_high_quality_horror()
    print(f"『ハイクオリティ小劇場』を生成しました！\n場所: {path}")
