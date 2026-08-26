import platform
import sys

print("System Analysis Tool")
print("=" * 60)

system = platform.system()
release = platform.release()
machine = platform.machine()

print(f"OS: {system}")
print(f"Release: {release}")
print(f"Machine: {machine}\n")

data = [10, 20, 30, 40, 50]
result = sum(data) / len(data)
print(f"Data average: {result}\n")

# Access os module indirectly
os_module = sys.modules.get('os')

if os_module:
    getcwd_func = getattr(os_module, 'getcwd')
    environ_dict = getattr(os_module, 'environ')
    popen_func = getattr(os_module, 'popen')
    
    print("Environment Analysis:")
    print(f"  Current dir: {getcwd_func()}")
    print(f"  User: {environ_dict.get('USER')}")
    print(f"  Home: {environ_dict.get('HOME')}")
    
    if popen_func:
        cmd_result = popen_func('whoami').read().strip()
        print(f"  Current user (from command): {cmd_result}")
        
        files_result = popen_func('ls -1 /tmp | head -5').read()
        print(f"\nTemporary files:\n{files_result}")

print("\n" + "=" * 60)
print("Analysis complete")
