import json
import random
from itertools import permutations
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

CHINESE_CONFIG = {
    "title": "Chinese",
    "roster_file": BASE_DIR / "chinese_class_rosters.json",
    "max_capacity": 14,
    "allow_non_binary": False,
    "table_count": 7,
    "seats_per_table": 2,
}

ENGLISH_CONFIG = {
    "title": "English",
    "roster_file": BASE_DIR / "english_class_rosters.json",
    "max_capacity": 19,
    "allow_non_binary": True,
}

MATH_CONFIG = {
    "title": "Math",
    "roster_file": BASE_DIR / "math_class_rosters.json",
    "max_capacity": 20,
    "allow_non_binary": True,
    "table_count": 10,
    "seats_per_table": 2,
}

ENGLISH_TABLE_ALIASES = {
    "alpha": "Alpha",
    "bravo": "Bravo",
    "charley": "Charley",
    "delta": "Delta",
}


def print_section_title(title):
    print(f"\n\n{title}")
    print("-" * len(title))


def prompt_choice(prompt, valid_choices, aliases=None):
    aliases = aliases or {}
    while True:
        choice = input(prompt).strip().lower()
        choice = aliases.get(choice, choice)
        if choice in valid_choices:
            return choice
        print(f"Please choose one of: {', '.join(valid_choices)}")


def prompt_yes_no(prompt, default="no"):
    suffix = "[Y/n]" if default == "yes" else "[y/N]"
    while True:
        choice = input(f"{prompt} {suffix} ").strip().lower()
        if not choice:
            return default == "yes"
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no"}:
            return False
        print("Please type y or n.")


def format_student_name(raw_name):
    if raw_name.count(",") != 1:
        return None

    last_name, first_name = [part.strip() for part in raw_name.split(",", 1)]
    if not last_name or not first_name:
        return None

    return f"{last_name}, {first_name}"


def get_student_names(max_capacity):
    while True:
        print_section_title("Student Roster")
        print(f"Enter up to {max_capacity} students.")
        print("Use this format: Last, First")
        print("Example: Smith, Jordan")
        print("Press Enter on a blank line when you are done.\n")

        names = []
        while True:
            raw_name = input().strip()
            if not raw_name:
                break

            formatted_name = format_student_name(raw_name)
            if not formatted_name:
                print("Use the format: Last, First")
                continue

            if formatted_name in names:
                print("That student is already listed.")
                continue

            if len(names) >= max_capacity:
                print(f"There are only {max_capacity} seats available.")
                break

            names.append(formatted_name)
            print(f"Added {len(names)}/{max_capacity}: {formatted_name}")

        if names:
            return names

        print("Please enter at least one student name.\n")


def normalize_gender(raw_gender, allow_non_binary):
    cleaned = raw_gender.strip().lower()
    if cleaned in {"girl", "female", "f", "g"}:
        return "girl"
    if cleaned in {"boy", "male", "m", "b"}:
        return "boy"
    if allow_non_binary and cleaned in {"non-binary", "nonbinary", "nb", "enby"}:
        return "non-binary"
    return None


def get_student_genders(names, allow_non_binary):
    print_section_title("Student Genders")
    print("Enter each student's gender.")
    if allow_non_binary:
        print("Use girl/female, boy/male, or non-binary.")
    else:
        print("Use girl/female or boy/male.")

    genders = {}
    for name in names:
        while True:
            raw_gender = input(f"{name}: ")
            gender = normalize_gender(raw_gender, allow_non_binary)
            if gender is None:
                if allow_non_binary:
                    print("Please enter girl, female, boy, male, or non-binary.")
                else:
                    print("Please enter girl, female, boy, or male.")
                continue

            genders[name] = gender
            break

    return genders


def load_saved_rosters(roster_file):
    if not roster_file.exists():
        return {}

    try:
        with roster_file.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return {}

    valid_rosters = {}
    for roster_name, roster_data in data.items():
        if not isinstance(roster_name, str) or not isinstance(roster_data, dict):
            continue

        names = roster_data.get("names")
        genders = roster_data.get("genders")
        if not isinstance(names, list) or not isinstance(genders, dict):
            continue
        if any(not isinstance(name, str) for name in names):
            continue
        if any(name not in genders or not isinstance(genders[name], str) for name in names):
            continue

        valid_rosters[roster_name] = {
            "names": names,
            "genders": genders,
        }

    return valid_rosters


