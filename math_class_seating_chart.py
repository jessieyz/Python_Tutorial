import json
import random
from pathlib import Path


TABLE_COUNT = 10
SEATS_PER_TABLE = 2
MAX_CAPACITY = TABLE_COUNT * SEATS_PER_TABLE
ROSTER_FILE = Path(__file__).with_name("math_class_rosters.json")


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

        if names:
            return names

        print("Please enter at least one student name.\n")


def format_student_name(raw_name):
    if raw_name.count(",") != 1:
        return None

    last_name, first_name = [part.strip() for part in raw_name.split(",", 1)]
    if not last_name or not first_name:
        return None

    return f"{last_name}, {first_name}"


def build_first_last_lookup(names):
    lookup = {}
    duplicates = set()

    for name in names:
        last_name, first_name = [part.strip() for part in name.split(",", 1)]
        first_last_name = f"{first_name} {last_name}".strip().lower()
        if first_last_name in lookup:
            duplicates.add(first_last_name)
        else:
            lookup[first_last_name] = name

    for duplicate in duplicates:
        lookup.pop(duplicate, None)

    return lookup, duplicates


def parse_pair_input_name(raw_name, first_last_lookup, duplicate_first_last_names):
    cleaned_name = " ".join(raw_name.strip().split())
    if not cleaned_name:
        return None

    first_last_key = cleaned_name.lower()
    if first_last_key in duplicate_first_last_names:
        return "duplicate"

    return first_last_lookup.get(first_last_key)


def normalize_gender(raw_gender):
    cleaned = raw_gender.strip().lower()
    if cleaned in {"girl", "female", "f", "g"}:
        return "girl"
    if cleaned in {"boy", "male", "m", "b"}:
        return "boy"
    if cleaned in {"non-binary", "nonbinary", "nb", "enby"}:
        return "non-binary"
    return None


def get_student_genders(names):
    print("\nEnter each student's gender.")
    print("Use girl/female, boy/male, or non-binary.")

    genders = {}
    for name in names:
        while True:
            raw_gender = input(f"{name}: ")
            gender = normalize_gender(raw_gender)
            if gender is None:
                print("Please enter girl, female, boy, male, or non-binary.")
                continue

            genders[name] = gender
            break

    return genders


def load_saved_rosters():
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


def get_student_pairs(names, prompt_title, prompt_detail):
    print(f"\n{prompt_title}")
    print(prompt_detail)
    print("Enter one pair per line in this format: First Last, First Last")
    print("Press Enter on a blank line when you are done.")

    name_set = set(names)
    first_last_lookup, duplicate_first_last_names = build_first_last_lookup(names)
    pairs = []
    seen_pairs = set()

    while True:
        raw_pair = input("Pair: ").strip()
        if not raw_pair:
            break

        if raw_pair.count(",") != 1:
            print("Use the format: First Last, First Last")
            continue

        raw_left, raw_right = [part.strip() for part in raw_pair.split(",", 1)]
        left_name = parse_pair_input_name(
            raw_left,
            first_last_lookup,
            duplicate_first_last_names,
        )
        right_name = parse_pair_input_name(
            raw_right,
            first_last_lookup,
            duplicate_first_last_names,
        )

        if left_name is None or right_name is None:
            print("Both names must match students in the class list using First Last format.")
            continue

        if left_name == "duplicate" or right_name == "duplicate":
            print("That First Last name matches more than one student in the class list.")
            continue

        if left_name == right_name:
            print("A student cannot be paired with themself.")
            continue

        if left_name not in name_set or right_name not in name_set:
            print("Both students must already be in the class list.")
            continue

        pair_key = tuple(sorted((left_name, right_name)))
        if pair_key in seen_pairs:
            print("That pair is already listed.")
            continue

        seen_pairs.add(pair_key)
        pairs.append(pair_key)

    return pairs


