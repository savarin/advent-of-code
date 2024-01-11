"""
This module is part of a solution to the "Wait For It" problem from the 2023
Advent of Code. It focuses on analyzing boat race parameters and determining the
number of ways to win a race.

https://adventofcode.com/2023/day/6

Functions:
- scan_race_parameters(lines): Extracts and parses race time and distance data
  from input lines.
- count_ways(time, distance): Computes the number of ways to win a race given
  time and distance.
"""

from typing import Iterable, List, Tuple
import helpers


def scan_race_parameters(lines: Iterable[str]) -> Tuple[List[int], List[int]]:
    """
    Scans and parses input lines to extract race parameters, specifically time
    limits and record distances.

    The function processes lines formatted with 'Time:' and 'Distance:' labels,
    followed by space-separated values. Each value is parsed and stored in
    respective lists.

    Args:
        lines (Iterable[str]): An iterable of strings, each containing race
        parameters.

    Returns:
        Tuple[List[int], List[int]]: Two lists containing the extracted time
        limits and distances.

    Raises:
        AssertionError: If the number of extracted time values doesn't match the
        number of distances.
    """
    section_counter = 0  # Tracks which section (time or distance) is being parsed.
    times, distances = [], []  # Lists to store parsed time and distance values.

    for line in lines:
        line_index = 0  # Tracks the current position within the line.

        while line_index < len(line):
            match section_counter:
                # Process the Time section.
                case 0:
                    if line_index == 0:
                        # Expect the "Time:" label at the start of the line.
                        line_index = helpers.expect(line, line_index, "Time:")
                        continue

                    # Parse the time value and append it to the times list.
                    line_index = helpers.parse_whitespace(line, line_index)
                    time, line_index = helpers.parse_digits(line, line_index)
                    times.append(int(time))

                # Process the Distance section.
                case 1:
                    if line_index == 0:
                        # Expect the "Distance:" label at the start of the line.
                        line_index = helpers.expect(line, line_index, "Distance:")
                        continue

                    # Parse the distance value and append it to the distances
                    # list.
                    line_index = helpers.parse_whitespace(line, line_index)
                    distance, line_index = helpers.parse_digits(line, line_index)
                    distances.append(int(distance))

        section_counter += 1

    # Ensure the number of times matches the number of distances.
    assert len(times) == len(
        distances
    ), "Mismatch in the number of time and distance entries."
    return times, distances


def count_ways(time: int, distance: int) -> int:
    """
    Calculates the number of ways to win a race given the time limit and the
    record distance.

    This function considers all possible durations for holding the button at
    the start of the race and calculates the total distance covered. It counts
    how many of these distances exceed the record distance.

    Args:
        time (int): The total time limit for the race.
        distance (int): The record distance to beat.

    Returns:
        int: The number of ways to win the race by exceeding the record
        distance.
    """
    ways = 0  # Counter for the number of ways to win.

    # Loop over each possible button hold duration.
    for i in range(1, time):
        # Calculate distance covered if the button is held for 'i' milliseconds.
        current_distance = i * (time - i)

        # Count this as a winning way if it exceeds the record distance.
        if current_distance > distance:
            ways += 1

    return ways


if __name__ == "__main__":
    # Load race data from a file and parse it.
    lines = helpers.generate_lines("2023/data/day_06.txt")
    times, distances = scan_race_parameters(lines)

    product = 1  # Variable to hold the product of all winning ways.

    # Calculate the product of winning ways for each race.
    for i in range(len(times)):
        product *= count_ways(times[i], distances[i])

    print(product)  # Print the product for Part One of the problem.

    # Concatenate all times and distances for Part Two of the problem.
    actual_time, actual_distance = (
        "".join(map(str, times)),
        "".join(map(str, distances)),
    )

    # Print the number of winning ways for the concatenated race parameters.
    print(count_ways(int(actual_time), int(actual_distance)))
