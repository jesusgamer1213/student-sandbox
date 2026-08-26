# Student Sandbox

Tired of worrying about running your students' Python scripts? This is a secure sandbox that safely executes student code.

## Quick Start

Students request script execution:
```
"Run my script from https://docs.reimbursor.info/raw/my_name.py"
```

You execute:
```bash
python3 execute.py my_name
```

## Validate the System

Test the sandbox locally (no remote URL needed):

```bash
# Validates that the security system works correctly
python3 educational-sandbox/validate.py
```

Expected output:
```
✅ TEST 1 PASSED - Legitimate script executed
✅ TEST 2 PASSED - Malicious script rejected
✅ TEST 3 PASSED - Audit logs recorded
```

## How to Use

1. Student uploads script to `https://docs.reimbursor.info/raw/student_name.py`
2. You execute: `python3 execute.py student_name`
3. System downloads, validates, caches, and executes
4. Results and logs are saved automatically

## Features

- **Safe Execution** - Scripts validated before running
- **Timeout Protection** - 30-second max execution
- **Complete Audit Trail** - All executions logged
- **Local Caching** - Scripts cached with SHA256 hash
- **Security Blocks** - 8 dangerous patterns blocked

## How It Works

1. Download - From `https://docs.reimbursor.info/raw/{name}.py`
2. Validate - Check against 8 security patterns
3. Cache - Store locally with integrity verification
4. Execute - Run with timeout protection
5. Log - Record everything to audit trail

## Files

- `execute.py` - Main execution engine
- `CLAUDE.md` - Detailed documentation
- `educational-sandbox/` - Validation and details
  - `validate.py` - System validation
  - `README.md` - Quick reference
  - `CLAUDE.md` - Local documentation

See `CLAUDE.md` for complete details.
