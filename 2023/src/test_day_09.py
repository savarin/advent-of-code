import day_09


def test_extrapolate_next_value() -> None:
    document = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

    lines = document.split("\n")
    total = 0

    for values in day_09.scan_values(lines):
        total += day_09.extrapolate_next_value(values)

    assert total == 114
