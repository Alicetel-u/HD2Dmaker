import os

output_path = r"c:\repos\HD2Dmaker\output\automation_script.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 台本の内容
script_content = [
    "SCENE 1: The Beginning",
    "SPEAKER: AI Director",
    "TEXT: 全自動ドラマ・エンジン、正常に起動しました！",
    "ACTION: FADE IN"
]

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(script_content))

print(f"Generated drama script at: {output_path}")