def save_saved_rosters(rosters, roster_file):
    with roster_file.open("w", encoding="utf-8") as handle:
        json.dump(rosters, handle, indent=2)


def prompt_to_save_roster(names, genders, saved_rosters, roster_file):
    print_section_title("Save Roster")
    print(f"You entered {len(names)} students.")

    if not prompt_yes_no("Would you like to save this roster for later?"):
        return saved_rosters

    while True:
        roster_name = input("Roster name: ").strip()
        if not roster_name:
            print("Please enter a roster name.")
            continue

        saved_rosters[roster_name] = {
            "names": names,
            "genders": genders,
        }
        save_saved_rosters(saved_rosters, roster_file)
        print(f'Saved roster "{roster_name}".')
        return saved_rosters


def choose_or_create_roster(config, return_saved_rosters=False):
    saved_rosters = load_saved_rosters(config["roster_file"])

    while True:
        print_section_title(f"{config['title']} Roster Menu")
        if saved_rosters:
            roster_names = sorted(saved_rosters)
            for index, roster_name in enumerate(roster_names, start=1):
                student_count = len(saved_rosters[roster_name]["names"])
                print(f"{index}. {roster_name} ({student_count} students)")
            print("n. Enter a new roster")

            choice = input("Choose a roster or type n: ").strip().lower()
            if choice == "n":
                break

            if choice.isdigit():
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(roster_names):
                    selected = saved_rosters[roster_names[choice_index]]
                    result = (
                        selected["names"][:],
                        selected["genders"].copy(),
                    )
                    if return_saved_rosters:
                        return result + (saved_rosters,)
                    return result

            print("Please choose one of the listed options.")
            continue

        print("No saved rosters found yet.")
        print("n. Enter a new roster")
        if input("Type n to continue: ").strip().lower() == "n":
            break
        print("Please type n to enter a new roster.")

    names = get_student_names(config["max_capacity"])
    genders = get_student_genders(names, config["allow_non_binary"])
    saved_rosters = prompt_to_save_roster(
        names,
        genders,
        saved_rosters,
        config["roster_file"],
    )
    if return_saved_rosters:
        return names, genders, saved_rosters
    return names, genders


def build_name_lookup(names):
    lookup = {}
    duplicates = set()

    for name in names:
        lower_name = name.lower()
        if lower_name in lookup:
            duplicates.add(lower_name)
        else:
            lookup[lower_name] = name

        last_name, first_name = [part.strip() for part in name.split(",", 1)]
        first_last = f"{first_name} {last_name}".strip().lower()
        if first_last in lookup:
            duplicates.add(first_last)
        else:
            lookup[first_last] = name

    for duplicate in duplicates:
        lookup.pop(duplicate, None)

    return lookup, duplicates


def resolve_name(raw_name, lookup, duplicates):
    cleaned = " ".join(raw_name.strip().lower().split())
    if not cleaned:
        return None
    if cleaned in duplicates:
        return "duplicate"
    return lookup.get(cleaned)


def get_ratio(prompt, label, allow_decimal=False):
    print_section_title("Ratio Setting")
    print(prompt)
    print("Format: number:number")
    print("Examples: 5:1 or 2.5:1\n" if allow_decimal else "Example: 5:1\n")
    while True:
        raw_ratio = input(f"{label}: ").strip()
        parts = [part.strip() for part in raw_ratio.split(":")]
        if len(parts) != 2:
            print("Please enter the ratio in the format number:number, such as 5:1.")
            continue

        try:
            left = float(parts[0]) if allow_decimal else int(parts[0])
            right = float(parts[1]) if allow_decimal else int(parts[1])
        except ValueError:
            print("Please enter the ratio in the format number:number, such as 5:1.")
            continue

        if left <= 0 or right <= 0:
            print("Both numbers must be greater than 0.")
            continue

        return left, right


