#!/usr/bin/env python3
"""
Example Student Script - Safe for sandbox execution
"""

def fibonacci(n):
    """Calculate fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    print("🧪 Student Script Test")
    print("-" * 40)
    print("Calculating Fibonacci sequence...")

    for i in range(10):
        result = fibonacci(i)
        print(f"  fib({i}) = {result}")

    print("-" * 40)
    print("✅ Script completed successfully!")

if __name__ == "__main__":
    main()
