import day_03


def test_get_calibration_values_simple() -> None:
    document = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

    assert day_03.get_part_numbers_sum(document.split("\n")) == (4361, 467835)
