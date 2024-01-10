from typing import Dict, List, Optional, Iterable, Tuple
import dataclasses

import helpers


@dataclasses.dataclass
class Range:
    source: str
    target: str

    def __post_init__(self) -> None:
        self.dictionary: Dict[Tuple[int, int], int] = {}


@dataclasses.dataclass
class Almanac:
    def __post_init__(self) -> None:
        self.dictionaries: Dict[str, Range] = {}

    def init_dictionary(self, source: str, target: str) -> None:
        self.dictionaries[source] = Range(source, target)

    def update_dictionary(
        self, source: str, source_start: int, target_start: int, size: int
    ) -> None:
        self.dictionaries[source].dictionary[
            (source_start, source_start + size)
        ] = target_start

    def fill_dictionary(self, source: str) -> None:
        keys = sorted(self.dictionaries[source].dictionary.keys())
        source_start = 0

        for k, v in keys:
            if source_start < k:
                self.dictionaries[source].dictionary[(source_start, k)] = source_start

            source_start = v

    def find_target(self, source: str, source_value: int) -> Tuple[int, Optional[int]]:
        for k, v in self.dictionaries[source].dictionary.items():
            if k[0] <= source_value < k[1]:
                return v + source_value - k[0], k[1] - source_value - 1

        return source_value, None


def init_almanac(lines: Iterable[str]) -> Tuple[Almanac, List[int]]:
    seeds: List[int] = []
    almanac = Almanac()

    item_counter = 0

    for line in lines:
        if len(line) == 0:
            item_counter += 1
            continue

        line_index = 0

        while line_index < len(line):
            match item_counter:
                # Scan line starting with specific word.
                #   seeds:
                case 0:
                    line_index = helpers.expect(line, line_index, "seeds:")
                    item_counter += 1

                # Scan line with digits of indeterminate length.
                #   79 14 55 13
                case 1:
                    line_index = helpers.parse_whitespace(line, line_index)
                    seed, line_index = helpers.parse_digits(line, line_index)
                    seeds.append(int(seed))

                # Scan line with mapping ending with specific word and includes
                # the string '-to-' separating the source and target terms.
                #   seed-to-soil map:
                case _:
                    if item_counter % 2 == 0:
                        assert line.endswith(" map:")
                        source, target = line[:-5].split("-to-")

                        almanac.init_dictionary(source, target)
                        item_counter += 1
                        break

                    # Scan line with exactly 3 digits.
                    #   50 98 2
                    target_start, line_index = helpers.parse_digits(line, line_index)
                    line_index = helpers.parse_whitespace(line, line_index)
                    source_start, line_index = helpers.parse_digits(line, line_index)
                    line_index = helpers.parse_whitespace(line, line_index)
                    size, line_index = helpers.parse_digits(line, line_index)

                    almanac.update_dictionary(
                        source, int(source_start), int(target_start), int(size)
                    )

    return almanac, seeds


def find_min_location_individual(almanac: Almanac, seeds: List[int]) -> Tuple[int, int]:
    min_seed, min_location = None, None

    for i, seed in enumerate(seeds):
        source = "seed"
        value = seed

        target = None

        while target != "location":
            target = almanac.dictionaries[source].target
            value, _ = almanac.find_target(source, value)
            source = target

        if min_location is None or min_location > value:
            min_location = value
            min_seed = seed

    assert min_location is not None and min_seed is not None
    return min_location, min_seed


def find_min_location_range(almanac: Almanac, seeds: List[int]) -> Tuple[int, int]:
    min_seed, min_location = None, None

    # Fill gaps to maximize ability to skip lookups.
    for k in almanac.dictionaries:
        almanac.fill_dictionary(k)

    for i in range(0, len(seeds), 2):
        skip_count = 0

        for j in range(seeds[i], seeds[i] + seeds[i + 1]):
            if skip_count > 0:
                skip_count -= 1
                continue

            assert skip_count == 0

            sizes = []
            source = "seed"
            value = j

            target = None

            while target != "location":
                target = almanac.dictionaries[source].target
                value, size = almanac.find_target(source, value)
                source = target
                sizes.append(size if size is not None else 0)

            if min_location is None or min_location > value:
                min_location = value
                min_seed = j

            # Ensure skip range is the minimum of all contiguous ranges.
            skip_count = min(sizes)

    assert min_location is not None and min_seed is not None
    return min_location, min_seed


if __name__ == "__main__":
    lines = helpers.generate_lines("2023/data/day_05.txt")
    almanac, seeds = init_almanac(lines)

    print(find_min_location_individual(almanac, seeds))
    print(find_min_location_range(almanac, seeds))
