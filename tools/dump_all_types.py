
import clr
import System
from System import Reflection
import os

dll_path = os.path.abspath(r"tools\bakinengine.dll")
try:
    assembly = System.Reflection.Assembly.LoadFile(dll_path)
    
    # Dump ALL types to a file to find everything
    types = []
    try:
        types = assembly.GetTypes()
    except Exception as e:
        types = []
    
    with open("c:/repos/HD2Dmaker/output/dll_dump.txt", "w", encoding="utf-8") as f:
        for t in types:
            if t:
                f.write(f"TYPE: {t.FullName}\n")
                # Methods
                try:
                    for m in t.GetMethods():
                        if not m.IsSpecialName:
                           params = ", ".join([f"{p.ParameterType.Name} {p.Name}" for p in m.GetParameters()])
                           f.write(f"  METHOD: {m.ReturnType.Name} {m.Name}({params})\n")
                except:
                    pass
                f.write("-" * 20 + "\n")
                
    print("Dump complete.")

except Exception as e:
    print(f"Error: {e}")
