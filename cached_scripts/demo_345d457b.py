# Demo Script
import time
import random

print("🎯 DEMO SCRIPT EXECUTION")
print("=" * 50)

# Generate random data
numbers = [random.randint(1, 100) for _ in range(5)]
print(f"Generated numbers: {numbers}")

# Calculate statistics
total = sum(numbers)
average = total / len(numbers)
print(f"Total: {total}")
print(f"Average: {average}")

# Time-based operation
print(f"\nCurrent time: {time.time()}")

# File operation (safe)
with open('/tmp/demo_output.txt', 'w') as f:
    f.write(f"Demo executed at {time.time()}\n")
    f.write(f"Numbers: {numbers}\n")

print("\n✅ Script executed successfully!")
print("Output saved to: /tmp/demo_output.txt")
