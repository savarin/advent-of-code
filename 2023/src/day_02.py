"""
This module is designed to solve the 'Cube Conundrum' puzzle from the 2023
Advent of Code. It involves analyzing a series of games where different numbers
of colored cubes are drawn from a bag. The tasks include determining which games
are possible given certain limitations on the number of cubes of each color, and
calculating the minimum set of cubes required for each game.

https://adventofcode.com/2023/day/2

Functions:
- convert_to_draws_dict: Converts a string of draws into a dictionary of colors
  and counts.
- verify_within_limits: Checks if the draws are within the specified limits for
  each color.
- validate_line: Validates and extracts information from a line describing a
  game.
- add_valid_games: Sums the IDs of games that are possible within given limits.
- add_set_powers: Calculates the sum of the powers of minimum sets of cubes
  required for each game.
"""

from typing import Dict, Iterable, Tuple

import helpers


# Convert string of cube draws into a dictionary with counts for each color
def convert_to_draws_dict(draws_string: str) -> Dict[str, int]:
    """
    Converts a string representation of cube draws into a dictionary mapping
    cube colors to counts.

    Args:
        draws_string (str): A string representing the cube draws, e.g., '3 red,
        5 green'.

    Returns:
        Dict[str, int]: A dictionary where keys are cube colors and values are
        counts.
    """
    draws = {}

    for item in draws_string.split(", "):
        count, color = item.split(" ")
        draws[color] = int(count)  # Map color to its count

    return draws


# Verify if the draws are within the predefined limits for each color
def verify_within_limits(limits: Dict[str, int], draws: Dict[str, int]) -> bool:
    """
    Verifies whether the number of cubes drawn of each color is within the
    specified limits.

    Args:
        limits (Dict[str, int]): A dictionary mapping cube colors to maximum
        allowed counts.
        draws (Dict[str, int]): A dictionary mapping cube colors to drawn
        counts.

    Returns:
        bool: True if all drawn counts are within limits, False otherwise.
    """
    for k, v in draws.items():
        if v > limits[k]:  # Check if drawn count exceeds the limit for the color
            return False

    return True


# Validate the format of each game line and extract relevant information
def validate_line(line: str) -> Tuple[str, str]:
    """
    Validates the format of a line from the game data and extracts the game
    prefix and draw strings.

    Args:
        line (str): A line from the game data.

    Returns:
        Tuple[str, str]: A tuple containing the game prefix and the string of
        all draws.
    """
    prefix, all_draws_string = line.split(": ")
    assert prefix[:5] == "Game "  # Ensure correct prefix format

    # Check that the rest of the prefix consists of digits
    for char in prefix[5:]:
        assert char.isdigit()

    return prefix, all_draws_string


# Sum the IDs of games that are possible within given cube count limits
def add_valid_games(limits: Dict[str, int], lines: Iterable[str]) -> int:
    """
    Sums the IDs of games that are possible given specific limits on the number
    of cubes of each color.

    Args:
        limits (Dict[str, int]): A dictionary mapping cube colors to maximum
        allowed counts.
        lines (Iterable[str]): An iterable of game data lines.

    Returns:
        int: The sum of IDs of games that are possible within the given limits.
    """
    total = 0
    for line in lines:
        prefix, all_draws_string = validate_line(line)
        game_id = int(prefix[5:])

        is_valid = True  # Flag to track if the game is valid within the limits

        # Process each draw string in the game
        for draws_string in all_draws_string.split("; "):
            if not verify_within_limits(limits, convert_to_draws_dict(draws_string)):
                is_valid = False
                break

        if is_valid:
            total += game_id  # Add game ID to total if valid

    return total


# Calculate the sum of the power of the minimum sets of cubes for each game
def add_set_powers(lines: Iterable[str]) -> int:
    """
    Calculates the sum of the powers of the minimum sets of cubes required for
    each game. The power of a set of cubes is the product of the counts of each
    color of cube.

    Args:
        lines (Iterable[str]): An iterable of game data lines.

    Returns:
        int: The sum of the power of minimum sets of cubes for each game.
    """
    total = 0
    for line in lines:
        prefix, all_draws_string = validate_line(line)
        max_draws_dict: Dict[str, int] = {}  # Track maximum count for each color

        # Process each draw string and update the maximum counts
        for draws_string in all_draws_string.split("; "):
            draws_dict = convert_to_draws_dict(draws_string)
            for k, v in draws_dict.items():
                if k not in max_draws_dict or max_draws_dict[k] < v:
                    max_draws_dict[k] = v  # Update the maximum count for the color

        power = 1  # Initialize power of the set

        # Calculate the power as the product of maximum counts
        for _, v in max_draws_dict.items():
            power *= v

        total += power  # Add the power to the total

    return total


# Main execution point
if __name__ == "__main__":
    # Generate and process lines from the data file
    lines = list(helpers.generate_lines("2023/data/day_02.txt"))

    # Print the sum of IDs of valid games within given limits
    print(add_valid_games({"red": 12, "green": 13, "blue": 14}, lines))

    # Print the sum of powers of minimum sets of cubes for each game
    print(add_set_powers(lines))
