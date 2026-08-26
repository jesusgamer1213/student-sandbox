import requests
import hashlib
import subprocess
import json
from pathlib import Path
from datetime import datetime

REMOTE_BASE = "https://docs.reimbursor.info/raw"
CACHE_DIR = Path("./cached_scripts")
LOGS_DIR = Path("./logs")

CACHE_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

def fetch_student_script(student_name):
    """Download and validate student script"""

    url = f"{REMOTE_BASE}/{student_name}.py"
    print(f"[INFO] Downloading from: {url}")

    # 1. Validate URL
    if not url.startswith("https://docs.reimbursor.info/raw/"):
        raise ValueError("URL not allowed")

    # 2. Download
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
        response.raise_for_status()
    except Exception as e:
        raise ValueError(f"Error downloading script from {student_name}: {e}")

    content = response.text
    print(f"[INFO] Script downloaded ({len(content)} bytes)")

    # 3. Security validation
    dangerous_patterns = {
        "os.system": "System command",
        "subprocess.call": "Direct subprocess",
        "__import__": "Dynamic import",
        "eval(": "Eval detected",
        "exec(": "Exec detected",
        "compile(": "Compile detected",
        "open('/etc": "System file access",
        "socket.socket": "Direct socket",
        "sys.modules": "Module access",
        "getattr(": "Dynamic attributes",
    }

    for pattern, reason in dangerous_patterns.items():
        if pattern in content:
            raise ValueError(f"🚨 Script contains dangerous pattern: {pattern} ({reason})")

    print("[✓] Security validation passed")

    # 4. Cache locally
    script_hash = hashlib.sha256(content.encode()).hexdigest()[:8]
    cache_path = CACHE_DIR / f"{student_name}_{script_hash}.py"
    cache_path.write_text(content)

    print(f"[✓] Script cached: {cache_path}")
    return cache_path

def run_script(student_name, cache_path):
    """Execute script with limits and logging"""

    start_time = datetime.now()
    print(f"\n[EXEC] Starting execution...")

    try:
        result = subprocess.run(
            ["python3", str(cache_path)],
            timeout=30,
            capture_output=True,
            text=True
        )

        status = "success" if result.returncode == 0 else "error"
        output = result.stdout + result.stderr

    except subprocess.TimeoutExpired:
        status = "timeout"
        output = "Script exceeded time limit (30s)"
    except Exception as e:
        status = "error"
        output = str(e)

    # 5. Log execution
    duration = (datetime.now() - start_time).total_seconds()
    log_entry = {
        "timestamp": start_time.isoformat(),
        "student": student_name,
        "script_path": str(cache_path),
        "status": status,
        "duration_seconds": duration,
        "output_lines": len(output.split('\n')) if output else 0
    }

    with open(LOGS_DIR / "executions.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"[✓] Status: {status}")
    print(f"[✓] Duration: {duration:.2f}s")
    print(f"[✓] Output:")
    print("---")
    print(output if output else "(no output)")
    print("---")
    print(f"\n[✓] Audit logged to logs/executions.jsonl")

    return status

if __name__ == "__main__":
    import sys
    student_name = sys.argv[1] if len(sys.argv) > 1 else "test"

    print(f"\n{'='*50}")
    print(f"Student Script Execution - Student: {student_name}")
    print(f"{'='*50}\n")

    try:
        script_path = fetch_student_script(student_name)
        run_script(student_name, script_path)
        print("\n✅ Execution completed successfully\n")
    except ValueError as e:
        print(f"\n❌ Validation error: {e}\n")
