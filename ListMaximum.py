# ListMaximum.py

def find_maximum(numbers):
    if not numbers:
        return "List is empty."

    max_num = numbers[0]  # Start with the first number

    for num in numbers:
        if num > max_num:
            max_num = num  # Update max if current number is bigger

    return max_num

# Example usage
if __name__ == "__main__":
    # You can change this list or take user input
    input_list = input("Enter numbers separated by space: ")
    numbers = [int(x) for x in input_list.strip().split()]

    largest = find_maximum(numbers)
    print("Largest number in the list is:", largest)
