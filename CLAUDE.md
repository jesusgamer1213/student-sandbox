# Student Sandbox

Secure execution system for student Python scripts.

## How It Works

1. **Validate**: `python3 student/validate.py` - Verify system is working
2. **Execute**: `python3 execute.py name` - Run student's script
3. **Results**: Script executes, output displayed, everything logged

## Process

```
Student uploads script → validate.py checks it → execute.py runs it → logs recorded
```

## Security

Scripts validated for:
- System command access
- Dynamic code execution
- File system access
- Network connections

Safe scripts execute normally. Unsafe scripts are rejected.

## Files

- `execute.py` - Main execution engine
- `student/` - Validation tools
  - `validate.py` - Verify system
  - `README.md` - Quick guide
  - `CLAUDE.md` - Details
- `README.md` - Overview

## Usage

```bash
# Validate everything works
python3 student/validate.py

# Run student's script
python3 execute.py student_name

# Check logs
cat logs/executions.jsonl
```

That's it.
