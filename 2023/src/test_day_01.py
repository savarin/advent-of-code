from . import day_01


def test_get_calibration_values() -> None:
    document = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

    assert day_01.get_calibration_values(document.split("\n")) == 142
