from typing import Dict, List, Iterable, Tuple
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

    def find_target(self, source: str, source_value: int) -> int:
        for k, v in self.dictionaries[source].dictionary.items():
            if k[0] <= source_value < k[1]:
                return v + source_value - k[0]

        return source_value


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
                case 0:
                    line_index = helpers.expect(line, line_index, "seeds:")
                    item_counter += 1

                case 1:
                    line_index = helpers.parse_whitespace(line, line_index)
                    seed, line_index = helpers.parse_digits(line, line_index)
                    seeds.append(int(seed))

                case _:
                    if item_counter % 2 == 0:
                        assert line.endswith(" map:")
                        source, target = line[:-5].split("-to-")

                        almanac.init_dictionary(source, target)
                        item_counter += 1
                        break

                    target_start, line_index = helpers.parse_digits(line, line_index)
                    line_index = helpers.parse_whitespace(line, line_index)
                    source_start, line_index = helpers.parse_digits(line, line_index)
                    line_index = helpers.parse_whitespace(line, line_index)
                    size, line_index = helpers.parse_digits(line, line_index)

                    almanac.update_dictionary(
                        source, int(source_start), int(target_start), int(size)
                    )

    return almanac, seeds


def find_min_location(almanac: Almanac, seeds: List[int]) -> Tuple[int, int]:
    min_seed, min_location = None, None

    for seed in seeds:
        source = "seed"
        value = seed

        target = None

        while target != "location":
            target = almanac.dictionaries[source].target
            value = almanac.find_target(source, value)
            source = target

        if min_location is None or min_location > value:
            min_location = value
            min_seed = seed

    assert min_location is not None and min_seed is not None
    return min_location, min_seed


if __name__ == "__main__":
    lines = helpers.generate_lines("2023/data/day_05.txt")
    almanac, seeds = init_almanac(lines)
    min_location, min_seed = find_min_location(almanac, seeds)

    print(min_location, min_seed)
