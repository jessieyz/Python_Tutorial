import time

def get_choice(prompt):
    """
    Repeatedly ask for input until a valid number or decimal is entered.
    
    Args:
        prompt (str): The question to ask the player
    
    Returns:
        float: The numeric value entered by the player
    """
    while True:
        try:
            choice = input(prompt).strip()
            # Convert to float (accepts both integers and decimals)
            return float(choice)
        except ValueError:
            print("Invalid input. Please enter a valid number or decimal.")

def miles_to_kilometers(miles):
    """
    Convert miles to kilometers.
    """
    kilometers = miles * 1.60934
    return kilometers

def kilometers_to_miles(kilometers):
    """
    Convert kilometers to miles.
    """
    miles = kilometers / 1.60934
    return miles

def fahrenheit_to_celsius(fahrenheit):
    """
    Convert Fahrenheit to Celsius.
    """
    celsius = (fahrenheit - 32) * 5/9
    return celsius

def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit.
    """
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit
            
def main():
    """
    Main function to handle user input and conversion requests.
    """
    print("\n=== Unit Conversion Tool ===")
    time.sleep(1)  # Pause for a moment before showing options
    print("\nAvailable conversions:")
    print("1. Miles to Kilometers")
    print("2. Kilometers to Miles")
    print("3. Fahrenheit to Celsius")
    print("4. Celsius to Fahrenheit")
    
    # Get conversion type from user
    conversion_type = input("\nEnter the conversion type (1-4): ").strip()
    
    # Get the number to convert
    number = get_choice("Enter the number to convert: ")
    
    # Perform the conversion based on user choice
    if conversion_type == "1":
        result = miles_to_kilometers(number)
        print(f"\nResult: {number} mi = {result:.10f}".rstrip('0').rstrip('.') + " km")
    elif conversion_type == "2":
        result = kilometers_to_miles(number)
        print(f"\nResult: {number} km = {result:.10f}".rstrip('0').rstrip('.') + " mi")
    elif conversion_type == "3":
        result = fahrenheit_to_celsius(number)
        print(f"\nResult: {number}°F = {result:.10f}".rstrip('0').rstrip('.') + "°C")
    elif conversion_type == "4":
        result = celsius_to_fahrenheit(number)
        print(f"\nResult: {number}°C = {result:.10f}".rstrip('0').rstrip('.') + "°F")
    else:
        print("\nInvalid conversion type. Please enter 1-4.")

if __name__ == "__main__":
    while True:
        main()
        ask_again = input("\nWould you like to perform another conversion? (yes/no): ").strip().lower()
        if ask_again != "yes":
            print("\nThank you for using the Unit Conversion Tool!")
            break
