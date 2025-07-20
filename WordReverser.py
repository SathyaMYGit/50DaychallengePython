# WordReverser.py

def reverse_words(sentence):
    # Split sentence into words
    words = sentence.strip().split()
    
    # Reverse each word
    reversed_words = [word[::-1] for word in words]
    
    # Join the reversed words back into a sentence
    return ' '.join(reversed_words)

# Example usage
if __name__ == "__main__":
    user_input = input("Enter a sentence: ")
    result = reverse_words(user_input)
    print("Reversed words:", result)
