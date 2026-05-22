from random import randint

import pygal


def parse_die(die_input: str) -> tuple[int, int] | None:
    die_input = die_input.replace(" ", "").lower()

    if "d" not in die_input:
        print("You forgot a 'd'. Please follow the format: d6, 2d6, or 2d4,1d8, etc.")
        return None

    parts: list[str] = die_input.split("d")
    if len(parts) != 2:
        print("Invalid input. Please follow the format: d6, 2d6, or 2d4,1d8 etc.")
        return None

    num, sides = parts[0] or "1", parts[1]
    if not num.isdigit() or not sides.isdigit():
        print("Must use a single 'd' and provide numbers for sides.")
        print("Please follow the format: d6, 2d6, or 2d4,1d8 etc.")
        return None

    num: int = int(num)
    sides: int = int(sides)

    if num < 1:
        print("Number of dice must be 1 or greater.")
        return None
    if 2 > sides or sides > 1000:
        print("Number of sides must be between 2 and 1000.")
        return None

    return (num, sides)


def dice_input() -> list[tuple[int, int]]:
    result = []
    while True:
        print("What're we rolling today? (e.g. d6 or 2d6 or d10,d20)")
        initial_dice_input = input(" >> ")

        dice_input_list: list[str] = initial_dice_input.replace(" ", "").split(",")

        for die in dice_input_list:
            parsed = parse_die(die)
            if parsed is None:
                break
            result.append(parsed)
        else:
            return result


def extract_dice_strings(dice_list: list[tuple[int, int]]) -> str:
    return ", ".join(f"{num}D{sides}" for num, sides in dice_list)


def rolls_input() -> int:
    while True:
        num_rolls = input("How many times are we rolling the di(c)e? (e.g. 1000) >> ")
        if not num_rolls.isdigit():
            print("Please use digits!")
            continue
        return int(num_rolls.strip())


def roll_dice(num_die: int = 1, die_sides: int = 6) -> int:
    """Rolls dice and returns an int."""
    return sum(randint(1, die_sides) for _ in range(num_die))


def create_roll_data(dice: list[tuple[int, int]], num_rolls: int = 1000) -> list[int]:
    """Creates die data -- returns a list of frequencies of number rolls."""
    results: list[int] = []
    for roll_num in range(num_rolls):
        result = 0
        for die in dice:
            result += roll_dice(die[0], die[1])
        results.append(result)

    min_result = sum(num for num, _ in dice)
    max_result = sum(num * sides for num, sides in dice)

    frequencies: list[int] = []
    for value in range(min_result, max_result + 1):
        frequency = results.count(value)
        frequencies.append(frequency)

    return frequencies


def valid_filename(name: str) -> bool:
    return bool(name) and name.isprintable() and " " not in name


def main():
    print("===== Pygal Roll Data SVG Generator Software Program Utility App =====")

    # Get user input and create the roll frequency data
    dice_list: list[tuple[int, int]] = dice_input()
    dice_string: str = extract_dice_strings(dice_list)
    num_rolls: int = rolls_input()
    freq_data: list[int] = create_roll_data(dice_list, num_rolls)

    min_result = sum(num for num, _ in dice_list)
    max_result = sum(num * sides for num, sides in dice_list)

    # Make the histogram with pygal
    hist = pygal.Bar()

    hist.title = f"Results of rolling {dice_string} {num_rolls} times."
    hist.x_title = "Result"
    hist.y_title = "Frequency of Result"

    max_labels = 30
    span = max_result - min_result
    step = max(1, span // max_labels)

    all_labels = list(range(min_result, max_result + 1))
    hist.x_labels = [str(x) for x in all_labels]
    hist.x_labels_major = [str(x) for x in all_labels[::step]]
    hist.show_minor_x_labels = False
    if span > max_labels:
        hist.x_label_rotation = 45

    hist.add(dice_string, freq_data)

    while True:
        filename: str = input("What would you like to name the file? >> ")
        if valid_filename(filename):
            hist.render_to_file(filename + ".svg")
            print(f"Your results have been rendered to: {filename}.svg")
            break
        else:
            print("Please enter a valid filename!")
            continue


if __name__ == "__main__":
    main()
