# NameFormatter.py

def format_name(full_name):
    parts = full_name.strip().split()

    if len(parts) < 2:
        return "Please enter at least first and last name."

    first = parts[0].capitalize()
    last = parts[-1].capitalize()
    middle = ' '.join(p.capitalize() for p in parts[1:-1]) if len(parts) > 2 else ''

    # Formats
    formats = {
        "First Last": f"{first} {last}",
        "Last, First": f"{last}, {first}",
        "Initials": ' '.join(p[0].upper() for p in parts),
        "Full Name with Middle": f"{first} {middle} {last}".strip()
    }

    return formats

# Example usage
if __name__ == "__main__":
    name = input("Enter full name: ")
    results = format_name(name)

    if isinstance(results, dict):
        print("\nFormatted Outputs:")
        for key, value in results.items():
            print(f"{key}: {value}")
    else:
        print(results)
