import pytest

from day_24 import Hailstone, Vector
import day_24


def test_expect() -> None:
    assert day_24.expect("012", 0, "0")
    assert day_24.expect("012", 1, "1")
    assert day_24.expect("012", 2, "2")

    with pytest.raises(ValueError):
        assert day_24.expect("012", 0, "1")


def test_parse_digits() -> None:
    assert day_24.parse_digits("012", 0) == ("012", 3)
    assert day_24.parse_digits("-012", 0) == ("-012", 4)
    assert day_24.parse_digits("-012", 1) == ("012", 4)

    assert day_24.parse_digits("a", 0) == ("", 0)
    assert day_24.parse_digits("1a", 0) == ("1", 1)


def test_parse_hailstone() -> None:
    assert day_24.parse_hailstone("19, 13, 30 @ -2, 1, -2") == Hailstone(
        position=Vector(x=19, y=13, z=30), velocity=Vector(x=-2, y=1, z=-2)
    )


def test_calculate_intersection_2d() -> None:
    h_1 = day_24.parse_hailstone("19, 13, 30 @ -2, 1, -2")
    h_2 = day_24.parse_hailstone("18, 19, 22 @ -1, -1, -2")
    assert day_24.calculate_intersection_2d(h_1, h_2) == (
        14.333333333333334,
        15.333333333333334,
    )

    h_1 = day_24.parse_hailstone("18, 19, 22 @ -1, -1, -2")
    h_2 = day_24.parse_hailstone("12, 31, 28 @ -1, -2, -1")
    assert day_24.calculate_intersection_2d(h_1, h_2) == (-6.0, -5.0)
