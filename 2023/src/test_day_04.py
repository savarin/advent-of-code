import pytest

from day_04 import Hailstone, Vector
import day_04


def test_expect() -> None:
    assert day_04.expect("012", 0, "0")
    assert day_04.expect("012", 1, "1")
    assert day_04.expect("012", 2, "2")

    with pytest.raises(ValueError):
        assert day_04.expect("012", 0, "1")


def test_parse_digits() -> None:
    assert day_04.parse_digits("012", 0) == ("012", 3)
    assert day_04.parse_digits("-012", 0) == ("-012", 4)
    assert day_04.parse_digits("-012", 1) == ("012", 4)

    assert day_04.parse_digits("a", 0) == ("", 0)
    assert day_04.parse_digits("1a", 0) == ("1", 1)


def test_parse_hailstone() -> None:
    assert day_04.parse_hailstone("19, 13, 30 @ -2, 1, -2") == Hailstone(
        position=Vector(x=19, y=13, z=30), velocity=Vector(x=-2, y=1, z=-2)
    )
