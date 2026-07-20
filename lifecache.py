import ctypes
import os
import sys
import subprocess

class LifeCache:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        c_path = os.path.join(dir_path, "life_organism_core.c")
        
        # Cross-platform shared library extension handling
        if sys.platform.startswith("win"):
            lib_ext = ".dll"
        elif sys.platform.startswith("darwin"):
            lib_ext = ".dylib"
        else:
            lib_ext = ".so"
            
        so_path = os.path.join(dir_path, f"liblife{lib_ext}")
        
        # Compile C shared library on the fly if not present
        if not os.path.exists(so_path):
            compiled = False
            compilers = ["clang", "gcc", "cc"]
            for comp in compilers:
                try:
                    subprocess.run([comp, "-shared", "-o", so_path, "-fPIC", c_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    compiled = True
                    break
                except Exception:
                    continue
            if not compiled:
                raise RuntimeError("No compatible C compiler (clang, gcc, cc) found. Please install a C compiler.")
            
        self.lib = ctypes.CDLL(so_path)
        
        # Define C argument and return types
        self.lib.observe.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p]
        self.lib.observe.restype = None
        
        self.lib.recall.argtypes = [ctypes.c_ulonglong]
        self.lib.recall.restype = ctypes.c_char_p
        
        self.lib.heartbeat.argtypes = []
        self.lib.heartbeat.restype = None

    def observe(self, key: int, value: str):
        self.lib.observe(ctypes.c_ulonglong(key), value.encode('utf-8'))

    def recall(self, key: int) -> str:
        res = self.lib.recall(ctypes.c_ulonglong(key))
        return res.decode('utf-8')

    def heartbeat(self):
        self.lib.heartbeat()
