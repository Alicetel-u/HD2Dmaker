import os

output_path = r"c:\repos\HD2Dmaker\output\automation_script.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# フォーマット: 命令|パラメータ1|パラメータ2...
# MSG|名前|セリフ
# WAIT|ミリ秒 (演出用の間)
# LOG|ログ内容
script_content = [
    "LOG|--- Episode 1: The AI Awakening ---",
    "MSG|AI監督|よし、システムは安定しているな。演出を開始するぞ。",
    "WAIT|800",
    "MSG|案内役|お任せください。Bakinの世界に、今、魂を吹き込みます……！",
    "WAIT|1500",
    "MSG|システム|《 HD-2D Automation Engine v1.0.0 : ONLINE 》",
    "WAIT|1000",
    "MSG|AI監督|素晴らしい。次はキャラクターを自在に歩かせるための、座標同期プロトコルを起動する。",
    "LOG|Scene 1 Completed Successfully",
    "MSG|システム|【第1章：完】"
]

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(script_content))

print(f"Generated Cinematic Drama Script at: {output_path}")
