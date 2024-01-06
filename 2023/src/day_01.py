from typing import List, Iterable, Optional

from . import helpers


def get_first_number(string: str) -> Optional[str]:
    for char in string:
        if char.isdigit():
            return char

    return None


def get_last_number(string: str) -> Optional[str]:
    for char in string[::-1]:
        if char.isdigit():
            return char

    return None


def combine_numbers_simple(line: str) -> int:
    first_number = get_first_number(line)
    last_number = get_last_number(line)
    number = (first_number or "") + (last_number or "")

    return int(number) if number != "" else 0


def get_calibration_values_simple(lines: Iterable[str]) -> int:
    total = 0

    for line in lines:
        total += combine_numbers_simple(line)

    return total


def is_substring_equal_word(string: str, word: str, index: int) -> Optional[str]:
    if index + len(word) > len(string):
        return None

    elif string[index : index + len(word)] == word:
        return word

    return None


def get_numbers(line: str) -> List[str]:
    numbers = []

    for i, char in enumerate(line):
        if char.isdigit():
            numbers.append(char)

        elif char == "o" and is_substring_equal_word(line, "ne", i + 1):
            numbers.append("1")

        elif char == "t":
            if is_substring_equal_word(line, "wo", i + 1):
                numbers.append("2")

            elif is_substring_equal_word(line, "hree", i + 1):
                numbers.append("3")

        elif char == "f":
            if is_substring_equal_word(line, "our", i + 1):
                numbers.append("4")

            elif is_substring_equal_word(line, "ive", i + 1):
                numbers.append("5")

        elif char == "s":
            if is_substring_equal_word(line, "ix", i + 1):
                numbers.append("6")

            elif is_substring_equal_word(line, "even", i + 1):
                numbers.append("7")

        elif char == "e" and is_substring_equal_word(line, "ight", i + 1):
            numbers.append("8")

        elif char == "n" and is_substring_equal_word(line, "ine", i + 1):
            numbers.append("9")

    return numbers


def combine_numbers_composite(line: str) -> int:
    numbers = get_numbers(line)

    if len(numbers) == 0:
        return 0

    return int(numbers[0] + numbers[-1])


def get_calibration_values_composite(lines: Iterable[str]) -> int:
    total = 0

    for line in lines:
        total += combine_numbers_composite(line)

    return total


if __name__ == "__main__":
    filename = "2023/data/day_01.txt"

    print(get_calibration_values_simple(helpers.generate_lines(filename)))
    print(get_calibration_values_composite(helpers.generate_lines(filename)))
