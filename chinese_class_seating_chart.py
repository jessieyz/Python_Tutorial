import json
import random
from pathlib import Path


TABLE_COUNT = 7
SEATS_PER_TABLE = 2
MAX_CAPACITY = TABLE_COUNT * SEATS_PER_TABLE
# Save Chinese class rosters in a file next to this script.
ROSTER_FILE = Path(__file__).with_name("chinese_class_rosters.json")


def get_student_names():
    # Keep asking until at least one valid student name is entered.
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


def normalize_gender(raw_gender):
    # Convert several common inputs to one consistent label.
    cleaned = raw_gender.strip().lower()
    if cleaned in {"girl", "female", "f", "g"}:
        return "girl"
    if cleaned in {"boy", "male", "m", "b"}:
        return "boy"
    return None


def get_student_genders(names):
    # Ask for a gender label for every student in the roster.
    print("\nEnter each student's gender.")
    print("Use girl/female or boy/male.")

    genders = {}
    for name in names:
        while True:
            raw_gender = input(f"{name}: ")
            gender = normalize_gender(raw_gender)
            if gender is None:
                print("Please enter girl, female, boy, or male.")
                continue

            genders[name] = gender
            break

    return genders


def load_saved_rosters():
    # Ignore missing or broken roster files and fall back to no saved rosters.
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
    # Write all saved rosters back to the JSON file.
    with ROSTER_FILE.open("w", encoding="utf-8") as roster_file:
        json.dump(rosters, roster_file, indent=2)


def prompt_to_save_roster(names, genders, saved_rosters):
    # Offer to save a newly entered roster so it can be reused later.
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
    # Show saved rosters first so the user can reuse a class list quickly.
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
    prompt_to_save_roster(names, genders, saved_rosters)
    return names, genders


def get_gender_preference_ratio():
    # Read a ratio that controls how strongly different-gender vssame-gender seating is preferred.
    print("\nEnter the different-gender to same-gender seating preference ratio.")
    print("Example: 5:1 means prefer different-gender seating 5 times as much.")

    while True:
        raw_ratio = input("Ratio: ").strip()
        parts = [part.strip() for part in raw_ratio.split(":")]

        if len(parts) != 2 or not all(part.isdigit() for part in parts):
            print("Please enter the ratio in the format number:number, such as 5:1.")
            continue

        different_gender_weight = int(parts[0])
        same_gender_weight = int(parts[1])

        if different_gender_weight <= 0 or same_gender_weight <= 0:
            print("Both numbers must be greater than 0.")
            continue

        return different_gender_weight, same_gender_weight


def count_same_gender_tables(order, genders):
    # Count how many full two-seat tables have the same gender in both seats.
    count = 0
    for index in range(0, len(order), SEATS_PER_TABLE):
        pair = order[index:index + SEATS_PER_TABLE]
        if len(pair) < 2:
            continue
        if genders[pair[0]] == genders[pair[1]]:
            count += 1
    return count


def count_same_gender_neighbors(order, genders):
    # Count same-gender neighbors across the whole row of seats.
    score = 0
    for index in range(1, len(order)):
        if genders[order[index - 1]] == genders[order[index]]:
            score += 1
    return score


def weighted_penalty(same_count, different_count, preference_ratio):
    # Lower scores are better. The ratio controls whether same-gender or different-gender pairings are rewarded more strongly.
    different_gender_weight, same_gender_weight = preference_ratio
    return (same_count * different_gender_weight) - (different_count * same_gender_weight)


def build_preferred_pattern(order, genders):
    # Show the gender pattern of the chosen seating order seat by seat.
    return [genders[student] for student in order]


