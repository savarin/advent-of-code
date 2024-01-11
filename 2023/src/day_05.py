"""
This module is designed to solve the "If You Give A Seed A Fertilizer" puzzle
from the 2023 Advent of Code. It processes an almanac detailing the
transformation of seeds through various stages (soil, fertilizer, etc.) to their
final locations. The goal is to determine the lowest location number that
corresponds to any of the initial seed numbers, considering both individual
seeds and ranges of seeds.

https://adventofcode.com/2023/day/5

Classes:
- Range: Represents a mapping from source category numbers to target category
  numbers.
- Almanac: Aggregates multiple Range instances for different transformation
  stages.

Functions:
- init_almanac(lines): Initializes an Almanac instance from provided input
  lines.
- find_min_location_individual(almanac, seeds): Finds the lowest location for
  individual seeds.
- find_min_location_range(almanac, seeds): Finds the lowest location for a range
  of seeds.
"""

from typing import Dict, List, Optional, Iterable, Tuple
import dataclasses

import helpers


# Define a dataclass to represent the transformation range from one category to another
@dataclasses.dataclass
class Range:
    source: str
    target: str

    def __post_init__(self) -> None:
        self.dictionary: Dict[Tuple[int, int], int] = {}


# Define a dataclass to represent the Almanac, which holds all transformation ranges
@dataclasses.dataclass
class Almanac:
    def __post_init__(self) -> None:
        # Initialize a dictionary to hold Range objects for each transformation
        self.dictionaries: Dict[str, Range] = {}

    # Initialize a dictionary for a specific source-to-target transformation
    def init_dictionary(self, source: str, target: str) -> None:
        self.dictionaries[source] = Range(source, target)

    # Update the dictionary for a source category with new range mapping data
    def update_dictionary(
        self, source: str, source_start: int, target_start: int, size: int
    ) -> None:
        self.dictionaries[source].dictionary[
            (source_start, source_start + size)
        ] = target_start

    # Fill gaps in the dictionary for a source category
    def fill_dictionary(self, source: str) -> None:
        keys = sorted(self.dictionaries[source].dictionary.keys())
        source_start = 0

        # Iterate over the sorted keys and fill in any gaps in the mapping
        for k, v in keys:
            if source_start < k:
                self.dictionaries[source].dictionary[(source_start, k)] = source_start

            source_start = v

    # Find the target value for a given source value
    def find_target(self, source: str, source_value: int) -> Tuple[int, Optional[int]]:
        for k, v in self.dictionaries[source].dictionary.items():
            if k[0] <= source_value < k[1]:
                return v + source_value - k[0], k[1] - source_value - 1

        return source_value, None


# Initialize an Almanac from a series of input lines
def init_almanac(lines: Iterable[str]) -> Tuple[Almanac, List[int]]:
    seeds: List[int] = []
    almanac = Almanac()

    item_counter = 0

    # Process each line to build the almanac and seed list
    for line in lines:
        if len(line) == 0:
            item_counter += 1
            continue

        line_index = 0

        # Use a state machine to process different sections of the input
        while line_index < len(line):
            match item_counter:
                case 0:
                    # Expect and process the line starting with "seeds:"
                    line_index = helpers.expect(line, line_index, "seeds:")
                    item_counter += 1

                case 1:
                    # Process lines containing seed numbers
                    line_index = helpers.parse_whitespace(line, line_index)
                    seed, line_index = helpers.parse_digits(line, line_index)
                    seeds.append(int(seed))

                case _:
                    # Process mapping lines
                    if item_counter % 2 == 0:
                        # Initialize dictionary for new source-target pair
                        assert line.endswith(" map:")
                        source, target = line[:-5].split("-to-")

                        almanac.init_dictionary(source, target)
                        item_counter += 1
                        break

                    # Process and update dictionary with mapping data
                    target_start, line_index = helpers.parse_digits(line, line_index)
                    line_index = helpers.parse_whitespace(line, line_index)
                    source_start, line_index = helpers.parse_digits(line, line_index)
                    line_index = helpers.parse_whitespace(line, line_index)
                    size, line_index = helpers.parse_digits(line, line_index)

                    almanac.update_dictionary(
                        source, int(source_start), int(target_start), int(size)
                    )

    return almanac, seeds


# Find the minimum location number for individual seeds
def find_min_location_individual(almanac: Almanac, seeds: List[int]) -> Tuple[int, int]:
    min_seed, min_location = None, None

    # Iterate over each seed to find the one with the minimum location number
    for i, seed in enumerate(seeds):
        source = "seed"
        value = seed

        target = None

        # Transform the seed through each category until the final location is reached
        while target != "location":
            target = almanac.dictionaries[source].target
            value, _ = almanac.find_target(source, value)
            source = target

        # Update the minimum location and corresponding seed if a new minimum is found
        if min_location is None or min_location > value:
            min_location = value
            min_seed = seed

    assert min_location is not None and min_seed is not None
    return min_location, min_seed


# Find the minimum location number for a range of seeds
def find_min_location_range(almanac: Almanac, seeds: List[int]) -> Tuple[int, int]:
    min_seed, min_location = None, None

    # Fill gaps in the dictionaries to optimize the search
    for k in almanac.dictionaries:
        almanac.fill_dictionary(k)

    # Process each range of seeds
    for i in range(0, len(seeds), 2):
        skip_count = 0

        # Iterate over each seed in the range
        for j in range(seeds[i], seeds[i] + seeds[i + 1]):
            if skip_count > 0:
                skip_count -= 1
                continue

            assert skip_count == 0

            sizes = []
            source = "seed"
            value = j

            target = None

            # Transform the seed through each category until the final location is reached
            while target != "location":
                target = almanac.dictionaries[source].target
                value, size = almanac.find_target(source, value)
                source = target
                sizes.append(size if size is not None else 0)

            # Update the minimum location and corresponding seed if a new minimum is found
            if min_location is None or min_location > value:
                min_location = value
                min_seed = j

            # Skip over seeds that fall within the already checked range
            skip_count = min(sizes)

    assert min_location is not None and min_seed is not None
    return min_location, min_seed


if __name__ == "__main__":
    # Read input lines, initialize the almanac and seed list, and find the minimum locations
    lines = helpers.generate_lines("2023/data/day_05.txt")
    almanac, seeds = init_almanac(lines)

    print(find_min_location_individual(almanac, seeds))
    print(find_min_location_range(almanac, seeds))
