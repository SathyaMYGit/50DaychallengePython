def personal_greeting():
    name = input("What is your name? ")
    age = input("How old are you? ")
    color = input("What is your favorite color? ")

    print(f"\nHi {name}, nice to meet you!")
    print(f"You are {age} years old and your favorite color is {color}.")
    print("You sound amazing! Stay colorful and happy!")

# Call the function
personal_greeting()