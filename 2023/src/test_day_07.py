import pytest

import day_07


@pytest.fixture
def document() -> str:
    return """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def test_calculate_winnings(document: str) -> None:
    assert day_07.calculate_winnings(document.split("\n"), False) == 6440
    assert day_07.calculate_winnings(document.split("\n"), True) == 5905
