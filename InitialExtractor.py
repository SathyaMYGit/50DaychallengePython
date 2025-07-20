# InitialExtractor.py

def extract_initials(full_name):
    # Split the full name by spaces
    name_parts = full_name.strip().split()
    
    # Take the first letter of each part and capitalize it
    initials = [part[0].upper() for part in name_parts if part]
    
    # Join the initials with a space
    return ' '.join(initials)

# Example usage
if __name__ == "__main__":
    name = input("Enter full name: ")
    print("Initials:", extract_initials(name))
