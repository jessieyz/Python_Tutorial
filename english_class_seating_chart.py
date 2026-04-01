import json
import random
from pathlib import Path


MAX_CAPACITY = 19
ROSTER_FILE = Path(__file__).with_name("english_class_rosters.json")

TABLE_ALIASES = {
    "alpha": "Alpha",
    "bravo": "Bravo",
    "charley": "Charley",
    "delta": "Delta",
}


def get_student_names():
    while True:
        print("Enter one student per line in this format: Last, First")
        print("Press Enter on a blank line when you are done.")
        print("Student names:")

        names = []
        while True:
            raw_name = input().strip()
            if not raw_name:
                break

            if raw_name.count(",") != 1:
                print("Use the format: Last, First")
                continue

            last_name, first_name = [part.strip() for part in raw_name.split(",", 1)]
            if not last_name or not first_name:
                print("Use the format: Last, First")
                continue

            formatted_name = f"{last_name}, {first_name}"
            if formatted_name in names:
                print("That student is already listed.")
                continue

            if len(names) >= MAX_CAPACITY:
                print(f"There are only {MAX_CAPACITY} seats available.")
                break

            names.append(formatted_name)

        if not names:
            print("Please enter at least one student name.")
            continue

        return names


def get_student_genders(names):
    print("\nEnter each student's gender.")
    print("Use boy/girl, male/female, or non-binary.")
    print("Each table will still be required to include at least one boy and one girl.")

    genders = {}
    for name in names:
        while True:
            raw_gender = input(f"{name}: ").strip().lower()
            gender = normalize_gender(raw_gender)
            if not gender:
                print("Please enter boy, girl, male, female, or non-binary.")
                continue
            genders[name] = gender
            break

    return genders


def load_saved_rosters():
    # Load previously saved rosters if the JSON file exists and is valid.
    if not ROSTER_FILE.exists():
        return {}

    try:
        with ROSTER_FILE.open("r", encoding="utf-8") as roster_file:
            data = json.load(roster_file)
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


def save_saved_rosters(rosters):
    with ROSTER_FILE.open("w", encoding="utf-8") as roster_file:
        json.dump(rosters, roster_file, indent=2)


def prompt_to_save_roster(names, genders, saved_rosters):
    print("\nWould you like to save this roster for later?")
    print("Type y to save it, or press Enter to skip.")

    if input().strip().lower() != "y":
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
        save_saved_rosters(saved_rosters)
        print(f'Saved roster "{roster_name}".')
        return saved_rosters


def choose_or_create_roster():
    # Reuse a saved roster when possible so names and genders do not need to be re-entered.
    saved_rosters = load_saved_rosters()

    while True:
        print("\nRoster Menu")
        print("-" * 30)
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
                    selected_roster = saved_rosters[roster_names[choice_index]]
                    return (
                        selected_roster["names"][:],
                        selected_roster["genders"].copy(),
                        saved_rosters,
                    )

            print("Please choose one of the listed options.")
            continue

        print("No saved rosters found.")
        print("n. Enter a new roster")
        choice = input("Type n to continue: ").strip().lower()
        if choice == "n":
            break
        print("Please type n to enter a new roster.")

    names = get_student_names()
    genders = get_student_genders(names)
    saved_rosters = prompt_to_save_roster(names, genders, saved_rosters)
    return names, genders, saved_rosters


def normalize_gender(raw_gender):
    if raw_gender in {"boy", "male", "m", "b"}:
        return "boy"
    if raw_gender in {"girl", "female", "f", "g"}:
        return "girl"
    if raw_gender in {"non-binary", "nonbinary", "nb"}:
        return "non-binary"
    return None


def get_alternating_ratio():
    print("\nEnter the boy/girl alternation preference ratio.")
    print("Example: 5:1 means prefer alternating 5 times as often as same-gender neighbors.")

    while True:
        raw_ratio = input("Ratio: ").strip()
        parts = [part.strip() for part in raw_ratio.split(":")]
        if len(parts) != 2 or not all(part.isdigit() for part in parts):
            print("Please enter the ratio in the format number:number, such as 5:1.")
            continue

        preferred_count = int(parts[0])
        allowed_count = int(parts[1])
        if preferred_count <= 0 or allowed_count <= 0:
            print("Both parts of the ratio must be greater than 0.")
            continue

        return preferred_count, allowed_count


def total_capacity():
    return MAX_CAPACITY


def get_tables_for_class_size(student_count):
    # Bravo and Delta expand only when the class size requires the extra seats.
    bravo_capacity = 4 if student_count <= 17 else 5
    delta_capacity = 4 if student_count <= 18 else 5
    return {
        "Alpha": {"capacity": 4, "zone": "front", "prefix": "a"},
        "Bravo": {"capacity": bravo_capacity, "zone": "back", "prefix": "b"},
        "Charley": {"capacity": 5, "zone": "back", "prefix": "c"},
        "Delta": {"capacity": delta_capacity, "zone": "front", "prefix": "d"},
    }


