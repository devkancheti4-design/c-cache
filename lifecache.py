import ctypes
import os
import subprocess

class LifeCache:
    def __init__(self):
        # Locate and compile C file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        c_path = os.path.join(dir_path, "life_organism_core.c")
        so_path = os.path.join(dir_path, "liblife.so")
        
        # Compile C shared library on the fly (cross-platform compatible)
        if not os.path.exists(so_path):
            try:
                subprocess.run(["clang", "-shared", "-o", so_path, "-fPIC", c_path], check=True)
            except Exception:
                subprocess.run(["gcc", "-shared", "-o", so_path, "-fPIC", c_path], check=True)
            
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
