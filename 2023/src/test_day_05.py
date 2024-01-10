import pytest

import day_05


@pytest.fixture
def document() -> str:
    return """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def test_find_min_location_individual(document: str) -> None:
    almanac, seeds = day_05.init_almanac(document.split("\n"))
    min_location, min_seed = day_05.find_min_location_individual(almanac, seeds)

    assert min_location == 35
    assert min_seed == 13


def test_find_min_location_range(document: str) -> None:
    almanac, seeds = day_05.init_almanac(document.split("\n"))
    min_location, min_seed = day_05.find_min_location_range(almanac, seeds)

    assert min_location == 46
    assert min_seed == 82