def build_name_lookup(names):
    # Support both "Last, First" and "First Last" so later prompts are easier to type.
    name_lookup = {}
    for name in names:
        lower_name = name.lower()
        name_lookup[lower_name] = name

        if "," in name:
            last_name, first_name = [part.strip() for part in name.split(",", 1)]
            first_last = f"{first_name} {last_name}".lower()
            name_lookup[first_last] = name

    return name_lookup


def resolve_student_name(raw_name, name_lookup):
    cleaned_name = raw_name.strip().lower()
    return name_lookup.get(cleaned_name)


def get_cannot_sit_together(names):
    print("\nEnter pairs of students who cannot sit together.")
    print("Use this format: First Last, First Last")
    print("Press Enter on a blank line when you are done.")
    print("Conflicts:")

    name_lookup = build_name_lookup(names)
    conflicts = {name: set() for name in names}

    while True:
        while True:
            pair = input().strip()
            if not pair:
                return conflicts

            parts = [part.strip() for part in pair.split(",", 1)]
            if len(parts) != 2:
                print("Please use the format: First Last, First Last")
                continue

            student_a = resolve_student_name(parts[0], name_lookup)
            student_b = resolve_student_name(parts[1], name_lookup)

            if not student_a or not student_b:
                print("One or both names were not found in the student list. Please retype that pair.")
                continue

            if student_a == student_b:
                print("A student cannot be listed with themselves. Please retype that pair.")
                continue

            conflicts[student_a].add(student_b)
            conflicts[student_b].add(student_a)
            break

    return conflicts


def get_required_seating(names):
    print("\nEnter seating requirements for specific students.")
    print("Examples:")
    print("  Alex Smith, front")
    print("  Jordan Jones, Bravo")
    print("Press Enter on a blank line when you are done.")
    print("Requirements:")

    name_lookup = build_name_lookup(names)
    requirements = {}

    while True:
        entry = input().strip()
        if not entry:
            break

        parts = [part.strip() for part in entry.split(",", 1)]
        if len(parts) != 2:
            print("Please use the format: First Last, front")
            continue

        student = resolve_student_name(parts[0], name_lookup)
        if not student:
            print("That student was not found in the student list.")
            continue

        restriction = parse_requirement(parts[1])
        if not restriction:
            print("Use front, back, Alpha, Bravo, Charley, or Delta.")
            continue

        requirements[student] = restriction

    return requirements


def parse_requirement(raw_requirement):
    cleaned = raw_requirement.strip().lower()

    if cleaned in {"front", "back"}:
        return {"type": "zone", "value": cleaned}

    if cleaned in TABLE_ALIASES:
        return {"type": "table", "value": TABLE_ALIASES[cleaned]}

    return None


def allowed_tables(student, requirements, tables):
    if student not in requirements:
        return list(tables.keys())

    restriction = requirements[student]
    if restriction["type"] == "table":
        return [restriction["value"]]

    return [
        table_name
        for table_name, details in tables.items()
        if details["zone"] == restriction["value"]
    ]


def can_place(student, table_name, seating_chart, conflicts, tables):
    # A placement is valid only if the table has room and no listed conflict is already there.
    if len(seating_chart[table_name]) >= tables[table_name]["capacity"]:
        return False

    for seated_student in seating_chart[table_name]:
        if seated_student in conflicts[student]:
            return False

    return True


def gender_counts(students_at_table, genders):
    counts = {}
    for student in students_at_table:
        gender = genders[student]
        counts[gender] = counts.get(gender, 0) + 1
    return counts


def table_gender_score(table_name, student, seating_chart, genders):
    students_after_placement = seating_chart[table_name] + [student]
    counts = list(gender_counts(students_after_placement, genders).values())

    if not counts:
        return 0

    return max(counts) - min(counts)


def adjacent_gender_score(table_name, student, seating_chart, genders, alternation_ratio):
    # Prefer alternating boy/girl neighbors, but allow some same-gender adjacency based on the ratio.
    students_at_table = seating_chart[table_name]
    if not students_at_table:
        return 0

    previous_student = students_at_table[-1]
    previous_gender = genders[previous_student]
    current_gender = genders[student]

    if "non-binary" in {previous_gender, current_gender}:
        return 0

    if previous_gender != current_gender:
        return 0

    preferred_count, allowed_count = alternation_ratio
    total_weight = preferred_count + allowed_count
    return 0 if random.randint(1, total_weight) <= allowed_count else 1


def table_has_boy_and_girl(students_at_table, genders):
    if not students_at_table:
        return False

    table_genders = {genders[student] for student in students_at_table}
    return "boy" in table_genders and "girl" in table_genders