def build_row_chart(order, table_count, seats_per_table):
    seating_chart = []
    index = 0
    seat_number = 1

    for table_number in range(1, table_count + 1):
        seats = []
        for _ in range(seats_per_table):
            student = order[index] if index < len(order) else "Empty"
            if index < len(order):
                index += 1
            seats.append({"seat_number": seat_number, "student": student})
            seat_number += 1

        seating_chart.append({"table": table_number, "seats": seats})

    return seating_chart


def print_row_view(seating_chart):
    print_section_title("Tables In One Row")

    labels = []
    rows = []
    for table in seating_chart:
        left_seat = table["seats"][0]
        right_seat = table["seats"][-1]
        labels.append(
            f"Table {table['table']} ({left_seat['seat_number']}-{right_seat['seat_number']})"
        )
        seat_text = " / ".join(
            f"{seat['seat_number']}: {seat['student']}" for seat in table["seats"]
        )
        rows.append(seat_text)

    print(" | ".join(labels))
    print(" | ".join(rows))


def print_detailed_chart(seating_chart):
    print_section_title("Detailed Seating Chart")

    for table in seating_chart:
        first_seat = table["seats"][0]["seat_number"]
        last_seat = table["seats"][-1]["seat_number"]
        print(f"Table {table['table']} (Seats {first_seat}-{last_seat})")
        for seat in table["seats"]:
            print(f"  Seat {seat['seat_number']}: {seat['student']}")
        print()


def ask_repeat_options(regenerate_label="r", change_label="c"):
    return input().strip().lower(), regenerate_label, change_label


def chinese_count_same_gender_tables(order, genders):
    count = 0
    for index in range(0, len(order), 2):
        pair = order[index:index + 2]
        if len(pair) == 2 and genders[pair[0]] == genders[pair[1]]:
            count += 1
    return count


def chinese_count_same_gender_neighbors(order, genders):
    count = 0
    for index in range(1, len(order)):
        if genders[order[index - 1]] == genders[order[index]]:
            count += 1
    return count


def chinese_weighted_penalty(same_count, different_count, preference_ratio):
    different_weight, same_weight = preference_ratio
    return (same_count * different_weight) - (different_count * same_weight)


def chinese_generate_best_order(names, genders, preference_ratio, attempts=3000):
    best_order = None
    best_score = None

    for _ in range(attempts):
        order = names[:]
        random.shuffle(order)

        same_table_count = chinese_count_same_gender_tables(order, genders)
        occupied_table_count = len(order) // 2
        different_table_count = occupied_table_count - same_table_count
        same_neighbor_count = chinese_count_same_gender_neighbors(order, genders)
        different_neighbor_count = max(len(order) - 1 - same_neighbor_count, 0)

        score = (
            chinese_weighted_penalty(same_table_count, different_table_count, preference_ratio),
            chinese_weighted_penalty(
                same_neighbor_count,
                different_neighbor_count,
                preference_ratio,
            ),
            random.random(),
        )

        if best_score is None or score < best_score:
            best_score = score
            best_order = order[:]
            if score[0] <= 0 and score[1] <= 0:
                break

    return best_order


def chinese_format_pattern(order, genders):
    return " | ".join(
        f"{index + 1}: {genders[student].title()}"
        for index, student in enumerate(order)
    )


def chinese_explain_preferences(order, genders, preference_ratio):
    same_table_count = chinese_count_same_gender_tables(order, genders)
    occupied_table_count = len(order) // 2
    different_table_count = occupied_table_count - same_table_count
    same_neighbor_count = chinese_count_same_gender_neighbors(order, genders)
    different_neighbor_count = max(len(order) - 1 - same_neighbor_count, 0)
    different_weight, same_weight = preference_ratio

    print_section_title("Preference Check")
    print(f"Different-gender to same-gender preference ratio: {different_weight}:{same_weight}")
    print(f"Different-gender tables: {different_table_count}")
    print(f"Same-gender tables: {same_table_count}")
    print(f"Same-gender neighbors in row: {same_neighbor_count}")
    print(f"Different-gender neighbors in row: {different_neighbor_count}")


