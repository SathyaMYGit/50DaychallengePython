# NameList.py

def main():
    print("Enter 5 names:")
    names = []

    for i in range(1, 6):
        name = input(f"Name {i}: ")
        names.append(name)

    print("\nNames and their lengths:")
    for name in names:
        print(f"{name} - {len(name)} characters")

if __name__ == "__main__":
    main()
