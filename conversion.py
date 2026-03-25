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
    print(kilometers)

def kilometers_to_miles(kilometers):
    """
    Convert kilometers to miles.
    """
    miles = kilometers / 1.60934
    print(miles)

def fahrenheit_to_celsius(fahrenheit):
    """
    Convert Fahrenheit to Celsius.
    """
    celsius = (fahrenheit - 32) * 5/9
    print(celsius)

def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit.
    """
    fahrenheit = (celsius * 9/5) + 32
    print(fahrenheit)