def get_seat_preferences(names):
    print("\nEnter student seat preferences.")
    print("These are soft preferences. The generator will try to honor them, but it may not always be possible.")
    print("Enter one preference per line in this format: First Last, SeatNumber")
    print(f"Seat numbers must be between 1 and {len(names)} for this class list.")
    print("Press Enter on a blank line when you are done.")

    first_last_lookup, duplicate_first_last_names = build_first_last_lookup(names)
    preferences = {}
    used_seats = set()

    while True:
        raw_preference = input("Seat preference: ").strip()
        if not raw_preference:
            break

        if raw_preference.count(",") != 1:
            print("Use the format: First Last, SeatNumber")
            continue

        raw_name, raw_seat = [part.strip() for part in raw_preference.split(",", 1)]
        student_name = parse_pair_input_name(
            raw_name,
            first_last_lookup,
            duplicate_first_last_names,
        )

        if student_name is None:
            print("The student name must match the class list using First Last format.")
            continue

        if student_name == "duplicate":
            print("That First Last name matches more than one student in the class list.")
            continue

        if not raw_seat.isdigit():
            print(f"Seat number must be a whole number from 1 to {len(names)}.")
            continue

        seat_number = int(raw_seat)
        if seat_number < 1 or seat_number > len(names):
            print(f"Seat number must be between 1 and {len(names)} for this class list.")
            continue

        if student_name in preferences:
            print("That student already has a seat preference listed.")
            continue

        if seat_number in used_seats:
            print("That seat already has a different student preference listed.")
            continue

        preferences[student_name] = seat_number
        used_seats.add(seat_number)

    return preferences


def get_gender_preference_ratio():
    print("\nEnter the different-gender to same-gender seating preference ratio.")
    print("Example: 5:1 means prefer different-gender seating 5 times as much.")
    print("Decimals are allowed, such as 2.5:1.")

    while True:
        raw_ratio = input("Ratio: ").strip()
        parts = [part.strip() for part in raw_ratio.split(":")]

        if len(parts) != 2:
            print("Please enter the ratio in the format number:number, such as 5:1.")
            continue

        try:
            different_gender_weight = float(parts[0])
            same_gender_weight = float(parts[1])
        except ValueError:
            print("Please enter the ratio in the format number:number, such as 5:1.")
            continue

        if different_gender_weight <= 0 or same_gender_weight <= 0:
            print("Both numbers must be greater than 0.")
            continue

        return different_gender_weight, same_gender_weight


def get_left_right_order_ratio():
    print("\nEnter the left-right seat order ratio within each table.")
    print("Example: 1:1 is evenly random, 3:1 favors the current order, 1:3 favors swapping.")
    print("Decimals are allowed, such as 2.5:1.")

    while True:
        raw_ratio = input("Left-right ratio: ").strip()
        parts = [part.strip() for part in raw_ratio.split(":")]

        if len(parts) != 2:
            print("Please enter the ratio in the format number:number, such as 1:1.")
            continue

        try:
            keep_order_weight = float(parts[0])
            swap_order_weight = float(parts[1])
        except ValueError:
            print("Please enter the ratio in the format number:number, such as 1:1.")
            continue

        if keep_order_weight <= 0 or swap_order_weight <= 0:
            print("Both numbers must be greater than 0.")
            continue

        return keep_order_weight, swap_order_weight


def table_balance_score(order, genders):
    score = 0
    for index in range(0, len(order), SEATS_PER_TABLE):
        pair = order[index:index + SEATS_PER_TABLE]
        if len(pair) < 2:
            continue
        if genders[pair[0]] == genders[pair[1]]:
            score += 1
    return score


def pair_table_map(order):
    table_pairs = {}
    for index in range(0, len(order), SEATS_PER_TABLE):
        pair = order[index:index + SEATS_PER_TABLE]
        if len(pair) == SEATS_PER_TABLE:
            table_pairs[tuple(sorted(pair))] = index // SEATS_PER_TABLE + 1
    return table_pairs


def blocked_pair_violations(order, blocked_pairs):
    current_pairs = pair_table_map(order)
    return sum(1 for pair in blocked_pairs if pair in current_pairs)


def preferred_pair_misses(order, preferred_pairs):
    current_pairs = pair_table_map(order)
    return sum(1 for pair in preferred_pairs if pair not in current_pairs)