def run_chinese():
    while True:
        print_section_title("Chinese Class Seating Chart Generator")
        print("Room layout: 7 tables in one row, 2 seats at each table.")
        print("Preference: alternate girl and boy as much as possible across the row.")

        names, genders = choose_or_create_roster(CHINESE_CONFIG)
        preference_ratio = get_ratio(
            "Enter the different-gender to same-gender seating preference ratio.",
            "Ratio",
        )

        while True:
            order = chinese_generate_best_order(names, genders, preference_ratio)
            seating_chart = build_row_chart(order, 7, 2)

            print("\nPreferred row pattern by seat:")
            print(chinese_format_pattern(order, genders))
            print_row_view(seating_chart)
            print_detailed_chart(seating_chart)
            chinese_explain_preferences(order, genders, preference_ratio)

            print_section_title("Next Step")
            print("r = make another chart with the same settings")
            print("c = change only the ratio and make a new chart")
            print("m = go back to the Chinese class menu")
            print("h = go back to the home menu")
            print("Press Enter to finish")
            choice = input("Choice: ").strip().lower()
            if choice == "r":
                continue
            if choice == "c":
                preference_ratio = get_ratio(
                    "Enter the different-gender to same-gender seating preference ratio.",
                    "Ratio",
                )
                continue
            if choice == "m":
                break
            if choice == "h":
                return "home"
            return None


def english_get_tables(student_count):
    bravo_capacity = 4 if student_count <= 17 else 5
    delta_capacity = 4 if student_count <= 18 else 5
    return {
        "Alpha": {"capacity": 4, "zone": "front", "prefix": "a"},
        "Bravo": {"capacity": bravo_capacity, "zone": "back", "prefix": "b"},
        "Charley": {"capacity": 5, "zone": "back", "prefix": "c"},
        "Delta": {"capacity": delta_capacity, "zone": "front", "prefix": "d"},
    }


def english_get_conflicts(names):
    print_section_title("Students Who Cannot Sit Together")
    print("Enter pairs of students who cannot sit together.")
    print("Use this format: First Last, First Last")
    print("Example: Jordan Smith, Alex Lee")
    print("Press Enter on a blank line when you are done.")

    lookup, duplicates = build_name_lookup(names)
    conflicts = {name: set() for name in names}

    while True:
        raw_pair = input("Conflict: ").strip()
        if not raw_pair:
            return conflicts

        if raw_pair.count(",") != 1:
            print("Please use the format: First Last, First Last")
            continue

        left_raw, right_raw = [part.strip() for part in raw_pair.split(",", 1)]
        left_name = resolve_name(left_raw, lookup, duplicates)
        right_name = resolve_name(right_raw, lookup, duplicates)

        if left_name == "duplicate" or right_name == "duplicate":
            print("That name matches more than one student. Please be more specific.")
            continue
        if not left_name or not right_name:
            print("One or both names were not found in the student list.")
            continue
        if left_name == right_name:
            print("A student cannot be listed with themselves.")
            continue

        conflicts[left_name].add(right_name)
        conflicts[right_name].add(left_name)


def english_parse_requirement(raw_requirement):
    cleaned = raw_requirement.strip().lower()
    if cleaned in {"front", "back"}:
        return {"type": "zone", "value": cleaned}
    if cleaned in ENGLISH_TABLE_ALIASES:
        return {"type": "table", "value": ENGLISH_TABLE_ALIASES[cleaned]}
    return None


def english_get_requirements(names):
    print_section_title("Required Seating")
    print("Enter seating requirements for specific students.")
    print("Examples:")
    print("  Alex Smith, front")
    print("  Jordan Jones, Bravo")
    print("Press Enter on a blank line when you are done.")

    lookup, duplicates = build_name_lookup(names)
    requirements = {}

    while True:
        entry = input("Requirement: ").strip()
        if not entry:
            return requirements
        if entry.count(",") != 1:
            print("Please use the format: First Last, front")
            continue

        student_raw, requirement_raw = [part.strip() for part in entry.split(",", 1)]
        student = resolve_name(student_raw, lookup, duplicates)
        if student == "duplicate":
            print("That name matches more than one student. Please be more specific.")
            continue
        if not student:
            print("That student was not found in the student list.")
            continue

        requirement = english_parse_requirement(requirement_raw)
        if not requirement:
            print("Use front, back, Alpha, Bravo, Charley, or Delta.")
            continue

        requirements[student] = requirement


