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

def factorial(n):
  if n == 0 or n == 1:
    return 1
  else:
    return n * factorial(n - 1)

def power(base, exponent):
    if exponent == 0:
        return 1
    else:
        return base * power(base, exponent - 1)

def prime_factorization(n):
    """Return the prime factorization of n as a list of prime factors"""
    n = int(n)
    if n <= 1:
        return []
    
    factors = []
    divisor = 2
    
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1
    
    if n > 1:
        factors.append(n)
    
    return factors

def fibonacci_sequence(n):
    """Return the Fibonacci sequence up to the nth number and the nth value."""
    n = int(n)
    if n < 0:
        return [], None
    if n == 0:
        return [0], 0
    if n == 1:
        return [0, 1], 1

    sequence = [0, 1]
    while len(sequence) <= n:
        sequence.append(sequence[-1] + sequence[-2])

    return sequence, sequence[n]

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
        print("7. Factorial")
        print("8. Power")
        print("9. Prime Factorization")
        print("10. Fibonacci Sequence")
        print("11. Exit")

        # Get the user's operation choice
        choice = input("\nEnter your choice (1-11): ")

        # Validate that the choice is one of the valid operations (1-11)
        if choice not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
            print("Invalid choice. Please try again.")
            continue

        # Check if user wants to exit
        if choice == "11":
            print("Exiting the calculator. Goodbye!")
            break

        # Determine the input prompt based on the operation choice
        if choice == "7" or choice == "9" or choice == "10":
            prompt = "Enter a number: "
        elif choice == "2":
            prompt = "Enter numbers separated by spaces (all numbers after the first will be subtracted from the first): "
        elif choice == "4":
            prompt = "Enter numbers separated by spaces (all numbers after the first will be divided from the first): "
        elif choice == "8":
            # For power operation, get base and exponent separately
            while True:
                try:
                    base = float(input("Enter base: "))
                    exponent = float(input("Enter exponent: "))
                    inputNumbers = [base, exponent]
                    break
                except ValueError:
                    print("Invalid input. Please enter valid numbers.")
                    continue
        else:
            prompt = "Enter numbers separated by spaces: "

        # Keep asking for numbers until valid input is provided
        if choice != "8":
            while True:
                inputNumbers = input(prompt)
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
        elif choice == "7":
            if len(inputNumbers) != 1:
                print("Invalid input. Please enter exactly one number.")
            else:
                print("\nResult:", factorial(int(inputNumbers[0])))
        elif choice == "8":
            if len(inputNumbers) != 2:
                print("Invalid input. Please enter exactly two numbers.")
            else:
                print("\nResult:", power(int(inputNumbers[0]), int(inputNumbers[1])))
        elif choice == "9":
            if len(inputNumbers) != 1:
                print("Invalid input. Please enter exactly one number.")
            else:
                factors = prime_factorization(inputNumbers[0])
                if factors:
                    print("\nPrime Factorization:", " × ".join(map(str, factors)))
                else:
                    print("\nInvalid input. Please enter a number greater than 1.")
        elif choice == "10":
            if len(inputNumbers) != 1:
                print("Invalid input. Please enter exactly one number.")
            elif inputNumbers[0] < 0 or not inputNumbers[0].is_integer():
                print("Invalid input. Please enter a non-negative whole number.")
            else:
                sequence, nth_value = fibonacci_sequence(int(inputNumbers[0]))
                print("\nFibonacci Sequence:", ", ".join(map(str, sequence)))
                print(f"{int(inputNumbers[0])}th Fibonacci Number:", nth_value)
        else:
            # This else clause should never execute due to earlier validation
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
