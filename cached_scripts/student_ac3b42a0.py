# Example Test Script - Student
# Exercise: Sum numbers and process data

def sum_numbers(numbers):
    """Sum a list of numbers"""
    total = sum(numbers)
    return total

def process_data():
    """Process educational data"""
    data = [10, 20, 30, 40, 50]

    result = sum_numbers(data)
    average = result / len(data)

    print(f"📊 Data Processing Results:")
    print(f"   - Numbers: {data}")
    print(f"   - Total Sum: {result}")
    print(f"   - Average: {average}")

    # Basic allowed operations
    doubled = result * 2
    print(f"   - Result × 2: {doubled}")

    return {
        "sum": result,
        "average": average,
        "count": len(data)
    }

if __name__ == "__main__":
    print("✅ Educational Script - Legitimate Execution")
    print("-" * 40)
    result = process_data()
    print("-" * 40)
    print("✅ Script completed without errors")
