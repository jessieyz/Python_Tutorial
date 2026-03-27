import time 
import os
import datetime

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_section(text):
    """Print a section header with visual separation."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")

def print_divider():
    """Print a divider line."""
    print("\n" + "-" * 60 + "\n")

def get_choice(prompt, valid_options):
    """
    Repeatedly ask for input until a valid choice is made.
    
    Args:
        prompt (str): The question to ask the player
        valid_options (list): List of valid responses (e.g., ["1", "2", "3"])
    
    Returns:
        str: The valid choice entered by the player
    """
    choice = None
    while choice not in valid_options:
        choice = input(prompt).strip().lower()
        if choice not in valid_options:
            print(f"Invalid choice. Please enter one of: {', '.join(valid_options)}")
    return choice

def narrate(text, pause_time=2):
    """
    Print narrative text with a pause for dramatic effect.
    
    Args:
        text (str): The text to display
        pause_time (int): Seconds to pause after printing
    """
    print(text)
    time.sleep(pause_time)

def game_guidelines():
    """Display game guidelines and rules."""
    # TODO: Review and edit the RULES and HOW TO PLAY sections
    print_section("GAME GUIDELINES & RULES")
    time.sleep(2)
    print("Welcome, brave adventurer!")
    time.sleep(2)
    print()
    print("GAME CONTEXT:")
    print("You find yourself trapped in a mysterious place with no memory of how you got there.")
    print("Your only goal: ESCAPE TO THE OUTSIDE and find your way back home.")
    print("The choices you make will determine whether you find freedom or remain trapped forever.")
    print()
    print("RULES:")
    print("1. Make choices carefully - your decisions shape the story")
    print("2. Enter the number or word corresponding to your choice")
    print("3. Each path leads to different outcomes and endings")
    print("4. Some choices may lead to dead ends - try again!")
    print("5. Explore all paths to discover hidden stories and escape routes")
    print()
    print("HOW TO PLAY:")
    print("• Read the story carefully")
    print("• Choose options by entering the specified number or word")
    print("• Enjoy the narrative unfold based on your decisions")
    print("• Play multiple times to discover all endings and escape routes")
    print_divider()

def play_game():
    """Run one complete game. Returns True if player wants to play again, False otherwise."""
    clear_screen()
    print_section("Welcome to the choose your own adventure game!")
    time.sleep(3)
    x = datetime.datetime.now()
    print(f"Current date and time: {x.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(3)
    game_guidelines()
    time.sleep(5)
    narrate("You are in a room with two doors. One on the right and one on the left.", 3)
    print_divider()
    
    # First choice: which door?
    print("Which door do you pick?")
    print("1. Right Door")
    print("2. Left Door")
    first_door = get_choice("Enter 1 or 2: ", ["1", "2"])
    
    if first_door == "1":
        play_right_door()
    elif first_door == "2":
        play_left_door()
    
    return True  # ask to play again by default

def play_right_door():
    """Handle the right door storyline."""
    print_divider()
    narrate("You find yourself walking down a narrow hallway.", 2)
    narrate("At the end of the hallway, you see a bookshelf with a small table next to it. On the table is a vase filled with red roses.", 4)
    print_divider()
    
    # Second choice: what to examine?
    print("Do you want to examine the book shelf, the vase, or the table?")
    print("1. Examine the bookshelf")
    print("2. Examine the vase")
    print("3. Examine the table")
    examination = get_choice("Enter 1, 2, or 3: ", ["1", "2", "3"])
    
    if examination == "1":
        play_bookshelf_path()
    elif examination == "2":
        play_vase_path()
    elif examination == "3":
        play_table_path()

def play_vase_path():
    """Handle the vase examination."""
    print_divider()
    narrate("You examine the vase and find nothing out of the ordinary about the flowers. The flowers are the color of blood.", 3)
    # TODO: Add more story content for the vase path
    # TODO: Implement branching choices for vase path

def play_table_path():
    """Handle the table examination."""
    print_divider()
    narrate("You examine the table and find a note.", 3)
    # TODO: Add more story content for the table path
    # TODO: Implement what the note says
    # TODO: Add branching choices based on note discovery

def play_bookshelf_path():
    """Handle the bookshelf examination."""
    narrate("You examine the bookshelf and find a book that catches your eye.", 3)
    narrate("When you try to take the book out, the bookshelf swings forward revealing two sets of stairs, one leading up and the other down.", 5)
    print_divider()
    
    # Third choice: which stairs?
    print("Do you want to go up the stairs or down the stairs?")
    print("1. Go Up")
    print("2. Go Down")
    stairs_choice = get_choice("Enter 1 or 2: ", ["1", "2"])
    
    if stairs_choice == "1":
        play_upstairs_path()
    elif stairs_choice == "2":
        play_downstairs_path()

def play_downstairs_path():
    """Handle going downstairs."""
    print_divider()
    narrate("You descend the stairs and find yourself in a dark basement.", 3)
    # TODO: Add more story content for the downstairs path
    # TODO: Implement basement exploration and choices
    # TODO: Create basement ending scenarios

def play_upstairs_path():
    """Handle going upstairs."""
    print_divider()
    narrate("You climb the stairs and find yourself facing a door just outside a brightly lit, empty room.", 2)
    print_divider()
    
    # Final choice: enter the room?
    print("Do you want to enter the room?")
    room_choice = get_choice("Enter yes or no: ", ["yes", "no"])
    
    if room_choice == "yes":
        play_bright_room_ending()
    elif room_choice == "no":
        play_abyss_ending()

def play_bright_room_ending():
    """The bright room ending."""
    print_divider()
    narrate("You enter the room.", 2)
    narrate("As you step forward, the bright light blinds you and pulls you upward.", 4)
    narrate("You try to fight it, but the light is too strong.", 4)
    narrate("You feel yourself being pulled into the light and lose consciousness.", 4)
    narrate("The end.", 2)

def play_abyss_ending():
    """The dark abyss ending."""
    print_divider()
    narrate("You decide not to enter the room.", 2)
    narrate("Suddenly, the floor opens beneath you.", 2)
    narrate("You fall into a dark abyss.", 2)
    narrate("The end.", 2)

def play_left_door():
    """Handle the left door storyline."""
    print_divider()
    narrate("You find yourself entering another room with a single table in the center.", 3)
    # TODO: Add more story content for the left door path
    # TODO: Implement left door room exploration
    # TODO: Add choices and branching paths for left door

# Main game loop
if __name__ == "__main__":
    while True:
        ask_again = play_game()
        if ask_again:
            time.sleep(1)
            play_again = get_choice("\nWould you like to play again? (yes/no): ", ["yes", "no"])
            if play_again == "yes":
                print("Restarting the game...")
                time.sleep(1)
                continue
            else:
                print("Thank you for playing!")
                break
        else:
            print("Thank you for playing!")
            break
