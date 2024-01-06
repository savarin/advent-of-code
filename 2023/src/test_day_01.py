from . import day_01


def test_get_calibration_values_simple() -> None:
    document = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

    assert day_01.get_calibration_values_simple(document.split("\n")) == 142


def test_get_numbers() -> None:
    assert day_01.get_numbers("two1nine") == ["2", "1", "9"]
    assert day_01.get_numbers("eightwothree") == ["8", "2", "3"]
    assert day_01.get_numbers("abcone2threexyz") == ["1", "2", "3"]


def test_get_calibration_values_composite() -> None:
    document = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

    assert day_01.get_calibration_values_composite(document.split("\n")) == 281
