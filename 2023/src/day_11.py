"""
This module is part of the 2023 Advent of Code Day 11 challenge, titled "Cosmic
Expansion". It is tailored to address a unique space-themed problem, which
involves analyzing a vast cosmic image, delineating galaxies and voids. The
primary objective is to compute the sum of the shortest distances between each
pair of galaxies, taking into account the expansion of the universe that alters
the dimensions of certain rows and columns in the cosmic image.

The functionalities of this module encompass various computational and spatial
analysis techniques. These include identifying galaxy coordinates, adjusting for
cosmic expansion, and calculating distances between galaxies. Specifically, the
module scans input data representing the cosmic image, identifies galaxy
locations, and assesses which rows and columns are subject to cosmic expansion.
Subsequently, it recalculates galaxy coordinates based on this expansion and
computes the total sum of distances between all galaxy pairs, considering the
expanded universe.

The module encapsulates the essence of space exploration and cosmic phenomena,
offering a glimpse into the complexities of cosmic distances and expansion. It
portrays a scenario where the user assists a researcher in analyzing cosmic
data, contributing to the understanding of universe dynamics.

https://adventofcode.com/2023/day/11

Functions:
- scan_galaxies: Scans the input data to identify galaxy locations and non-empty
  rows and columns.
- create_adjustments: Creates adjustment mappings for rows and columns based on
  cosmic expansion.
- apply_adjustments: Applies the cosmic expansion adjustments to the galaxy
  locations.
- calculate_distance: Calculates the Manhattan distance between two galaxy
  locations.
- sum_distances: Calculates the sum of distances between every pair of galaxies.
"""

from typing import Dict, List, Tuple

import helpers


def scan_galaxies(
    lines: List[str],
) -> Tuple[Dict[int, Tuple[int, int]], List[bool], List[bool]]:
    """
    Scans the input data to identify galaxy locations and non-empty rows and
    columns.

    Args:
        lines (List[str]): A list of strings representing the universe, where
        '.' is empty space and '#' is a galaxy.

    Returns:
        Tuple[Dict[int, Tuple[int, int]], List[bool], List[bool]]: A tuple
        containing a dictionary of galaxy locations indexed by galaxy number,
        and two lists indicating non-empty rows and columns.
    """
    # Initialize lists to track non-empty rows and columns.
    non_empty_rows = [False for _ in range(len(lines))]
    non_empty_columns = [False for _ in range(len(lines[0]))]

    galaxies = {}
    galaxy_count = 0

    # Scan each character in the input data.
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                # Mark the location of the galaxy and update the non-empty row
                # and column.
                galaxies[galaxy_count] = (i, j)
                galaxy_count += 1

                non_empty_rows[i] = True
                non_empty_columns[j] = True

    return galaxies, non_empty_rows, non_empty_columns


def create_adjustments(
    non_empty_rows: List[bool], non_empty_columns: List[bool], factor: int = 2
) -> Tuple[Dict[int, int], Dict[int, int]]:
    """
    Creates adjustment mappings for rows and columns based on cosmic expansion.

    Args:
        non_empty_rows (List[bool]): A list indicating non-empty rows.
        non_empty_columns (List[bool]): A list indicating non-empty columns.
        factor (int, optional): The expansion factor for empty rows/columns.
        Defaults to 2.

    Returns:
        Tuple[Dict[int, int], Dict[int, int]]: Two dictionaries mapping original
        row/column indices to their adjusted positions.
    """
    # Initialize dictionaries for row and column adjustments.
    row_adjustments, column_adjustments = {}, {}
    row_counter, column_counter = 0, 0

    # Calculate adjustments for each row.
    for i, row_item in enumerate(non_empty_rows):
        row_adjustments[i] = row_counter

        # Increase the counter for empty rows.
        if not row_item:
            row_counter += factor - 1

    # Calculate adjustments for each column.
    for j, column_item in enumerate(non_empty_columns):
        column_adjustments[j] = column_counter

        # Increase the counter for empty columns.
        if not column_item:
            column_counter += factor - 1

    return row_adjustments, column_adjustments


def apply_adjustments(
    galaxies: Dict[int, Tuple[int, int]],
    row_adjustments: Dict[int, int],
    column_adjustments: Dict[int, int],
) -> Dict[int, Tuple[int, int]]:
    """
    Applies the cosmic expansion adjustments to the galaxy locations.

    Args:
        galaxies (Dict[int, Tuple[int, int]]): A dictionary of galaxy locations
        indexed by galaxy number.
        row_adjustments (Dict[int, int]): A dictionary mapping original row
        indices to their adjusted positions.
        column_adjustments (Dict[int, int]): A dictionary mapping original
        column indices to their adjusted positions.

    Returns:
        Dict[int, Tuple[int, int]]: An updated dictionary of galaxy locations
        accounting for cosmic expansion.
    """
    # Apply adjustments to each galaxy's location.
    for i in range(len(galaxies)):
        row, column = galaxies[i]
        galaxies[i] = (row + row_adjustments[row], column + column_adjustments[column])

    return galaxies


def calculate_distance(location_1: Tuple[int, int], location_2: Tuple[int, int]) -> int:
    """
    Calculates the Manhattan distance between two galaxy locations.

    Args:
        location_1 (Tuple[int, int]): The location of the first galaxy.
        location_2 (Tuple[int, int]): The location of the second galaxy.

    Returns:
        int: The Manhattan distance between the two galaxies.
    """
    # Compute the row and column distances.
    row_distance = location_2[0] - location_1[0]
    column_distance = location_2[1] - location_1[1]

    # Return the sum of the absolute values of the distances.
    return abs(row_distance) + abs(column_distance)


def sum_distances(galaxies: Dict[int, Tuple[int, int]]) -> int:
    """
    Calculates the sum of distances between every pair of galaxies.

    Args:
        galaxies (Dict[int, Tuple[int, int]]): A dictionary of galaxy locations
        indexed by galaxy number.

    Returns:
        int: The sum of the Manhattan distances between each pair of galaxies.
    """
    galaxy_count = len(galaxies)
    total_distance = 0

    # Iterate over each pair of galaxies and sum their distances.
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

    galaxies_1 = apply_adjustments(galaxies.copy(), row_adjustments, column_adjustments)
    print(sum_distances(galaxies_1))

    row_adjustments, column_adjustments = create_adjustments(
        non_empty_rows, non_empty_columns, 1000000
    )

    galaxies_2 = apply_adjustments(galaxies.copy(), row_adjustments, column_adjustments)
    print(sum_distances(galaxies_2))
