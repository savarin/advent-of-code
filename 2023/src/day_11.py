"""
- iterate through all, collecting galaxies and bit flip indices
- go through each galaxy, correcting all locations
- iterate through galaxies finding distances and sum
"""
from typing import Dict, List, Tuple

import helpers


def scan_galaxies(
    lines: List[str],
) -> Tuple[Dict[int, Tuple[int, int]], List[bool], List[bool]]:
    non_empty_rows = [False for _ in range(len(lines))]
    non_empty_columns = [False for _ in range(len(lines[0]))]

    galaxies = {}
    galaxy_count = 0

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                galaxies[galaxy_count] = (i, j)
                galaxy_count += 1

                non_empty_rows[i] = True
                non_empty_columns[j] = True

    return galaxies, non_empty_rows, non_empty_columns


def create_adjustments(
    non_empty_rows: List[bool], non_empty_columns: List[bool]
) -> Tuple[Dict[int, int], Dict[int, int]]:
    row_adjustments, column_adjustments = {}, {}
    row_counter, column_counter = 0, 0

    for i, row_item in enumerate(non_empty_rows):
        row_adjustments[i] = row_counter

        if not row_item:
            row_counter += 1

    for j, column_item in enumerate(non_empty_columns):
        column_adjustments[j] = column_counter

        if not column_item:
            column_counter += 1

    return row_adjustments, column_adjustments


def apply_adjustments(
    galaxies: Dict[int, Tuple[int, int]],
    row_adjustments: Dict[int, int],
    column_adjustments: Dict[int, int],
) -> Dict[int, Tuple[int, int]]:
    for i in range(len(galaxies)):
        row, column = galaxies[i]
        galaxies[i] = (row + row_adjustments[row], column + column_adjustments[column])

    return galaxies


def calculate_distance(location_1: Tuple[int, int], location_2: Tuple[int, int]) -> int:
    row_distance = location_2[0] - location_1[0]
    column_distance = location_2[1] - location_1[1]

    return abs(row_distance) + abs(column_distance)


def sum_distances(galaxies: Dict[int, Tuple[int, int]]) -> int:
    galaxy_count = len(galaxies)
    total_distance = 0

    for i in range(0, galaxy_count):
        for j in range(i + 1, galaxy_count):
            total_distance += calculate_distance(galaxies[i], galaxies[j])

    return total_distance


if __name__ == "__main__":
    lines = list(helpers.generate_lines("2023/data/day_11.txt"))

    galaxies, non_empty_rows, non_empty_columns = scan_galaxies(lines)

    row_adjustments, column_adjustments = create_adjustments(
        non_empty_rows, non_empty_columns
    )

    galaxies = apply_adjustments(galaxies, row_adjustments, column_adjustments)

    total_distance = sum_distances(galaxies)

    print(total_distance)
