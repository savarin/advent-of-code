"""
This module provides solutions for the Advent of Code 2023 "Day 1: Trebuchet?!"
problem. The challenge involves processing a calibration document where each
line originally contained a specific calibration value. The task is to recover
these values despite modifications by a young Elf. The solution involves two
parts: the first part combines the first and last digits found on each line to
form a calibration value, while the second part accounts for digits spelled out
with letters.

https://adventofcode.com/2023/day/1

Functions:
- get_first_number: Finds the first digit in a string.
- get_last_number: Finds the last digit in a string.
- combine_numbers_simple: Combines the first and last digits found in a string.
- get_calibration_values_simple: Calculates the sum of calibration values for
  simple number combinations.
- is_substring_equal_word: Checks if a substring in a string matches a given
  word.
- get_numbers: Extracts digits and spelled-out numbers from a string.
- combine_numbers_composite: Combines the first and last 'numbers' (digit or
  spelled-out) in a string.
- get_calibration_values_composite: Calculates the sum of calibration values for
  composite number combinations.
"""

from typing import List, Iterable, Optional

import helpers


# Finds the first digit in a string
def get_first_number(string: str) -> Optional[str]:
    """
    Finds the first digit in a string.

    Args:
        string (str): The string to search.

    Returns:
        Optional[str]: The first digit found as a string, or None if no digit is
        found.
    """
    for char in string:
        if char.isdigit():
            return char

    return None


# Finds the last digit in a string
def get_last_number(string: str) -> Optional[str]:
    """
    Finds the last digit in a string.

    Args:
        string (str): The string to search.

    Returns:
        Optional[str]: The last digit found as a string, or None if no digit is
        found.
    """
    for char in string[::-1]:  # Iterate in reverse
        if char.isdigit():
            return char

    return None


# Combines first and last digits found in a string into an integer
def combine_numbers_simple(line: str) -> int:
    """
    Combines the first and last digits found in a string to form an integer.

    Args:
        line (str): The string to process.

    Returns:
        int: The combined integer, or 0 if no digits are found.
    """
    first_number = get_first_number(line)
    last_number = get_last_number(line)
    number = (first_number or "") + (last_number or "")  # Concatenate digits

    return int(number) if number != "" else 0


# Calculates the sum of simple calibration values from lines
def get_calibration_values_simple(lines: Iterable[str]) -> int:
    """
    Calculates the sum of calibration values, each determined by combining the
    first and last digit found on each line.

    Args:
        lines (Iterable[str]): A series of strings representing lines from the
        calibration document.

    Returns:
        int: The sum of calibration values.
    """
    total = 0

    for line in lines:
        total += combine_numbers_simple(line)

    return total


# Checks if a substring in a string matches a given word
def is_substring_equal_word(string: str, word: str, index: int) -> Optional[str]:
    """
    Checks if a substring in a string, starting at a given index, matches a
    given word.

    Args:
        string (str): The string to search in.
        word (str): The word to match.
        index (int): The starting index for the substring.

    Returns:
        Optional[str]: The word if a match is found, otherwise None.
    """
    if index + len(word) > len(string):
        return None

    elif string[index : index + len(word)] == word:
        return word

    return None


# Extracts digits and spelled-out numbers from a string
def get_numbers(line: str) -> List[str]:
    """
    Extracts digits and spelled-out numbers from a string, converting them into
    their digit equivalents.

    Args:
        line (str): The string to process.

    Returns:
        List[str]: A list of strings, each representing a digit found in the
        string.
    """
    numbers = []
    for i, char in enumerate(line):
        # Process based on the first character of spelled-out numbers
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


# Combines first and last 'numbers' (digit or spelled-out) in a string
def combine_numbers_composite(line: str) -> int:
    """
    Combines the first and last 'numbers' found in a string, where a 'number'
    can be a digit or a spelled-out number.

    Args:
        line (str): The string to process.

    Returns:
        int: The combined integer formed from the first and last numbers, or 0
        if no numbers are found.
    """
    numbers = get_numbers(line)

    if len(numbers) == 0:
        return 0

    return int(numbers[0] + numbers[-1])


# Calculates the sum of composite calibration values from lines
def get_calibration_values_composite(lines: Iterable[str]) -> int:
    """
    Calculates the sum of calibration values for the composite case, where each
    calibration value is determined by combining the first and last 'number'
    found on each line.

    Args:
        lines (Iterable[str]): A series of strings representing lines from the
        calibration document.

    Returns:
        int: The sum of composite calibration values.
    """
    total = 0

    for line in lines:
        total += combine_numbers_composite(line)

    return total


# Main execution block
if __name__ == "__main__":
    # Read lines from the calibration document
    lines = list(helpers.generate_lines("2023/data/day_01.txt"))

    # Print the total calibration values for both simple and composite cases
    print(get_calibration_values_simple(lines))
    print(get_calibration_values_composite(lines))