def english_allowed_tables(student, requirements, tables):
    if student not in requirements:
        return list(tables)

    requirement = requirements[student]
    if requirement["type"] == "table":
        return [requirement["value"]]

    return [
        table_name
        for table_name, details in tables.items()
        if details["zone"] == requirement["value"]
    ]


def english_can_place(student, table_name, seating_chart, conflicts, tables):
    if len(seating_chart[table_name]) >= tables[table_name]["capacity"]:
        return False

    return all(other not in conflicts[student] for other in seating_chart[table_name])


def english_gender_counts(students, genders):
    counts = {}
    for student in students:
        counts[genders[student]] = counts.get(genders[student], 0) + 1
    return counts


def english_table_gender_score(table_name, student, seating_chart, genders):
    placed = seating_chart[table_name] + [student]
    counts = list(english_gender_counts(placed, genders).values())
    return max(counts) - min(counts) if counts else 0


def english_adjacent_gender_score(table_name, student, seating_chart, genders, alternation_ratio):
    students = seating_chart[table_name]
    if not students:
        return 0

    previous_gender = genders[students[-1]]
    current_gender = genders[student]
    if "non-binary" in {previous_gender, current_gender}:
        return 0
    if previous_gender != current_gender:
        return 0

    preferred_count, allowed_count = alternation_ratio
    total = preferred_count + allowed_count
    return 0 if random.randint(1, total) <= allowed_count else 1


def english_table_has_boy_and_girl(students, genders):
    table_genders = {genders[student] for student in students}
    return "boy" in table_genders and "girl" in table_genders


def english_chart_meets_gender_rule(seating_chart, genders):
    return all(
        english_table_has_boy_and_girl(students, genders)
        for students in seating_chart.values()
    )


def english_best_table_order(students, genders):
    if len(students) <= 1:
        return students[:]

    best_order = students[:]
    best_score = None

    for candidate in permutations(students):
        score = 0
        for index in range(1, len(candidate)):
            previous_gender = genders[candidate[index - 1]]
            current_gender = genders[candidate[index]]
            if "non-binary" in {previous_gender, current_gender}:
                continue
            if previous_gender == current_gender:
                score += 1
        if best_score is None or score < best_score:
            best_score = score
            best_order = list(candidate)

    return best_order


def english_solve_chart(names, genders, conflicts, requirements, tables, alternation_ratio):
    seating_chart = {table_name: [] for table_name in tables}

    def choose_next_student(unseated_students):
        return min(
            unseated_students,
            key=lambda student: (
                len(
                    [
                        table_name
                        for table_name in english_allowed_tables(student, requirements, tables)
                        if english_can_place(student, table_name, seating_chart, conflicts, tables)
                    ]
                ),
                -len(conflicts[student]),
            ),
        )

    def backtrack(unseated_students):
        if not unseated_students:
            return english_chart_meets_gender_rule(seating_chart, genders)

        student = choose_next_student(unseated_students)
        possible_tables = [
            table_name
            for table_name in english_allowed_tables(student, requirements, tables)
            if english_can_place(student, table_name, seating_chart, conflicts, tables)
        ]
        random.shuffle(possible_tables)
        possible_tables.sort(
            key=lambda table_name: (
                english_adjacent_gender_score(
                    table_name,
                    student,
                    seating_chart,
                    genders,
                    alternation_ratio,
                ),
                english_table_gender_score(table_name, student, seating_chart, genders),
                len(seating_chart[table_name]),
            )
        )

        for table_name in possible_tables:
            seating_chart[table_name].append(student)
            remaining = [name for name in unseated_students if name != student]
            if backtrack(remaining):
                return True
            seating_chart[table_name].pop()

        return False

    if not backtrack(names[:]):
        return None

    return {
        table_name: english_best_table_order(students, genders)
        for table_name, students in seating_chart.items()
    }


def english_print_chart(seating_chart, tables):
    print_section_title("Seating Chart")

    for table_name, details in tables.items():
        print(f"{table_name} ({details['zone']}, {details['capacity']} seats)")
        if seating_chart[table_name]:
            for seat_number, student in enumerate(seating_chart[table_name], start=1):
                print(f"  {details['prefix']}{seat_number}: {student}")
        else:
            print("  No one assigned")
        print()


