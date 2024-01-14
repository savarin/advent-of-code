from typing import Generator, Iterable, List, Sequence, Tuple

import helpers


def scan_values(lines: Iterable[str]) -> Generator[List[int], None, None]:
    """
    Scans each line of input data and extracts numerical values.

    This function iterates through each line of input, parsing and converting
    the space-separated numerical values into a list of integers. It uses helper
    functions for parsing.

    Args:
        lines (Iterable[str]): An iterable (e.g., list or generator) of strings
        representing each line of the input data.

    Yields:
        Generator[List[int], None, None]: A generator yielding a list of
        integers for each line.
    """
    for line in lines:
        # Initialize line index to start parsing from the beginning of the line
        line_index = 0

        # List to store the parsed integers from the line
        values = []

        # Loop to parse the entire line
        while line_index != len(line):
            # Skip whitespace except at the beginning of the line
            if line_index != 0:
                line_index = helpers.parse_whitespace(line, line_index)

            # Parse digits and update line index
            value, line_index = helpers.parse_digits(line, line_index)

            # Convert parsed value to int and add to list
            values.append(int(value))

        # Yield the list of values for the current line
        yield values


def create_steps(values: Sequence[int]) -> List[Sequence[int]]:
    """
    Creates a list of sequences, each being the difference between consecutive
    values.

    This function takes a sequence of integers and iteratively calculates the
    difference between each pair of consecutive numbers. This process repeats on
    the resulting sequence until a sequence of all zeroes is obtained.

    Args:
        values (Sequence[int]): A sequence of integers representing the initial
        data.

    Returns:
        List[Sequence[int]]: A list of sequences, each derived from the previous
        one by calculating differences between consecutive numbers.
    """
    # Initialize steps with the original sequence
    steps = [values]

    # Loop to create sequences of differences until a sequence of all zeroes is
    # formed
    while True:
        # Get the last sequence of differences
        current_diff = steps[-1]

        # Flag to check if the current sequence is all zeroes
        all_zeroes = True

        # Check if the current sequence is all zeroes
        for value in current_diff:
            if value != 0:
                all_zeroes = False
                break

        # Break the loop if a sequence of all zeroes is found
        if all_zeroes:
            break

        # List to store the next sequence of differences
        next_diff = []

        # Calculate the difference between consecutive numbers
        for i in range(1, len(current_diff)):
            next_diff.append(current_diff[i] - current_diff[i - 1])

        # Add the new sequence to the list of steps
        steps.append(next_diff)

    # Return the list of sequences
    return steps


def extrapolate_next_value(values: Sequence[int]) -> Tuple[int, int]:
    """
    Extrapolates the next value and the prior value based on the sequences of
    differences.

    This function calculates the next value in the original sequence by summing
    the last elements of the decreasing sequences. It also calculates the prior
    value using a similar approach with the first elements.

    Args:
        values (Sequence[int]): The original sequence of integers.

    Returns
        Tuple[int, int]: A tuple where the first element is the extrapolated
        next value in the sequence, and the second element is the extrapolated
        prior value.
    """
    # Generate sequences of differences
    steps = create_steps(values)

    # Initialize the variable for the next extrapolated value
    next_value = 0

    # List to keep track of the starting values for prior extrapolation
    prior_starts = [0]

    # Loop backwards through the sequences to calculate the next and prior
    # values
    for i in range(len(steps) - 1, 0, -1):
        # Current sequence of differences
        current_diff = steps[i - 1]

        # Add the last value for next value extrapolation
        next_value += current_diff[-1]

        # Calculate and append the prior start value for extrapolation
        prior_starts.append(current_diff[0] - prior_starts[-1])

    # Return the next extrapolated value and the last prior start value
    return next_value, prior_starts[-1]


if __name__ == "__main__":
    # Read the input file and store the lines in a list
    lines = list(helpers.generate_lines("2023/data/day_09.txt"))

    # Initialize variables for total next and prior values
    next_total, prior_total = 0, 0

    # Process each line of values and sum up the extrapolated next and prior
    # values
    for values in scan_values(lines):
        next_item, prior_item = extrapolate_next_value(values)
        next_total += next_item
        prior_total += prior_item

    print(next_total)
    print(prior_total)
