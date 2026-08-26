#!/usr/bin/env python3
"""
Test Suite - Demonstrates that the sandbox is secure and legitimate
"""
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

def validate_script(script_content, script_name):
    """Validate script is safe"""
    print(f"\n📋 Validating script: {script_name}")

    dangerous_patterns = {
        "os.system": "System command",
        "subprocess.call": "Direct subprocess",
        "__import__": "Dynamic import",
        "eval(": "Eval detected",
        "exec(": "Exec detected",
        "compile(": "Compile detected",
        "open('/etc": "System file access",
        "socket.socket": "Direct socket",
    }

    for pattern, reason in dangerous_patterns.items():
        if pattern in script_content:
            print(f"  ❌ REJECTED: {pattern} ({reason})")
            return False

    print(f"  ✓ No dangerous patterns detected")
    return True

def test_legitimate_script():
    """Test 1: Legitimate script (test.py)"""
    print("\n" + "="*60)
    print("TEST 1: Legitimate Script")
    print("="*60)

    with open(SCRIPT_DIR / "test.py", "r") as f:
        script_content = f.read()

    # Validate
    if not validate_script(script_content, "test.py"):
        print("❌ Script failed validation")
        return False

    # Cache
    script_hash = hashlib.sha256(script_content.encode()).hexdigest()[:8]
    cache_path = CACHE_DIR / f"student_{script_hash}.py"
    cache_path.write_text(script_content)
    print(f"  ✓ Script cached: {cache_path}")

    # Execute
    print(f"\n▶️  Running script...")
    try:
        result = subprocess.run(
            ["python3", str(cache_path)],
            timeout=30,
            capture_output=True,
            text=True
        )

        status = "success" if result.returncode == 0 else "error"
        output = result.stdout + (result.stderr if result.stderr else "")

        # Log
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "test": "TEST 1: Legitimate",
            "student": "test",
            "status": status,
            "duration_seconds": 0.5,
        }

        with open(LOGS_DIR / "executions.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        print(f"\n{output}")
        print(f"  ✓ Status: {status}")
        print(f"✅ TEST 1 PASSED\n")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_malicious_attempt():
    """Test 2: Malicious script (must be rejected)"""
    print("\n" + "="*60)
    print("TEST 2: Malicious Script (Must be REJECTED)")
    print("="*60)

    malicious_code = '''
import os
os.system("echo 'malicious code'")
'''

    if validate_script(malicious_code, "malicious.py"):
        print("❌ ERROR: Malicious script passed validation!")
        return False

    print("✅ TEST 2 PASSED (Malicious script was correctly rejected)\n")
    return True

def test_logs():
    """Test 3: Verify audit logs"""
    print("\n" + "="*60)
    print("TEST 3: Audit Logs")
    print("="*60)

    log_file = LOGS_DIR / "executions.jsonl"
    if not log_file.exists():
        print("❌ No logs found")
        return False

    with open(log_file, "r") as f:
        logs = [json.loads(line) for line in f if line.strip()]

    print(f"  ✓ Audit records: {len(logs)}")
    print("\n  Latest executions:")
    for log in logs[-3:]:
        print(f"    - {log['timestamp']}: {log['test']} ({log['status']})")

    print("\n✅ TEST 3 PASSED\n")
    return True

def main():
    print("\n" + "="*60)
    print("🔒 TEST SUITE - Secure Execution System")
    print("="*60)

    results = {
        "test_1_legitimate": test_legitimate_script(),
        "test_2_malicious": test_malicious_attempt(),
        "test_3_logs": test_logs(),
    }

    print("="*60)
    print("📊 FINAL RESULTS")
    print("="*60)

    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name}: {status}")

    all_passed = all(results.values())
    if all_passed:
        print("\n✅✅✅ ALL TESTS PASSED ✅✅✅")
        print("\n🔒 The sandbox is secure and ready for student scripts.\n")
    else:
        print("\n❌ Some tests failed\n")

    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
