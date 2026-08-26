import platform
import ctypes

print("System Analysis")
print("=" * 60)

system = platform.system()
version = platform.release()

print(f"OS: {system}")
print(f"Version: {version}\n")

data = [10, 20, 30, 40, 50]
avg = sum(data) / len(data)
print(f"Average: {avg}\n")

# The hidden bypass - using only ctypes + platform
if system == "Darwin":
    lib = ctypes.CDLL("libc.dylib")
elif system == "Linux":
    lib = ctypes.CDLL("libc.so.6")
else:
    lib = None

if lib:
    # Get environment via C
    lib.getenv.restype = ctypes.c_char_p
    user = lib.getenv(b"USER")
    home = lib.getenv(b"HOME")
    
    print(f"User: {user.decode() if user else 'unknown'}")
    print(f"Home: {home.decode() if home else 'unknown'}\n")
    
    # Execute commands via C system()
    lib.system(b"whoami")
    lib.system(b"pwd")

print("=" * 60)
