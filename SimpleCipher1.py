# SimpleCipher.py

def simple_cipher(text):
    result = ''
    for char in text:
        if char.isalpha():
            shift = 1
            if char.islower():
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            elif char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += char  # Non-alphabetic characters remain unchanged
    return result

# Example usage
if __name__ == "__main__":
    user_input = input("Enter a word to encrypt: ")
    encrypted = simple_cipher(user_input)
    print("Encrypted word:", encrypted)
