import day_09


def test_extrapolate_next_value() -> None:
    document = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

    lines = document.split("\n")
    next_total, prior_total = 0, 0

    for values in day_09.scan_values(lines):
        next_item, prior_item = day_09.extrapolate_next_value(values)
        next_total += next_item
        prior_total += prior_item

    assert next_total == 114
    assert prior_total == 2
