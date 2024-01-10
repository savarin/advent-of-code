from typing import Dict, List, Iterable, Tuple
import dataclasses

import helpers


@dataclasses.dataclass
class Dictionary:
    source: str
    target: str

    def __post_init__(self) -> None:
        self.dictionary: Dict[int, int] = {}


@dataclasses.dataclass
class Almanac:
    def __post_init__(self) -> None:
        self.dictionaries: Dict[str, Dictionary] = {}

    def init_dictionary(self, source: str, target: str) -> None:
        self.dictionaries[source] = Dictionary(source, target)

    def update_dictionary(
        self, source: str, source_start: int, target_start: int, size: int
    ) -> None:
        for i in range(size):
            print(i)
            self.dictionaries[source].dictionary[source_start + i] = target_start + i


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
            value = almanac.dictionaries[source].dictionary.get(value, value)
            source = target

        if min_location is None or min_location > value:
            min_location = value
            min_seed = seed

    assert min_location is not None and min_seed is not None
    return min_location, min_seed