def chart_meets_gender_rule(seating_chart, genders):
    for students_at_table in seating_chart.values():
        if not table_has_boy_and_girl(students_at_table, genders):
            return False
    return True


def seat_order_score(students_at_table, genders):
    score = 0
    for index in range(1, len(students_at_table)):
        previous_gender = genders[students_at_table[index - 1]]
        current_gender = genders[students_at_table[index]]
        if "non-binary" in {previous_gender, current_gender}:
            continue
        if previous_gender == current_gender:
            score += 1
    return score


def arrange_table_seats(students_at_table, genders):
    # After table assignment is finished, reshuffle seat order to improve local alternation.
    if len(students_at_table) <= 1:
        return students_at_table[:]

    best_order = None
    best_score = None

    for _ in range(40):
        shuffled_students = students_at_table[:]
        random.shuffle(shuffled_students)
        current_score = seat_order_score(shuffled_students, genders)

        if best_score is None or current_score < best_score:
            best_order = shuffled_students
            best_score = current_score
        elif current_score == best_score and random.choice([True, False]):
            best_order = shuffled_students

    return best_order if best_order is not None else students_at_table[:]


def arrange_all_table_seats(seating_chart, genders):
    arranged_chart = {}
    for table_name, students_at_table in seating_chart.items():
        arranged_chart[table_name] = arrange_table_seats(students_at_table, genders)
    return arranged_chart


def choose_next_student(unseated_students, requirements, seating_chart, conflicts, tables):
    # Pick the most constrained student first so dead ends are found earlier.
    return min(
        unseated_students,
        key=lambda student: (
            len(
                [
                    table_name
                    for table_name in allowed_tables(student, requirements, tables)
                    if can_place(student, table_name, seating_chart, conflicts, tables)
                ]
            ),
            -len(conflicts[student]),
        ),
    )


def solve_seating_chart(names, genders, conflicts, requirements, tables, alternation_ratio):
    # Use backtracking to find a valid table assignment that satisfies the hard rules.
    seating_chart = {table_name: [] for table_name in tables}

    def backtrack(unseated_students):
        if not unseated_students:
            return chart_meets_gender_rule(seating_chart, genders)

        student = choose_next_student(
            unseated_students, requirements, seating_chart, conflicts, tables
        )
        possible_tables = [
            table_name
            for table_name in allowed_tables(student, requirements, tables)
            if can_place(student, table_name, seating_chart, conflicts, tables)
        ]
        random.shuffle(possible_tables)
        possible_tables.sort(
            key=lambda table_name: (
                adjacent_gender_score(
                    table_name,
                    student,
                    seating_chart,
                    genders,
                    alternation_ratio,
                ),
                table_gender_score(table_name, student, seating_chart, genders),
                len(seating_chart[table_name]),
            )
        )

        for table_name in possible_tables:
            seating_chart[table_name].append(student)
            remaining_students = [name for name in unseated_students if name != student]

            if backtrack(remaining_students):
                return True

            seating_chart[table_name].pop()

        return False

    if backtrack(names[:]):
        return arrange_all_table_seats(seating_chart, genders)

    return None


def print_seating_chart(seating_chart, tables):
    print("\nSeating Chart")
    print("-" * 30)

    for table_name, details in tables.items():
        print(f"{table_name} ({details['zone']}, {details['capacity']} seats)")
        if seating_chart[table_name]:
            for seat_number, student in enumerate(seating_chart[table_name], start=1):
                seat_label = f"{details['prefix']}{seat_number}"
                print(f"  {seat_label}: {student}")
        else:
            print("  No one assigned")
        print()


def ask_regeneration_choice():
    print("Type r to regenerate with the same inputs.")
    print("Type ratio to regenerate but change only the ratio.")
    print("Press Enter to finish.")
    return input().strip().lower()


def main():
    print("\nEnglish Class Seating Chart Generator")
    print("Room layout: Alpha and Delta are front tables.")
    print("Bravo and Charley are back tables.")

    names, genders, _saved_rosters = choose_or_create_roster()
    tables = get_tables_for_class_size(len(names))
    alternation_ratio = get_alternating_ratio()
    conflicts = get_cannot_sit_together(names)
    requirements = get_required_seating(names)

    while True:
        seating_chart = solve_seating_chart(
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
            return

        print_seating_chart(seating_chart, tables)

        regeneration_choice = ask_regeneration_choice()
        if regeneration_choice == "r":
            continue
        if regeneration_choice == "ratio":
            alternation_ratio = get_alternating_ratio()
            continue
        if regeneration_choice:
            print("Please type r, ratio, or press Enter.")
            continue
        else:
            return


if __name__ == "__main__":
    main()