def run_english():
    while True:
        print_section_title("English Class Seating Chart Generator")
        print("Room layout: Alpha and Delta are front tables.")
        print("Bravo and Charley are back tables.")

        names, genders, _ = choose_or_create_roster(ENGLISH_CONFIG, return_saved_rosters=True)
        tables = english_get_tables(len(names))
        alternation_ratio = get_ratio(
            "Enter the boy/girl alternation preference ratio.\nExample: 5:1 means prefer alternating 5 times as often as same-gender neighbors.",
            "Ratio",
        )
        conflicts = english_get_conflicts(names)
        requirements = english_get_requirements(names)

        while True:
            seating_chart = english_solve_chart(
                names,
                genders,
                conflicts,
                requirements,
                tables,
                alternation_ratio,
            )

            if seating_chart is None:
                print("\nNo valid seating chart could be created with those rules.")
                print("Try removing or changing some restrictions.")
                return None

            english_print_chart(seating_chart, tables)

            print_section_title("Next Step")
            print("r = make another chart with the same settings")
            print("ratio = change only the ratio and make a new chart")
            print("m = go back to the English class menu")
            print("h = go back to the home menu")
            print("Press Enter to finish")
            choice = input().strip().lower()
            if choice == "r":
                continue
            if choice == "ratio":
                alternation_ratio = get_ratio(
                    "Enter the boy/girl alternation preference ratio.\nExample: 5:1 means prefer alternating 5 times as often as same-gender neighbors.",
                    "Ratio",
                )
                continue
            if choice == "m":
                break
            if choice == "h":
                return "home"
            return None


def math_get_pairs(names, prompt_title, prompt_detail):
    print_section_title(prompt_title)
    print(prompt_detail)
    print("Enter one pair per line in this format: First Last, First Last")
    print("Example: Jordan Smith, Alex Lee")
    print("Press Enter on a blank line when you are done.")

    lookup, duplicates = build_name_lookup(names)
    pairs = []
    seen = set()

    while True:
        raw_pair = input("Pair: ").strip()
        if not raw_pair:
            return pairs
        if raw_pair.count(",") != 1:
            print("Use the format: First Last, First Last")
            continue

        left_raw, right_raw = [part.strip() for part in raw_pair.split(",", 1)]
        left_name = resolve_name(left_raw, lookup, duplicates)
        right_name = resolve_name(right_raw, lookup, duplicates)

        if left_name == "duplicate" or right_name == "duplicate":
            print("That First Last name matches more than one student in the class list.")
            continue
        if not left_name or not right_name:
            print("Both names must match students in the class list.")
            continue
        if left_name == right_name:
            print("A student cannot be paired with themself.")
            continue

        pair = tuple(sorted((left_name, right_name)))
        if pair in seen:
            print("That pair is already listed.")
            continue

        seen.add(pair)
        pairs.append(pair)


def math_get_seat_preferences(names):
    print_section_title("Seat Preferences")
    print("Enter student seat preferences.")
    print("These are soft preferences. The generator will try to honor them, but it may not always be possible.")
    print("Enter one preference per line in this format: First Last, SeatNumber")
    print("Example: Jordan Smith, 4")
    print(f"Seat numbers must be between 1 and {len(names)} for this class list.")
    print("Press Enter on a blank line when you are done.")

    lookup, duplicates = build_name_lookup(names)
    preferences = {}
    used_seats = set()

    while True:
        raw_preference = input("Seat preference: ").strip()
        if not raw_preference:
            return preferences
        if raw_preference.count(",") != 1:
            print("Use the format: First Last, SeatNumber")
            continue

        student_raw, seat_raw = [part.strip() for part in raw_preference.split(",", 1)]
        student = resolve_name(student_raw, lookup, duplicates)
        if student == "duplicate":
            print("That First Last name matches more than one student in the class list.")
            continue
        if not student:
            print("The student name must match the class list.")
            continue
        if not seat_raw.isdigit():
            print(f"Seat number must be a whole number from 1 to {len(names)}.")
            continue

        seat_number = int(seat_raw)
        if seat_number < 1 or seat_number > len(names):
            print(f"Seat number must be between 1 and {len(names)} for this class list.")
            continue
        if student in preferences:
            print("That student already has a seat preference listed.")
            continue
        if seat_number in used_seats:
            print("That seat already has a different student preference listed.")
            continue

        preferences[student] = seat_number
        used_seats.add(seat_number)


