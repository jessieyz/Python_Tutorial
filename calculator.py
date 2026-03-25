import time

def sum_numbers(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

def subtract_numbers(*numbers): 
    total = 0
    for num in numbers:
        total -= num
    return total

def multiply_numbers(*numbers): 
    total = 1
    for num in numbers:
        total *= num
    return total    

def divide_numbers(*numbers):
    if not numbers:
        return 0
    total = numbers[0]
    for num in numbers[1:]:
        total /= num
    return total

def max_value(*numbers):
    if len(numbers) == 0:
        return None
    return max(numbers)

def min_value(*numbers):
    if len(numbers) == 0:
        return None
    return min(numbers)

# TODO: add more functions for other operations

def main():
    print("\nWelcome to the simple calculator!")
    while True:
        time.sleep(2)
        # Display the operation menu
        print("\nSelect an operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Max")
        print("6. Min")
        print("7. Exit")

        # Get the user's operation choice
        choice = input("\nEnter your choice (1-7): ")

        # Check if user wants to exit
        if choice == "7":
            print("Exiting the calculator. Goodbye!")
            break

        # Validate that the choice is one of the valid operations (1-6)
        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Invalid choice. Please try again.")
            continue

        # Keep asking for numbers until valid input is provided
        while True:
            inputNumbers = input("Enter numbers separated by spaces: ")
            try:
                # Convert input string to list of floats
                inputNumbers = list(map(float, inputNumbers.split()))
                # Check if the list is empty
                if not inputNumbers:
                    print("Invalid input. Please enter at least one number.")
                    continue
                # Exit the loop if numbers are valid
                break
            except ValueError:
                # Handle case where conversion to float fails
                print("Invalid input. Please enter numbers separated by spaces.")
                continue

        # Perform the selected operation based on the choice
        if choice == "1":
            print("\nResult:", sum_numbers(*inputNumbers))
        elif choice == "2":
            print("\nResult:", subtract_numbers(*inputNumbers))
        elif choice == "3":
            print("\nResult:", multiply_numbers(*inputNumbers))
        elif choice == "4":
            print("\nResult:", divide_numbers(*inputNumbers))
        elif choice == "5":
            print("\nResult:", max_value(*inputNumbers))
        elif choice == "6":
            print("\nResult:", min_value(*inputNumbers))
        else:
            # This else clause should never execute due to earlier validation
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()