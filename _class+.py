import random

# Define all class options
art_map = {1: "Art", 2: "Theatre"}
music_map = {3: "Choir", 4: "Band"}
math_maps = {
    '8': {5: "Algebra", 6: "Geometry"},
    '7': {5: "Pre-Algebra", 6: "Algebra"},
    '6': {5: "Pre-Algebra", 6: "Pre-Algebra Prep"}
}
language_map = {7: "Spanish", 8: "Chinese", 9: "French"}
language_maps = {'8': language_map, '7': language_map, '6': language_map}
language_range = {'8': (7, 9), '7': (7, 9), '6': (7, 9)}

def assign_classes(grade):
    arts_num = random.randint(1, 2)
    music_num = random.randint(3, 4)
    math_num = random.randint(5, 6)
    lang_num = random.randint(*language_range[grade])

    arts = art_map[arts_num]
    music = music_map[music_num]
    math = math_maps[grade][math_num]
    language = language_maps[grade][lang_num]

    if grade == '6':
        # For 6th grade, assign other classes for the second half
        other_arts = art_map[2 if arts_num == 1 else 1]
        other_music = music_map[4 if music_num == 3 else 3]
        print(f"You are in {arts} and {music} for the first half of the year and {other_arts} and {other_music} for the second half of the year. You are also in {language}, and {math}.")
    else:
        print(f"You are in {arts}, {music}, {language}, and {math}.")

grade = input("Put your grade: ")
if grade in ['6', '7', '8']:
    assign_classes(grade)
else:
    print("Invalid grade. Please enter 6, 7, or 8.")