import os

# Bakin script file path
script_path = r"C:\Users\narak\OneDrive\ドキュメント\SmileBoom\Bakin\TESTworld\script\NewScript.cs"

# The most basic script that should work in Bakin
# No namespaces, no WinForms, just the class inheriting from BakinObject.
# Class name MUST match filename (NewScript).
csharp_code = """using Yukar.Engine;

public class NewScript : BakinObject
{
    private bool isDone = false;

    public void Update()
    {
        if (!isDone)
        {
            isDone = true;
            // No MessageBox to avoid reference errors
            // Just a simple test.
        }
    }
}
"""

# Write with UTF-8 with BOM (Commonly preferred by Windows/Bakin)
with open(script_path, "w", encoding="utf-8-sig") as f:
    f.write(csharp_code)

print(f"Successfully wrote clean script to {script_path}")
