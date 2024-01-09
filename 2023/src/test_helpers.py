import pytest

import helpers


def test_expect() -> None:
    assert helpers.expect("012", 0, "0")
    assert helpers.expect("012", 1, "1")
    assert helpers.expect("012", 2, "2")

    with pytest.raises(ValueError):
        assert helpers.expect("012", 0, "1")


def test_parse_digits() -> None:
    assert helpers.parse_digits("012", 0) == ("012", 3)
    assert helpers.parse_digits("-012", 0) == ("-012", 4)
    assert helpers.parse_digits("-012", 1) == ("012", 4)

    assert helpers.parse_digits("a", 0) == ("", 0)
    assert helpers.parse_digits("1a", 0) == ("1", 1)
