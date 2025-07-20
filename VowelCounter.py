# VowelCounter.py

def count_vowels(word):
    vowels = 'aeiouAEIOU'
    count = 0

    for char in word:
        if char in vowels:
            count += 1

    return count

# Example usage
if __name__ == "__main__":
    user_input = input("Enter a word: ")
    vowel_count = count_vowels(user_input)
    print(f"Number of vowels in '{user_input}':", vowel_count)
