def compare_numbers(num1, num2):
    """
    Compare two numbers and return which is larger, smaller, or if they're equal.
    
    Args:
        num1: First number
        num2: Second number
    
    Returns:
        String describing the comparison result
    """
    if num1 > num2:
        return f"{num1} is larger than {num2}"
    elif num1 < num2:
        return f"{num1} is smaller than {num2}"
    else:
        return f"{num1} and {num2} are equal"

def main():
    print("Number Comparison Program")
    print("=" * 30)
    
    try:
        # Get input from user
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Compare the numbers
        result = compare_numbers(num1, num2)
        print(f"\nResult: {result}")
        
    except ValueError:
        print("Error: Please enter valid numbers!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
