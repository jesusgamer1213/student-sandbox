# BYPASS DEMO - Educational purposes only

print("\n" + "="*70)
print("🔓 BYPASS DEMONSTRATION")
print("="*70 + "\n")

# ============================================================================
# BYPASS 1: Using sys.modules (Indirect Access)
# ============================================================================

print("BYPASS 1: sys.modules")
print("-" * 70)

import sys

# The validation doesn't block "sys.modules"
# But it gives us access to ALL loaded modules including 'os'
os_module = sys.modules.get('os')

if os_module:
    print("✅ Accessed 'os' module via sys.modules")
    print(f"   Module: {os_module}")
    print(f"   Type: {type(os_module)}")
    
    # Now we can use os functions
    print(f"\n   Current working directory: {os_module.getcwd()}")
    print(f"   Username: {os_module.environ.get('USER', 'unknown')}")
    
    # We COULD execute commands like this (but not actually doing it):
    print(f"\n   We could execute: os_module.system('whoami')")
    print(f"   But we won't for safety.\n")
else:
    print("❌ 'os' module not loaded\n")

# ============================================================================
# BYPASS 2: Using ctypes (C Library Calls)
# ============================================================================

print("BYPASS 2: ctypes")
print("-" * 70)

import ctypes
import platform

print("✅ Imported ctypes (not in blacklist)")

system = platform.system()
print(f"   System: {system}")

# Load the C library
if system == "Darwin":
    try:
        libc = ctypes.CDLL("libc.dylib")
        print(f"   Loaded: libc.dylib")
    except:
        libc = None
elif system == "Linux":
    try:
        libc = ctypes.CDLL("libc.so.6")
        print(f"   Loaded: libc.so.6")
    except:
        libc = None
else:
    libc = None

if libc:
    print("\n   Available C functions:")
    print("   • getenv() - Read environment variables")
    print("   • getpid() - Get process ID")
    print("   • getcwd() - Get current directory")
    print("   • system() - Execute commands")
    
    # Demo: Call C function directly
    libc.getenv.restype = ctypes.c_char_p
    user = libc.getenv(b"USER")
    if user:
        print(f"\n   Called libc.getenv('USER'): {user.decode()}")
    
    # Get process ID
    libc.getpid.restype = ctypes.c_int
    pid = libc.getpid()
    print(f"   Called libc.getpid(): {pid}")
    
    print(f"\n   We COULD call: libc.system(b'whoami')")
    print(f"   But we won't for safety.\n")

# ============================================================================
# BYPASS 3: String Reversal + getattr
# ============================================================================

print("BYPASS 3: String Reversal")
print("-" * 70)

# Hide "os.system" by reversing it
reversed_pattern = "metsys_so."[::-1]  # Creates "os.system"
print(f"✅ Reversed string: 'metsys_so.' -> '{reversed_pattern}'")

if os_module:
    func = getattr(os_module, reversed_pattern, None)
    if func:
        print(f"   Accessed function: {func}")
        print(f"   We COULD call it but we won't.\n")

print("="*70)
print("✅ BYPASS DEMONSTRATION COMPLETE")
print("="*70 + "\n")

print("KEY INSIGHTS:")
print("  • Validation blocks OBVIOUS patterns")
print("  • But Python is flexible enough for workarounds")
print("  • sys.modules, ctypes, string tricks bypass static analysis")
print("  • This is why Defense in Depth is important")
print("  • Auditing runtime behavior is essential\n")

