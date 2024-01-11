import pytest

import day_06


@pytest.fixture
def document() -> str:
    return """\
Time:      7  15   30
Distance:  9  40  200"""


def test_count_ways(document: str) -> None:
    times, distances = day_06.scan_race_parameters(document.split("\n"))
    assert times == [7, 15, 30]
    assert distances == [9, 40, 200]

    assert day_06.count_ways(times[0], distances[0]) == 4
    assert day_06.count_ways(times[1], distances[1]) == 8
    assert day_06.count_ways(times[2], distances[2]) == 9
