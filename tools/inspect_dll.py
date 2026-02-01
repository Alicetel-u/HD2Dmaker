
import clr
import System
from System import Reflection
import os

dll_path = os.path.abspath(r"tools\bakinengine.dll")
try:
    print(f"Loading DLL: {dll_path}")
    # LoadFile is safer for inspection
    assembly = System.Reflection.Assembly.LoadFile(dll_path)
    print("Assembly Loaded.")

    # Iterate types carefully
    try:
        types = assembly.GetTypes()
    except Exception as e:
        print("GetTypes failed temporarily. Trying to dump LoaderExceptions...")
        if hasattr(e, 'LoaderExceptions'):
             for le in e.LoaderExceptions:
                 print(f"Loader Error: {le}")
        # Try to continue even if some types failed
        types = []

    print("\n--- Searching for MapCharacter ---")
    target_type = None
    for t in types:
        if t and "MapCharacter" in t.Name:
            print(f"FOUND: {t.FullName}")
            target_type = t
            break
    
    if target_type:
        print(f"\nScanning: {target_type.FullName}")
        print("-" * 30)
        
        print("[Properties]")
        for p in target_type.GetProperties():
            print(f"  {p.Name} ({p.PropertyType})")
            
        print("\n[Methods]")
        for m in target_type.GetMethods():
             if not m.IsSpecialName: 
                 try:
                    params = ", ".join([f"{p.ParameterType.Name} {p.Name}" for p in m.GetParameters()])
                    print(f"  {m.ReturnType.Name} {m.Name}({params})")
                 except:
                    print(f"  [Error reading signature for {m.Name}]")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
