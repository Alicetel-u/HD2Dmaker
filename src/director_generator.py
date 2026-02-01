import os
import uuid

class BakinDirectorGenerator:
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

    def generate_move_event_to(self, target_guid, x, z, y=0):
        # 指定したイベントを指定した座標(x, z, y)に瞬間移動させる
        # ※スポット指定の形式はaaa.txt/aaa2.txtの解析を元に再現
        # 形式例: 479f0fec-878d-4137-ad5b-235dac32b714|1001|8.5|3.75|17.5
        # ここでは座標指定のみを模擬する形式で作成
        return f"""\t\tコマンド\tPLMOVE
\t\t\tスポット\t00000000-0000-0000-0000-000000000000|0|{x}|{y}|{z}
\t\t\t整数\t0
\t\tコマンド終了
"""

    def generate_change_graphic(self, cast_guid, motion=""):
        # キャラクターの見た目を変更する
        return f"""\t\tコマンド\tPLGRAPHIC
\t\t\t整数\t0
\t\t\tGuid\t{cast_guid}
\t\t\t整数\t0
\t\t\tGuid\t00000000-0000-0000-0000-000000000000
\t\t\tGuid\t00000000-0000-0000-0000-000000000000
\t\t\t文字列\t{motion}
\t\t\t整数\t0
\t\t\t整数\t0
\t\t\t整数\t1
\t\t\t整数\t0
\t\t\tGuid\t00000000-0000-0000-0000-000000000000
\t\t\t整数\t0
\t\t\t整数\t0
\t\tコマンド終了
"""

    def generate_dialogue(self, text, speaker=""):
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

    def generate_wait(self, sec):
        return f"""\t\tコマンド\tWAIT
\t\t\t小数\t{sec}
\t\t\t整数\t0
\t\tコマンド終了
"""

    def generate_event(self, event_name, commands):
        guid = str(uuid.uuid4())
        content = self.template_start.format(guid=guid, event_name=event_name)
        for cmd in commands:
            content += cmd
        content += self.template_end
        return content

def produce_auto_placement_drama():
    gen = BakinDirectorGenerator()
    
    # キャラクター定義（Bakin側のリソースGuidが必要ですが、一旦サンプルを使用）
    HERO_GUID = "9ee62641-4119-452e-9556-57bda9919d83" # 格闘家A
    GHOST_GUID = "00000000-0000-0000-0000-000000000000" # デフォルト
    
    commands = [
        # 1. 開演前の「キャラ配置」 (プレイヤーを特定の位置へ)
        # 廊下の奥(x=15, z=13)に瞬間移動
        gen.generate_move_event_to(HERO_GUID, 15, 13, 3.75),
        gen.generate_wait(0.1),
        
        # 2. 配役（グラフィック設定）
        gen.generate_change_graphic(HERO_GUID, "WAIT"),
        
        # 3. 劇の開始
        gen.generate_dialogue("よし、位置についたな。...", "システム"),
        gen.generate_dialogue("ここが指定された場所か。...", "冒険者"),
        
        # 4. キャラクターを動かす演出
        # ここで別のイベント(幽霊役など)がいれば、それも移動させられますが、
        # 現状はプレイヤーキャラ1人の制御を中心にしています。
        
        gen.generate_dialogue("誰か……\\w[1.0]いるのか？", "冒険者"),
        gen.generate_wait(1.0),
        gen.generate_dialogue("……だ……れ……も……い……な……い……よ……", "壁の声"),
        
        # 5. 驚きのリアクション
        gen.generate_dialogue("！？", "冒険者")
    ]
    
    output_path = r"c:\repos\HD2Dmaker\output\auto_placement_drama.txt"
    with open(output_path, "w", encoding="utf-16") as f:
        f.write(gen.generate_event("AutoPlacementDrama", commands))
    return output_path

if __name__ == "__main__":
    path = produce_auto_placement_drama()
    print(f"『キャラ配置自動化・小劇場』を生成しました！\n場所: {path}")
