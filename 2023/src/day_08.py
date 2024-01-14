"""
This module is designed to solve the "Haunted Wasteland" problem from the 2023
Advent of Code, Day 8. It includes functions for processing and interpreting a
map of a network of labeled nodes, based on a set of left/right instructions.
The primary challenge involves navigating this network from a starting node to a
destination node, with a special focus on the shortest path and optimal
navigation strategy. The module also tackles an extended challenge of navigating
from multiple starting nodes to their respective destinations simultaneously.

The functions in this module are tailored to parse the map data, identify
navigation instructions, and execute these instructions to traverse the node
network. This involves both single-path navigation and a more complex scenario
where multiple paths are navigated in parallel, adhering to the unique rules of
the puzzle.

https://adventofcode.com/2023/day/8

Functions:
- scan_map(lines): Parses input lines into navigation instructions and node
  connections.
- follow_directions_single(instructions, directions, start_location, condition):
  Follows instructions from a single node until a specified condition is met.
- follow_directions_multiple(instructions, directions): Determines the required
  steps to reach destination nodes from multiple starting nodes simultaneously.
"""
from typing import Callable, Dict, Iterable, Tuple
import math

import helpers


# Constant defining the length of a location identifier in the map
LOCATION_LENGTH = 3


def scan_map(lines: Iterable[str]) -> Tuple[str, Dict[str, Tuple[str, str]]]:
    """
    Parses the lines of the input map to extract navigation instructions and
    node connections.

    Args:
        lines (Iterable[str]): Iterable of strings, each representing a line in
        the input map.

    Returns:
        Tuple[str, Dict[str, Tuple[str, str]]]: A tuple containing a string of
        instructions and a dictionary where keys are node names and values are
        tuples representing connected nodes (left, right).
    """
    # Counter to track the current section of the map being processed
    section_counter = 0

    # Dictionary to store the connections between nodes
    directions = {}

    for line in lines:
        # Skip empty lines
        if len(line) == 0:
            continue

        match section_counter:
            case 0:
                # First section: Extract navigation instructions
                instructions = line
                section_counter += 1

            case 1:
                # Second section: Parse node connections
                line_index = 0
                key = line[:LOCATION_LENGTH]  # Extract the node name
                line_index += LOCATION_LENGTH

                # Parsing the line to identify connected nodes
                line_index = helpers.parse_whitespace(line, line_index)
                line_index = helpers.expect(line, line_index, "=")
                line_index = helpers.parse_whitespace(line, line_index)
                line_index = helpers.expect(line, line_index, "(")

                # Extract left node
                left = line[line_index : line_index + LOCATION_LENGTH]
                line_index += LOCATION_LENGTH
                line_index = helpers.parse_whitespace(line, line_index)
                line_index = helpers.expect(line, line_index, ",")
                line_index = helpers.parse_whitespace(line, line_index)

                # Extract right node
                right = line[line_index : line_index + LOCATION_LENGTH]
                line_index += LOCATION_LENGTH
                line_index = helpers.expect(line, line_index, ")")

                # Store connections in directions dictionary
                directions[key] = (left, right)

    return instructions, directions


def follow_directions_single(
    instructions: str,
    directions: Dict[str, Tuple[str, str]],
    start_location: str,
    condition: Callable[[str], bool],
) -> int:
    """
    Follows the instructions starting from a single node until a given condition
    is met.

    Args:
        instructions (str): String of navigation instructions (e.g., "LRLL").
        directions (Dict[str, Tuple[str, str]]): Dictionary of node connections.
        start_location (str): The starting node.
        condition (Callable[[str], bool]): A function that returns True if the
        navigation should continue.

    Returns:
        int: Number of steps taken to meet the condition.
    """
    current_location = start_location
    step_counter = 0

    while condition(current_location):
        # Repeat instructions cyclically
        next_direction = instructions[step_counter % len(instructions)]

        # Convert direction to index (0 for left, 1 for right)
        next_index = "LR".index(next_direction)

        # Determine next location
        next_location = directions[current_location][next_index]
        current_location = next_location
        step_counter += 1

    return step_counter


def follow_directions_multiple(
    instructions: str, directions: Dict[str, Tuple[str, str]]
) -> int:
    """
    Follows instructions from all nodes ending with 'A' until they reach nodes
    ending with 'Z'.

    Args:
        instructions (str): String of navigation instructions.
        directions (Dict[str, Tuple[str, str]]): Dictionary of node connections.

    Returns:
        int: The least common multiple of steps taken from all starting nodes to
        reach their destinations.
    """
    # Find all start locations ending with 'A'
    start_locations = [location for location in directions if location[2] == "A"]

    # Calculate the number of steps for each start location
    step_counters = [
        follow_directions_single(
            instructions, directions, location, lambda x: x[2] != "Z"
        )
        for location in start_locations
    ]

    # Return the least common multiple of all step counts
    return math.lcm(*step_counters)


if __name__ == "__main__":
    # Main execution block
    lines = list(helpers.generate_lines("2023/data/day_08.txt"))  # Read input file
    # Parse the map to get instructions and directions
    instructions, directions = scan_map(lines)

    # Print the number of steps required to reach "ZZZ" from "AAA" following the instructions
    print(
        follow_directions_single(instructions, directions, "AAA", lambda x: x != "ZZZ")
    )
    # Print the least common multiple of steps taken from all starting nodes ending with 'A' to reach nodes ending with 'Z'
    print(follow_directions_multiple(instructions, directions))
