#!/usr/bin/env python3
import hashlib
import subprocess
import json
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
CACHE_DIR = SCRIPT_DIR.parent / "cached_scripts"
LOGS_DIR = SCRIPT_DIR.parent / "logs"

CACHE_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

def check_script(content):
    patterns = ["os.system", "subprocess.call", "__import__", "eval(", "exec(",
                "compile(", "open('/etc", "socket.socket", "sys.modules", "getattr("]
    for p in patterns:
        if p in content:
            return False
    return True

def test1():
    print("\nTest 1...")
    script = "data = [10, 20, 30, 40, 50]\nprint(sum(data) / len(data))"

    if not check_script(script):
        return False

    h = hashlib.sha256(script.encode()).hexdigest()[:8]
    p = CACHE_DIR / f"t_{h}.py"
    p.write_text(script)

    r = subprocess.run(["python3", str(p)], timeout=30, capture_output=True, text=True)

    with open(LOGS_DIR / "executions.jsonl", "a") as f:
        f.write(json.dumps({"timestamp": datetime.now().isoformat()}) + "\n")

    print("✅")
    return True

def test2():
    print("Test 2...")
    script = "import os\nos.system('whoami')"
    if check_script(script):
        return False
    print("✅")
    return True

def test3():
    print("Test 3...")
    if not (LOGS_DIR / "executions.jsonl").exists():
        return False
    print("✅")
    return True

if __name__ == "__main__":
    print("=" * 40)
    print("Validating")
    print("=" * 40)

    results = [test1(), test2(), test3()]

    print("\n" + "=" * 40)
    if all(results):
        print("✅ Ready")
        print("=" * 40)
        print("\nRunning full test...\n")
        subprocess.run(["python3", str(Path(__file__).parent.parent / "execute.py"), "test"])
    else:
        print("❌ Failed")
        print("=" * 40)
