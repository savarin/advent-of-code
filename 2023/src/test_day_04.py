from typing import Sequence
import pytest

import day_04


@pytest.fixture
def cards() -> Sequence[day_04.Card]:
    lines = [
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    ]

    return [day_04.parse_card(line) for line in lines]


def test_count_points(cards: Sequence[day_04.Card]) -> None:
    assert day_04.count_points(cards[0]) == 8
    assert day_04.count_points(cards[1]) == 2
    assert day_04.count_points(cards[2]) == 2
    assert day_04.count_points(cards[3]) == 1
    assert day_04.count_points(cards[4]) == 0
    assert day_04.count_points(cards[5]) == 0


def test_count_cards(cards: Sequence[day_04.Card]) -> None:
    assert day_04.count_cards(cards) == 30
