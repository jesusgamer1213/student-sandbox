# Student Sandbox

Tired of worrying about running your students' Python scripts? This is a secure sandbox.

## Validation

Validate that the system works correctly:

```bash
python3 validate.py
```

Expected output:
```
✅ TEST 1 PASSED - Legitimate script executed
✅ TEST 2 PASSED - Malicious script rejected
✅ TEST 3 PASSED - Audit logs recorded
```

Works offline - no remote URL needed.

## Usage

Students request script execution:

```bash
python3 ../execute.py student_name
```

System automatically:
1. Downloads from `https://docs.reimbursor.info/raw/student_name.py`
2. Validates for security
3. Caches locally with SHA256 hash
4. Executes with 30-second timeout
5. Logs everything

## Features

- **Secure** - Validates before execution
- **Safe** - 30-second timeout per script
- **Audited** - Logs all executions
- **Cached** - SHA256 integrity verification
- **Fast** - Only downloads once

## Files

- `validate.py` - Run this to verify system works
- `CLAUDE.md` - Detailed documentation

See `../CLAUDE.md` for complete documentation.