def generate_best_order(names, genders, preference_ratio, attempts=3000):
    # Try many random seat orders and keep the one with the best score.
    best_order = None
    best_score = None

    for _ in range(attempts):
        order = names[:]
        random.shuffle(order)

        # Score each random arrangement by table pairings first, then by neighboring seats across the full row.
        same_table_count = count_same_gender_tables(order, genders)
        occupied_table_count = len(order) // SEATS_PER_TABLE
        different_table_count = occupied_table_count - same_table_count
        adjacent_same_gender_count = count_same_gender_neighbors(order, genders)
        adjacent_different_gender_count = max(len(order) - 1 - adjacent_same_gender_count, 0)
        current_score = (
            weighted_penalty(same_table_count, different_table_count, preference_ratio),
            weighted_penalty(
                adjacent_same_gender_count,
                adjacent_different_gender_count,
                preference_ratio,
            ),
            random.random(),
        )

        if best_score is None or current_score < best_score:
            best_order = order[:]
            best_score = current_score

            # Stop early if the current order already satisfies both table-level and row-level preferences well enough.
            if current_score[0] <= 0 and current_score[1] <= 0:
                break
        elif current_score == best_score and random.choice([True, False]):
            # Break ties randomly so the mismatch does not always land in the same place.
            best_order = order[:]

    return best_order, build_preferred_pattern(best_order, genders)


def build_seating_chart(order):
    # Seat numbers run left to right across the row: 1-2 at table 1, 3-4 at table 2, and so on.
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


def format_target_pattern(target_pattern):
    # Turn the chosen gender pattern into a readable seat-by-seat label.
    return " | ".join(
        f"{index + 1}: {target_pattern[index].title()}"
        for index in range(len(target_pattern))
    )


def print_row_view(seating_chart):
    # Print all seven tables as a single left-to-right row.
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
    # Print each table on its own so individual seat assignments are easy to read.
    print("\nDetailed Seating Chart")
    print("-" * 30)

    for table in seating_chart:
        first_seat = table["seats"][0]["seat_number"]
        last_seat = table["seats"][-1]["seat_number"]
        print(f"Table {table['table']} (Seats {first_seat}-{last_seat})")
        for seat in table["seats"]:
            print(f"  Seat {seat['seat_number']}: {seat['student']}")
        print()


def explain_preferences(order, genders, preference_ratio):
    # Summarize how the chosen chart matches the user's ratio preference.
    same_table_count = count_same_gender_tables(order, genders)
    occupied_table_count = len(order) // SEATS_PER_TABLE
    different_table_count = occupied_table_count - same_table_count
    adjacent_repeat_count = count_same_gender_neighbors(order, genders)
    adjacent_different_count = max(len(order) - 1 - adjacent_repeat_count, 0)
    different_gender_weight, same_gender_weight = preference_ratio

    print("Preference Check")
    print("-" * 30)
    print(
        "Different-gender to same-gender preference ratio: "
        f"{different_gender_weight}:{same_gender_weight}"
    )
    print(f"Different-gender tables: {different_table_count}")
    print(f"Same-gender tables: {same_table_count}")
    print(f"Same-gender neighbors in row: {adjacent_repeat_count}")
    print(f"Different-gender neighbors in row: {adjacent_different_count}")

    if different_gender_weight > same_gender_weight:
        print("This chart leans toward different-gender seating.")
    elif same_gender_weight > different_gender_weight:
        print("This chart leans toward same-gender seating.")
    else:
        print("This chart balances different-gender and same-gender seating evenly.")


def ask_next_action():
    # Let the user either reroll the chart, change only the ratio, or finish.
    print("\nNext step:")
    print("  r = regenerate with the same ratio")
    print("  c = change only the ratio and regenerate")
    print("  Press Enter to finish")
    return input("Choice: ").strip().lower()


def main():
    # Main program flow: choose a roster, choose a ratio, then keep generating charts until the user decides to stop.
    print("\nChinese Class Seating Chart Generator")
    print(f"Room layout: {TABLE_COUNT} tables in one row, {SEATS_PER_TABLE} seats at each table.")
    print("Preference: alternate girl and boy as much as possible across the row.\n")

    names, genders = choose_or_create_roster()
    preference_ratio = get_gender_preference_ratio()

    while True:
        order, target_pattern = generate_best_order(names, genders, preference_ratio)
        seating_chart = build_seating_chart(order)

        print("\nPreferred row pattern by seat:")
        print(format_target_pattern(target_pattern))
        print_row_view(seating_chart)
        print_detailed_chart(seating_chart)
        explain_preferences(order, genders, preference_ratio)

        next_action = ask_next_action()
        if next_action == "r":
            continue
        if next_action == "c":
            preference_ratio = get_gender_preference_ratio()
            continue
        if next_action:
            print("Finishing because that option was not recognized.")
            break
        break


if __name__ == "__main__":
    main()