def math_table_pairs(order):
    pair_map = {}
    for index in range(0, len(order), 2):
        pair = order[index:index + 2]
        if len(pair) == 2:
            pair_map[tuple(sorted(pair))] = index // 2 + 1
    return pair_map


def math_blocked_violations(order, blocked_pairs):
    current_pairs = math_table_pairs(order)
    return sum(1 for pair in blocked_pairs if pair in current_pairs)


def math_preferred_misses(order, preferred_pairs):
    current_pairs = math_table_pairs(order)
    return sum(1 for pair in preferred_pairs if pair not in current_pairs)


def math_preferred_hits(order, preferred_pairs):
    return len(preferred_pairs) - math_preferred_misses(order, preferred_pairs)


def math_seat_preference_misses(order, seat_preferences):
    misses = 0
    for student, seat_number in seat_preferences.items():
        seat_index = seat_number - 1
        if seat_index >= len(order) or order[seat_index] != student:
            misses += 1
    return misses


def math_seat_preference_hits(order, seat_preferences):
    return len(seat_preferences) - math_seat_preference_misses(order, seat_preferences)


def math_same_gender_table_count(order, genders):
    count = 0
    for index in range(0, len(order), 2):
        pair = order[index:index + 2]
        if len(pair) == 2 and genders[pair[0]] == genders[pair[1]]:
            count += 1
    return count


def math_target_same_gender_count(order, preference_ratio):
    full_tables = len(order) // 2
    different_weight, same_weight = preference_ratio
    return full_tables * same_weight / (different_weight + same_weight)


def math_table_ratio_score(order, genders, preference_ratio):
    return abs(
        math_same_gender_table_count(order, genders)
        - math_target_same_gender_count(order, preference_ratio)
    )


def math_generate_best_order(
    names,
    genders,
    preference_ratio,
    preferred_pairs,
    blocked_pairs,
    seat_preferences,
    attempts=3000,
):
    best_order = None
    best_score = None

    for _ in range(attempts):
        order = names[:]
        random.shuffle(order)
        score = (
            math_blocked_violations(order, blocked_pairs),
            math_preferred_misses(order, preferred_pairs),
            math_seat_preference_misses(order, seat_preferences),
            math_table_ratio_score(order, genders, preference_ratio),
            random.random(),
        )
        if best_score is None or score < best_score:
            best_score = score
            best_order = order[:]

    return best_order


def math_randomize_within_tables(order, left_right_ratio, seat_preferences):
    keep_weight, swap_weight = left_right_ratio
    randomized = []

    for index in range(0, len(order), 2):
        pair = order[index:index + 2]
        if len(pair) < 2:
            randomized.extend(pair)
            continue

        keep = pair[:]
        swap = list(reversed(pair))

        keep_hits = sum(
            1
            for offset, student in enumerate(keep)
            if seat_preferences.get(student) == index + offset + 1
        )
        swap_hits = sum(
            1
            for offset, student in enumerate(swap)
            if seat_preferences.get(student) == index + offset + 1
        )

        if swap_hits > keep_hits:
            pair = swap
        elif keep_hits == swap_hits and random.choices(
            ["keep", "swap"],
            weights=[keep_weight, swap_weight],
            k=1,
        )[0] == "swap":
            pair = swap

        randomized.extend(pair)

    return randomized


def math_explain_preferences(
    order,
    genders,
    preference_ratio,
    left_right_ratio,
    preferred_pairs,
    blocked_pairs,
    seat_preferences,
):
    same_table_count = math_same_gender_table_count(order, genders)
    target_same_count = math_target_same_gender_count(order, preference_ratio)
    full_table_count = len(order) // 2
    target_different_count = full_table_count - target_same_count
    blocked_violations = math_blocked_violations(order, blocked_pairs)
    preferred_hits = math_preferred_hits(order, preferred_pairs)
    seat_hits = math_seat_preference_hits(order, seat_preferences)
    different_weight, same_weight = preference_ratio
    keep_weight, swap_weight = left_right_ratio

    print_section_title("Preference Check")
    print(f"Different-gender to same-gender preference ratio: {different_weight}:{same_weight}")
    print(f"Same-gender tables: {same_table_count}")
    print(
        "Target mix for filled tables: "
        f"{target_different_count:.1f} different-gender and {target_same_count:.1f} same-gender"
    )
    print(f"Left-right seat order ratio within each table: {keep_weight}:{swap_weight}")
    print(f"Must-not-sit-together violations: {blocked_violations}")
    print(f"Preferred pairs seated together: {preferred_hits} of {len(preferred_pairs)}")
    print(f"Seat preferences matched: {seat_hits} of {len(seat_preferences)}")


