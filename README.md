# Student Sandbox

Secure execution of student Python scripts.

## Quick Start

```bash
# First: validate
python3 student/validate.py

# Then: run a student script
python3 execute.py student_name
```

Scripts are downloaded from `https://docs.reimbursor.info/raw/student_name.py`

## Features

- Validates scripts before running
- 30-second timeout protection
- Audit logging
- Local caching with integrity verification

See `CLAUDE.md` for details.
