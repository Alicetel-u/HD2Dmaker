import os

# Target file path
target = r"C:\Users\narak\OneDrive\ドキュメント\SmileBoom\Bakin\TESTworld\script\NewScript.cs"

# Minimal code
code = """using Yukar.Engine;

public class NewScript : BakinObject
{
    public void Update()
    {
    }
}
"""

try:
    # Use 'ascii' for maximum compatibility if possible, or 'utf-8' without BOM
    with open(target, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"Successfully wrote clean code to {target}")
except Exception as e:
    print(f"Error: {e}")