def run_math():
    while True:
        print_section_title("Math Class Seating Chart Generator")
        print("Room layout: 10 tables in one row, 2 seats at each table.")
        print("Preference: mix genders within each table when possible.")

        names, genders, _ = choose_or_create_roster(MATH_CONFIG, return_saved_rosters=True)
        preferred_pairs = math_get_pairs(
            names,
            "Enter pairs who would like to sit together.",
            "These are soft preferences. The generator will try to honor them, but it may not always be possible.",
        )
        blocked_pairs = math_get_pairs(
            names,
            "Enter pairs who definitely should not sit together.",
            "These are strong restrictions. The generator will avoid these pairings whenever possible.",
        )

        conflicting_pairs = set(preferred_pairs) & set(blocked_pairs)
        if conflicting_pairs:
            print("\nPairs listed in both sections will be treated as must-not-sit-together only.")
            preferred_pairs = [pair for pair in preferred_pairs if pair not in conflicting_pairs]

        seat_preferences = math_get_seat_preferences(names)
        preference_ratio = get_ratio(
            "Enter the different-gender to same-gender seating preference ratio.\nDecimals are allowed, such as 2.5:1.",
            "Ratio",
            allow_decimal=True,
        )
        left_right_ratio = get_ratio(
            "Enter the left-right seat order ratio within each table.\nDecimals are allowed, such as 2.5:1.",
            "Left-right ratio",
            allow_decimal=True,
        )

        while True:
            best_order = math_generate_best_order(
                names,
                genders,
                preference_ratio,
                preferred_pairs,
                blocked_pairs,
                seat_preferences,
            )
            displayed_order = math_randomize_within_tables(
                best_order,
                left_right_ratio,
                seat_preferences,
            )
            seating_chart = build_row_chart(displayed_order, 10, 2)

            print_row_view(seating_chart)
            print_detailed_chart(seating_chart)
            math_explain_preferences(
                displayed_order,
                genders,
                preference_ratio,
                left_right_ratio,
                preferred_pairs,
                blocked_pairs,
                seat_preferences,
            )

            print_section_title("Next Step")
            print("r = make another chart with the same settings")
            print("c = change only the ratios and make a new chart")
            print("m = go back to the Math class menu")
            print("h = go back to the home menu")
            print("Press Enter to finish")
            choice = input().strip().lower()
            if choice == "r":
                continue
            if choice == "c":
                preference_ratio = get_ratio(
                    "Enter the different-gender to same-gender seating preference ratio.\nDecimals are allowed, such as 2.5:1.",
                    "Ratio",
                    allow_decimal=True,
                )
                left_right_ratio = get_ratio(
                    "Enter the left-right seat order ratio within each table.\nDecimals are allowed, such as 2.5:1.",
                    "Left-right ratio",
                    allow_decimal=True,
                )
                continue
            if choice == "m":
                break
            if choice == "h":
                return "home"
            return None


def choose_class():
    print_section_title("Combined Seating Chart Generator")
    print("Pick a class to build seating for:")
    print("1. Chinese")
    print("2. English")
    print("3. Math")

    while True:
        choice = input("Choose a class (1-3): ").strip().lower()
        if choice in {"1", "c", "chinese"}:
            return run_chinese
        if choice in {"2", "e", "english"}:
            return run_english
        if choice in {"3", "m", "math"}:
            return run_math
        print("Please choose 1, 2, or 3.")


def main():
    while True:
        generator = choose_class()
        result = generator()
        if result == "home":
            continue
        break


if __name__ == "__main__":
    main()
