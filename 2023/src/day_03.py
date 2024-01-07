from typing import DefaultDict, Iterable, List, Tuple
import collections

import helpers


def get_neighbors(
    location: Tuple[int, int], max_row_index: int, max_column_index: int
) -> List[Tuple[int, int]]:
    neighbors = []

    for neighbor in [
        (location[0] + 1, location[1]),
        (location[0] - 1, location[1]),
        (location[0], location[1] + 1),
        (location[0], location[1] - 1),
        (location[0] + 1, location[1] + 1),
        (location[0] + 1, location[1] - 1),
        (location[0] - 1, location[1] + 1),
        (location[0] - 1, location[1] - 1),
    ]:
        if neighbor[0] <= max_row_index and neighbor[1] <= max_column_index:
            neighbors.append(neighbor)

    return neighbors


def get_part_numbers_sum(lines: Iterable[str]) -> Tuple[int, int]:
    digit_chars = ""
    digit_locations = set()
    digits = {}
    digit_count: DefaultDict[int, int] = collections.defaultdict(int)

    symbol_locations = []

    max_row_index, max_column_index = 0, 0

    for i, line in enumerate(lines):
        if max_row_index < i:
            max_row_index = i

        for j, char in enumerate(line):
            if max_column_index < j:
                max_column_index = j

            if char.isdigit():
                digit_chars += char
                digit_locations.add((i, j))
                continue

            if digit_chars != "":
                digit = int(digit_chars)
                digits[(digit, digit_count[digit])] = digit_locations
                digit_count[digit] += 1

                digit_chars = ""
                digit_locations = set()

            if char == ".":
                continue

            symbol_locations.append(((i, j), char))

    part_numbers = []
    gear_candidates = collections.defaultdict(list)

    for symbol_location, symbol in symbol_locations:
        for neighbor in get_neighbors(symbol_location, max_row_index, max_column_index):
            is_digit_adjacent = False

            for digit_pair, digit_locations in digits.items():
                if neighbor in digit_locations:
                    is_digit_adjacent = True
                    break

            if is_digit_adjacent:
                part_numbers.append(digit_pair[0])

                if symbol == "*":
                    gear_candidates[symbol_location].append(digit_pair[0])

                del digits[digit_pair]

            if len(digits) == 0:
                break

    gear_ratio_total = 0

    for location, numbers in gear_candidates.items():
        if len(numbers) == 2:
            gear_ratio_total += numbers[0] * numbers[1]

    return sum(part_numbers), gear_ratio_total


if __name__ == "__main__":
    lines = helpers.generate_lines("2023/data/day_03.txt")

    print(get_part_numbers_sum(lines))
