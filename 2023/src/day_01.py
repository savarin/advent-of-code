from typing import Iterable, Optional

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


def combine_numbers(line: str) -> int:
    first_number = get_first_number(line)
    last_number = get_last_number(line)
    number = (first_number or "") + (last_number or "")

    return int(number) if number != "" else 0


def get_calibration_values(lines: Iterable[str]) -> int:
    total = 0

    for line in lines:
        number = combine_numbers(line)
        total += int(number)

    return total


if __name__ == "__main__":
    print(get_calibration_values(helpers.generate_lines("2023/data/day_01.txt")))