def preferred_pair_hits(order, preferred_pairs):
    return len(preferred_pairs) - preferred_pair_misses(order, preferred_pairs)


def seat_preference_misses(order, seat_preferences):
    misses = 0
    for student_name, seat_number in seat_preferences.items():
        seat_index = seat_number - 1
        if seat_index >= len(order) or order[seat_index] != student_name:
            misses += 1
    return misses


def seat_preference_hits(order, seat_preferences):
    return len(seat_preferences) - seat_preference_misses(order, seat_preferences)


def target_same_gender_table_count(order, preference_ratio):
    full_table_count = len(order) // SEATS_PER_TABLE
    different_gender_weight, same_gender_weight = preference_ratio
    total_weight = different_gender_weight + same_gender_weight
    return full_table_count * same_gender_weight / total_weight


def table_ratio_score(order, genders, preference_ratio):
    same_table_count = table_balance_score(order, genders)
    target_same_count = target_same_gender_table_count(order, preference_ratio)
    return abs(same_table_count - target_same_count)


def generate_best_order(
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
        current_score = (
            blocked_pair_violations(order, blocked_pairs),
            preferred_pair_misses(order, preferred_pairs),
            seat_preference_misses(order, seat_preferences),
            table_ratio_score(order, genders, preference_ratio),
            random.random(),
        )

        if best_score is None or current_score < best_score:
            best_order = order[:]
            best_score = current_score

    return best_order


def randomize_within_tables(order, left_right_ratio, seat_preferences):
    keep_order_weight, swap_order_weight = left_right_ratio
    randomized_order = []
    for index in range(0, len(order), SEATS_PER_TABLE):
        table_group = order[index:index + SEATS_PER_TABLE]
        if len(table_group) == SEATS_PER_TABLE:
            keep_group = table_group[:]
            swap_group = list(reversed(table_group))
            keep_hits = 0
            swap_hits = 0

            for offset, student_name in enumerate(keep_group):
                seat_number = index + offset + 1
                if seat_preferences.get(student_name) == seat_number:
                    keep_hits += 1

            for offset, student_name in enumerate(swap_group):
                seat_number = index + offset + 1
                if seat_preferences.get(student_name) == seat_number:
                    swap_hits += 1

            if swap_hits > keep_hits:
                table_group = swap_group
            elif keep_hits == swap_hits and random.choices(
                ["keep", "swap"],
                weights=[keep_order_weight, swap_order_weight],
                k=1,
            )[0] == "swap":
                table_group = swap_group

        randomized_order.extend(table_group)

    return randomized_order


def build_seating_chart(order):
    seating_chart = []
    index = 0
    seat_number = 1
    for table_number in range(1, TABLE_COUNT + 1):
        seats = []
        for _ in range(SEATS_PER_TABLE):
            if index < len(order):
                student = order[index]
                index += 1
            else:
                student = "Empty"

            seats.append(
                {
                    "seat_number": seat_number,
                    "student": student,
                }
            )
            seat_number += 1

        seating_chart.append(
            {
                "table": table_number,
                "seats": seats,
            }
        )

    return seating_chart


def print_row_view(seating_chart):
    print("\nTables In One Row")
    print("-" * 110)

    table_labels = []
    seat_rows = []
    for table in seating_chart:
        left_seat = table["seats"][0]
        right_seat = table["seats"][1]
        table_labels.append(
            f"Table {table['table']} ({left_seat['seat_number']}-{right_seat['seat_number']})"
        )
        seat_rows.append(
            f"{left_seat['seat_number']}: {left_seat['student']} / "
            f"{right_seat['seat_number']}: {right_seat['student']}"
        )

    print(" | ".join(table_labels))
    print(" | ".join(seat_rows))


def print_detailed_chart(seating_chart):
    print("\nDetailed Seating Chart")
    print("-" * 30)

    for table in seating_chart:
        first_seat = table["seats"][0]["seat_number"]
        last_seat = table["seats"][-1]["seat_number"]
        print(f"Table {table['table']} (Seats {first_seat}-{last_seat})")
        for seat in table["seats"]:
            print(f"  Seat {seat['seat_number']}: {seat['student']}")
        print()


def explain_preferences(
    order,
    genders,
    preference_ratio,
    left_right_ratio,
    preferred_pairs,
    blocked_pairs,
    seat_preferences,
):
    same_table_count = table_balance_score(order, genders)
    target_same_count = target_same_gender_table_count(order, preference_ratio)
    full_table_count = len(order) // SEATS_PER_TABLE
    target_different_count = full_table_count - target_same_count
    blocked_violations = blocked_pair_violations(order, blocked_pairs)
    preferred_hits = preferred_pair_hits(order, preferred_pairs)
    seat_hits = seat_preference_hits(order, seat_preferences)
    different_gender_weight, same_gender_weight = preference_ratio
    keep_order_weight, swap_order_weight = left_right_ratio

    print("Preference Check")
    print("-" * 30)
    print(
        "Different-gender to same-gender preference ratio: "
        f"{different_gender_weight}:{same_gender_weight}"
    )
    print(f"Same-gender tables: {same_table_count}")
    print(
        "Target mix for filled tables: "
        f"{target_different_count:.1f} different-gender and {target_same_count:.1f} same-gender"
    )
    print(
        "Left-right seat order ratio within each table: "
        f"{keep_order_weight}:{swap_order_weight}"
    )
    print(f"Must-not-sit-together violations: {blocked_violations}")
    print(f"Preferred pairs seated together: {preferred_hits} of {len(preferred_pairs)}")
    print(f"Seat preferences matched: {seat_hits} of {len(seat_preferences)}")

    if blocked_violations == 0 and table_ratio_score(order, genders, preference_ratio) < 1:
        print("This chart is close to the requested different-gender to same-gender table ratio.")
    elif blocked_violations == 0:
        print("This chart avoids blocked pairs and is the best overall match found.")
    else:
        print("Blocked pair requests conflicted with other constraints, so this is the best match found.")


def ask_to_regenerate():
    print("\nType r to regenerate with the same settings.")
    print("Type c to change only the ratios and regenerate.")
    print("Press Enter to finish.")
    return input().strip().lower()


def main():
    print("\nMath Class Seating Chart Generator")
    print(f"Room layout: {TABLE_COUNT} tables in one row, {SEATS_PER_TABLE} seats at each table.")
    print("Preference: mix genders within each table when possible.\n")

    names, genders, _ = choose_or_create_roster()
    preferred_pairs = get_student_pairs(
        names,
        "Enter pairs who would like to sit together.",
        "These are soft preferences. The generator will try to honor them, but it may not always be possible.",
    )
    blocked_pairs = get_student_pairs(
        names,
        "Enter pairs who definitely should not sit together.",
        "These are strong restrictions. The generator will avoid these pairings whenever possible.",
    )
    conflicting_pairs = set(preferred_pairs) & set(blocked_pairs)
    if conflicting_pairs:
        print("\nPairs listed in both sections will be treated as must-not-sit-together only.")
        preferred_pairs = [pair for pair in preferred_pairs if pair not in conflicting_pairs]
    seat_preferences = get_seat_preferences(names)
    preference_ratio = get_gender_preference_ratio()
    left_right_ratio = get_left_right_order_ratio()

    while True:
        best_order = generate_best_order(
            names,
            genders,
            preference_ratio,
            preferred_pairs,
            blocked_pairs,
            seat_preferences,
        )
        displayed_order = randomize_within_tables(
            best_order,
            left_right_ratio,
            seat_preferences,
        )
        seating_chart = build_seating_chart(displayed_order)

        print_row_view(seating_chart)
        print_detailed_chart(seating_chart)
        explain_preferences(
            displayed_order,
            genders,
            preference_ratio,
            left_right_ratio,
            preferred_pairs,
            blocked_pairs,
            seat_preferences,
        )

        next_action = ask_to_regenerate()
        if next_action == "c":
            preference_ratio = get_gender_preference_ratio()
            left_right_ratio = get_left_right_order_ratio()
            continue
        if next_action != "r":
            break


if __name__ == "__main__":
    main()
