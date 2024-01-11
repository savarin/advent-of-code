"""
This module addresses the 'Gear Ratios' problem from the 2023 Advent of Code. It
involves analyzing an engine schematic represented as a grid of numbers and
symbols. The primary tasks are to compute the sum of part numbers adjacent to
symbols and to determine the sum of gear ratios, where gears are represented by
'*' symbols adjacent to exactly two part numbers.

Functions:
- get_neighbors: Determines the adjacent locations to a given grid location.
- get_part_numbers_sum: Calculates the sum of part numbers and the sum of gear
  ratios as specified in the engine schematic.
"""

from typing import DefaultDict, Iterable, List, Tuple
import collections

import helpers


# Function to get neighboring cells of a grid location
def get_neighbors(
    location: Tuple[int, int], max_row_index: int, max_column_index: int
) -> List[Tuple[int, int]]:
    neighbors = []

    # Calculate the 8 possible neighbors (including diagonals) for the given
    # location
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
        # Include the neighbor if it's within the bounds of the grid
        if neighbor[0] <= max_row_index and neighbor[1] <= max_column_index:
            neighbors.append(neighbor)

    return neighbors


# Main function to process the schematic and calculate sums
def get_part_numbers_sum(lines: Iterable[str]) -> Tuple[int, int]:
    """
    Processes the engine schematic to calculate the sum of part numbers and gear
    ratios.

    Part numbers are adjacent to symbols in the schematic. Gear ratios are
    calculated for gears, represented by '*' and adjacent to exactly two part
    numbers. The function returns a tuple containing the sum of part numbers and
    the sum of gear ratios.

    Args:
        lines (Iterable[str]): Lines of the engine schematic.

    Returns:
        Tuple[int, int]: Sum of part numbers and sum of gear ratios.
    """

    # Collect in dictionary digit-count as key and locations as values
    # Example:
    #   {(467, 0): [(0, 0), (0, 1), (0, 2)] denotes the first value of 467 at
    #   the locations (0, 0), (0, 1) and (0, 2)
    digit_chars = ""
    digit_locations = set()
    digits = {}
    digit_count: DefaultDict[int, int] = collections.defaultdict(int)

    # Collect in list tuples representing part location and part character
    # Example:
    #   [((1, 3), *)] denotes * at location (1, 3)
    symbol_locations = []

    max_row_index, max_column_index = 0, 0

    # Process each line of the schematic
    for i, line in enumerate(lines):
        max_row_index = max(max_row_index, i)

        for j, char in enumerate(line):
            max_column_index = max(max_column_index, j)

            # Collect digits and their locations
            if char.isdigit():
                digit_chars += char
                digit_locations.add((i, j))
                continue

            # Store digit sequences as part numbers
            if digit_chars != "":
                digit = int(digit_chars)
                digits[(digit, digit_count[digit])] = digit_locations
                digit_count[digit] += 1

                digit_chars = ""
                digit_locations = set()

            # Skip dots as they are not part of part numbers or symbols
            if char == ".":
                continue

            # Collect symbol locations for later processing
            symbol_locations.append(((i, j), char))

    part_numbers = []

    # Collect in dictionary asterisk location as key and part numbers as values
    # Example:
    #   {(1, 3): [467, 35]} denotes asterisk at location (1, 3) having adjacent
    #   part numbers 467 and 35
    gear_candidates = collections.defaultdict(list)

    # Process each symbol to identify part numbers and gears
    for symbol_location, symbol in symbol_locations:
        for neighbor in get_neighbors(symbol_location, max_row_index, max_column_index):
            is_digit_adjacent = False

            # Check if the neighbor is adjacent to a digit
            for digit_pair, digit_locations in digits.items():
                if neighbor in digit_locations:
                    is_digit_adjacent = True
                    break

            # Update part numbers and gear candidates
            if is_digit_adjacent:
                part_numbers.append(digit_pair[0])

                if symbol == "*":
                    gear_candidates[symbol_location].append(digit_pair[0])

                del digits[digit_pair]

            # Break if all digits are processed
            if len(digits) == 0:
                break

    # Calculate the total gear ratio
    gear_ratio_total = 0

    for location, numbers in gear_candidates.items():
        if len(numbers) == 2:
            gear_ratio_total += numbers[0] * numbers[1]

    # Return the sum of part numbers and the total gear ratio
    return sum(part_numbers), gear_ratio_total


# Entry point for running the program
if __name__ == "__main__":
    # Read and process lines from the data file
    lines = helpers.generate_lines("2023/data/day_03.txt")

    # Print the results of the calculation
    print(get_part_numbers_sum(lines))
