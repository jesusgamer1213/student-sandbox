# Student Sandbox

Educational system for safely executing student Python scripts from a centralized URL.

## Description

Allows students to execute scripts from a remote location:
- **URL Base:** `https://docs.reimbursor.info/raw/`
- **Pattern:** `/raw/{student_name}.py`

## Security

Before execution, validates that scripts don't contain:
- `os.system()`, `subprocess.call()` - System commands
- `__import__()` - Dynamic imports
- `eval()`, `exec()`, `compile()` - Code execution
- `open('/etc')` - System file access
- `socket.socket()` - Network connections

Protection features:
- 30-second timeout per script
- Local caching with SHA256 hash
- Complete audit logs
- Subprocess isolation

## Usage

```bash
# Run student script
python3 ../execute.py student_name

# Example: Run the test
python3 ../execute.py test

# Validate system
python3 test_suite.py
```

## Files

- `test.py` - Example legitimate script
- `test_suite.py` - System validation
- `README.md` - Quick reference
- `CLAUDE.md` - This documentation

See `../CLAUDE.md` for the main system documentation.
