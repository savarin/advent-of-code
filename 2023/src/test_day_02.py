import pytest

import day_02


@pytest.fixture
def document() -> str:
    return """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


def test_add_valid_games(document: str) -> None:
    limits = {"red": 12, "green": 13, "blue": 14}
    assert day_02.add_valid_games(limits, document.split("\n")) == 8


def test_add_set_powers(document: str) -> None:
    assert day_02.add_set_powers(document.split("\n")) == 2286
