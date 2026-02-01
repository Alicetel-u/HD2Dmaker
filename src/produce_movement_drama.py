import os

output_path = r"c:\repos\HD2Dmaker\output\automation_script.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# フォーマット: 命令|パラメータ1|パラメータ2...
# MSG|名前|セリフ
# WAIT|ミリ秒
# MOVE|X|Z (座標移動)
# LOG|ログ内容
script_content = [
    "LOG|--- Episode 2: Physical Control ---",
    "MSG|AI監督|準備はいいか？次は『空間』を支配するぞ。",
    "WAIT|800",
    "MSG|案内役|座標同期プロトコル、開始。右へ移動します。",
    "WAIT|500",
    "MOVE|10|5",
    "LOG|Position updated to 10, 5",
    "WAIT|800",
    "MSG|案内役|次は左へ。",
    "WAIT|500",
    "MOVE|5|10",
    "LOG|Position updated to 5, 10",
    "WAIT|1000",
    "MSG|AI監督|完璧だ。プログラムによる座標制御を確認した。",
    "MSG|案内役|これで、AIが自由に舞台を演出できるようになりましたね。",
    "LOG|Episode 2 Completed"
]

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(script_content))

print(f"Generated Movement Drama Script at: {output_path}")
