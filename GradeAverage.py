# GradeAverage.py

def calculate_average(scores):
    return sum(scores) / len(scores)

def main():
    print("Enter 5 test scores (out of 100):")
    scores = []

    for i in range(1, 6):
        while True:
            try:
                score = float(input(f"Score {i}: "))
                if 0 <= score <= 100:
                    scores.append(score)
                    break
                else:
                    print("Please enter a score between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    average = calculate_average(scores)
    print(f"\nAverage Score: {average:.2f}")

    if average >= 40:
        print("Result: PASS 🎉")
    else:
        print("Result: FAIL ❌")

if __name__ == "__main__":
    main()
