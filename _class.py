# Prompt the user to enter their grade
grade = input("Put your grade: ")

# Check if the user is in 8th grade
if grade == '8':
    import random

    # Define class options for 8th grade
    art_map = {1: "Art", 2: "Theatre"}
    music_map = {3: "Choir", 4: "Band"}
    math_map = {5: "Algebra", 6: "Geometry"}
    language_map = {7: "Spanish", 8: "Chinese", 9: "French"}

    # Randomly assign classes to the user
    arts = art_map[random.randint(1, 2)]
    music = music_map[random.randint(3, 4)]
    math = math_map[random.randint(5, 6)]
    language = language_map[random.randint(7, 9)]

    # Print the assigned classes
    print(f"You are in {arts}, {music}, {language}, and {math}.")

# Check if the user is in 7th grade
elif grade == '7':
    import random

    # Define class options for 7th grade
    art_map = {1: "Art", 2: "Theatre"}
    music_map = {3: "Choir", 4: "Band"}
    math_map = {5: "Pre-Algebra", 6: "Algebra"}
    language_map = {7: "Spanish", 8: "Chinese", 9: "French"}

    # Randomly assign classes to the user
    arts = art_map[random.randint(1, 2)]
    music = music_map[random.randint(3, 4)]
    math = math_map[random.randint(5, 6)]
    language = language_map[random.randint(7, 9)]

    # Print the assigned classes
    print(f"You are in {arts}, {music}, {language}, and {math}.")

# Check if the user is in 6th grade
elif grade == '6':
    import random
    
    # Define class options for 6th grade
    art_map = {1: "Art", 2: "Theatre"}
    music_map = {3: "Choir", 4: "Band"}
    math_map = {5: "Pre-Algebra", 6: "Pre-Algebra Prep"}
    language_map = {7: "Spanish", 8: "Chinese", 9: "French"}

    # Randomly assign classes to the user
    arts = art_map[random.randint(1, 2)]
    music = music_map[random.randint(3, 4)]
    math = math_map[random.randint(5, 6)]
    language = language_map[random.randint(7, 9)]

    # Determine the other classes for the second half of the year
    other_arts = 2 if arts == art_map[1] else 1
    other_music = 4 if music == music_map[3] else 3

    # Print the assigned classes for both halves of the year
    print(f"You are in {arts} and {music} for the first half of the year and {art_map[other_arts]} and {music_map[other_music]} for the second half of the year. You are also in {language}, and {math}.")

# Handle invalid input
else:
    print("Invalid grade. Please enter 6, 7, or 8.")