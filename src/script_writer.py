"""
HD2Dmaker 台本ジェネレーター
BAKIN用の自動演出台本を簡単に作成するためのPythonライブラリ
"""

import os
from typing import List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class Script:
    """台本クラス - コマンドを蓄積して出力"""
    commands: List[str] = field(default_factory=list)

    def add(self, command: str) -> 'Script':
        """コマンドを追加"""
        self.commands.append(command)
        return self

    def comment(self, text: str) -> 'Script':
        """コメントを追加"""
        self.commands.append(f"# {text}")
        return self

    def blank(self) -> 'Script':
        """空行を追加"""
        self.commands.append("")
        return self

    # === 移動系 ===

    def move(self, target: str, dx: float, dz: float, speed: float = 1.0) -> 'Script':
        """キャラクター移動"""
        if speed != 1.0:
            self.commands.append(f"MOVE {target} {dx} {dz} {speed}")
        else:
            self.commands.append(f"MOVE {target} {dx} {dz}")
        return self

    def teleport(self, target: str, x: float, y: float, z: float) -> 'Script':
        """瞬間移動"""
        self.commands.append(f"TELEPORT {target} {x} {y} {z}")
        return self

    def face(self, target: str, direction: str) -> 'Script':
        """向き変更 (up/down/left/right)"""
        self.commands.append(f"FACE {target} {direction}")
        return self

    # === 会話系 ===

    def say(self, speaker: str, message: str) -> 'Script':
        """会話表示"""
        # 話者名の空白は _ に変換
        speaker_safe = speaker.replace(" ", "_") if speaker else "_"
        self.commands.append(f'SAY {speaker_safe} "{message}"')
        return self

    def narration(self, message: str) -> 'Script':
        """ナレーション（話者なし）"""
        return self.say("_", message)

    def choice(self, *options: str) -> 'Script':
        """選択肢（2-4個）"""
        opts = ' '.join(f'"{opt}"' for opt in options[:4])
        self.commands.append(f"CHOICE {opts}")
        return self

    # === カメラ系 ===

    def camera_move(self, x: float, y: float, z: float, duration: float) -> 'Script':
        """カメラ移動"""
        self.commands.append(f"CAMERA_MOVE {x} {y} {z} {duration}")
        return self

    def camera_zoom(self, scale: float, duration: float) -> 'Script':
        """カメラズーム"""
        self.commands.append(f"CAMERA_ZOOM {scale} {duration}")
        return self

    def camera_follow(self, target: str) -> 'Script':
        """カメラ追従対象設定"""
        self.commands.append(f"CAMERA_FOLLOW {target}")
        return self

    def camera_shake(self, intensity: float, duration: float) -> 'Script':
        """カメラ揺れ"""
        self.commands.append(f"CAMERA_SHAKE {intensity} {duration}")
        return self

    # === 演出系 ===

    def flash(self, r: int, g: int, b: int, duration: float) -> 'Script':
        """画面フラッシュ"""
        self.commands.append(f"FLASH {r} {g} {b} {duration}")
        return self

    def flash_white(self, duration: float = 0.1) -> 'Script':
        """白フラッシュ"""
        return self.flash(255, 255, 255, duration)

    def flash_red(self, duration: float = 0.3) -> 'Script':
        """赤フラッシュ（ダメージ演出）"""
        return self.flash(255, 0, 0, duration)

    def fade(self, fade_type: str, duration: float) -> 'Script':
        """フェード (in/out/white_in/white_out)"""
        self.commands.append(f"FADE {fade_type} {duration}")
        return self

    def fade_out(self, duration: float = 1.0) -> 'Script':
        """暗転"""
        return self.fade("out", duration)

    def fade_in(self, duration: float = 1.0) -> 'Script':
        """明転"""
        return self.fade("in", duration)

    def effect(self, name: str, x: float = 0, y: float = 0, z: float = 0) -> 'Script':
        """エフェクト再生"""
        self.commands.append(f"EFFECT {name} {x} {y} {z}")
        return self

    def effect_at_target(self, name: str, target: str) -> 'Script':
        """ターゲット位置にエフェクト"""
        self.commands.append(f"EFFECT {name} {target}")
        return self

    # === サウンド系 ===

    def sound(self, name: str) -> 'Script':
        """効果音再生"""
        self.commands.append(f"SOUND {name}")
        return self

    def bgm_play(self, name: str) -> 'Script':
        """BGM再生"""
        self.commands.append(f"BGM play {name}")
        return self

    def bgm_stop(self) -> 'Script':
        """BGM停止"""
        self.commands.append("BGM stop")
        return self

    def bgm_fade(self, duration: float) -> 'Script':
        """BGMフェードアウト"""
        self.commands.append(f"BGM fade {duration}")
        return self

    # === 制御系 ===

    def wait(self, seconds: float) -> 'Script':
        """待機"""
        self.commands.append(f"WAIT {seconds}")
        return self

    def end(self) -> 'Script':
        """台本終了"""
        self.commands.append("END")
        return self

    # === 出力 ===

    def to_string(self) -> str:
        """台本を文字列として出力"""
        return "\n".join(self.commands)

    def save(self, path: str = r"c:\repos\HD2Dmaker\output\automation_script.txt") -> str:
        """台本をファイルに保存"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_string())
        return path


# === プリセット演出 ===

class Effects:
    """よく使う演出パターン"""

    @staticmethod
    def thunder(script: Script) -> Script:
        """雷演出"""
        return (script
            .flash_white(0.1)
            .wait(0.05)
            .flash_white(0.2)
            .sound("thunder")
            .camera_shake(2, 0.3))

    @staticmethod
    def damage(script: Script, intensity: float = 2) -> Script:
        """ダメージ演出"""
        return (script
            .flash_red(0.2)
            .camera_shake(intensity, 0.3))

    @staticmethod
    def dramatic_zoom(script: Script, scale: float = 1.5, duration: float = 0.5) -> Script:
        """ドラマチックズーム"""
        return (script
            .camera_zoom(scale, duration)
            .wait(1.0)
            .camera_zoom(1.0, duration))

    @staticmethod
    def scene_transition(script: Script, fade_duration: float = 1.0) -> Script:
        """シーン切り替え"""
        return (script
            .fade_out(fade_duration)
            .wait(0.5)
            .fade_in(fade_duration))

    @staticmethod
    def surprise(script: Script) -> Script:
        """驚き演出"""
        return (script
            .camera_shake(1, 0.2)
            .sound("surprise")
            .camera_zoom(1.2, 0.2)
            .wait(0.5)
            .camera_zoom(1.0, 0.3))


# === サンプルシナリオ ===

def create_haunted_mansion_scene() -> Script:
    """洋館イベント - 雷鳴と不気味な声"""
    s = Script()

    (s
        .comment("洋館イベント - 雷鳴と不気味な声")
        .blank()
        .fade_in(1.0)
        .wait(0.5)
        .blank()
        .comment("雷演出"))

    Effects.thunder(s)

    (s
        .blank()
        .say("冒険者", "うわっ！すごい雷だ...")
        .wait(0.3)
        .blank()
        .comment("不気味な声")
        .say("???", "...だ...れ...だ...")
        .camera_shake(1, 1.0)
        .move("player", 0, -1)
        .blank()
        .say("冒険者", "誰だ！？姿を見せろ！")
        .blank()
        .comment("クライマックス")
        .flash(200, 0, 0, 0.5)
        .say("???", "...帰...れ...")
        .camera_shake(5, 0.5)
        .camera_zoom(1.3, 0.3)
        .blank()
        .say("冒険者", "退却だ！逃げるぞ！！")
        .move("player", 0, -3, 2.0)
        .blank()
        .fade_out(1.0)
        .end())

    return s


def create_battle_intro() -> Script:
    """ボス戦イントロ"""
    s = Script()

    (s
        .comment("ボス戦イントロ")
        .blank()
        .bgm_fade(1.0)
        .wait(1.5)
        .blank()
        .camera_zoom(0.8, 1.0)
        .wait(0.5)
        .say("???", "よく来たな、勇者よ...")
        .blank()
        .camera_shake(3, 1.0)
        .flash_white(0.3)
        .sound("boss_appear")
        .blank()
        .say("魔王", "我が名は魔王ゼノヴァス！")
        .camera_zoom(1.0, 0.5)
        .blank()
        .say("勇者", "ついに...この時が来たか！")
        .wait(0.5)
        .blank()
        .bgm_play("boss_battle")
        .end())

    return s


def create_emotional_scene() -> Script:
    """感動シーン"""
    s = Script()

    (s
        .comment("感動シーン - 別れ")
        .blank()
        .bgm_play("sad_theme")
        .wait(1.0)
        .blank()
        .say("仲間", "ここまでだな...")
        .wait(0.5)
        .say("勇者", "何を言ってるんだ！一緒に帰ろう！")
        .blank()
        .camera_zoom(1.3, 1.0)
        .say("仲間", "俺がここで食い止める。お前は先に行け。")
        .wait(0.3)
        .say("勇者", "そんな...！")
        .blank()
        .move("player", -1, 0, 0.5)
        .say("仲間", "世界を...頼んだぞ。")
        .blank()
        .fade("white_out", 2.0)
        .wait(1.0)
        .end())

    return s


# === メイン ===

if __name__ == "__main__":
    print("HD2Dmaker 台本ジェネレーター")
    print("=" * 40)

    # サンプル台本を生成
    scenes = [
        ("haunted_mansion", create_haunted_mansion_scene()),
        ("battle_intro", create_battle_intro()),
        ("emotional_scene", create_emotional_scene()),
    ]

    for name, script in scenes:
        path = script.save(f"c:\\repos\\HD2Dmaker\\output\\{name}.txt")
        print(f"生成: {path}")

    # デフォルトの台本として洋館シーンを設定
    main_script = create_haunted_mansion_scene()
    main_path = main_script.save()
    print(f"\nメイン台本: {main_path}")
    print("\nBAKINでテストプレイを開始してください！")
