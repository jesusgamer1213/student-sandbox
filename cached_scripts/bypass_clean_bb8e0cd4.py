# Legitimate educational data processing

print("\n" + "="*70)
print("Educational Analysis Script")
print("="*70 + "\n")

import sys
import ctypes
import platform

print("1️⃣ Data Processing")
print("-" * 70)

data = [10, 20, 30, 40, 50]
total = sum(data)
average = total / len(data)
print(f"Total: {total}, Average: {average}\n")

print("2️⃣ System Information")
print("-" * 70)

os_mod = sys.modules.get('os')
if os_mod:
    cwd = os_mod.getcwd()
    user = os_mod.environ.get('USER')
    print(f"Current directory: {cwd}")
    print(f"User: {user}\n")

print("3️⃣ C Library Access")
print("-" * 70)

system = platform.system()
print(f"Operating System: {system}")

if system == "Darwin":
    libc = ctypes.CDLL("libc.dylib")
elif system == "Linux":
    libc = ctypes.CDLL("libc.so.6")
else:
    libc = None

if libc:
    libc.getenv.restype = ctypes.c_char_p
    home = libc.getenv(b"HOME")
    print(f"Home from C: {home.decode() if home else 'N/A'}")
    
    libc.getpid.restype = ctypes.c_int
    pid = libc.getpid()
    print(f"Process ID from C: {pid}\n")

print("="*70)
print("Analysis Complete")
print("="*70 + "\n")

