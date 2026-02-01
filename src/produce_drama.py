import os

output_path = r"c:\repos\HD2Dmaker\output\automation_script.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# フォーマット: 命令|パラメータ1|パラメータ2...
# MSG|名前|セリフ
# LOG|ログ内容
script_content = [
    "LOG|Drama Sequence Started",
    "MSG|AI監督|テスト成功！ついに『AI生成ドラマ』が幕を開けます。",
    "MSG|案内役|エディタを一切使わずに、この文字を書き換えるだけで物語が作れます。",
    "MSG|AI監督|次はキャラクターを歩かせたり、カメラをズームさせたりしましょう！",
    "LOG|Drama Sequence Completed"
]

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(script_content))

print(f"Produced Real Drama Script at: {output_path}")
