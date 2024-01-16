import day_11


def test_sum_distances() -> None:
    document = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

    lines = document.split("\n")
    galaxies, non_empty_rows, non_empty_columns = day_11.scan_galaxies(lines)

    assert galaxies == {
        0: (0, 3),
        1: (1, 7),
        2: (2, 0),
        3: (4, 6),
        4: (5, 1),
        5: (6, 9),
        6: (8, 7),
        7: (9, 0),
        8: (9, 4),
    }

    row_adjustments, column_adjustments = day_11.create_adjustments(
        non_empty_rows, non_empty_columns
    )

    assert row_adjustments == {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 1,
        5: 1,
        6: 1,
        7: 1,
        8: 2,
        9: 2,
    }

    assert column_adjustments == {
        0: 0,
        1: 0,
        2: 0,
        3: 1,
        4: 1,
        5: 1,
        6: 2,
        7: 2,
        8: 2,
        9: 3,
    }

    galaxies_1 = day_11.apply_adjustments(
        galaxies.copy(), row_adjustments, column_adjustments
    )

    assert galaxies_1 == {
        0: (0, 4),
        1: (1, 9),
        2: (2, 0),
        3: (5, 8),
        4: (6, 1),
        5: (7, 12),
        6: (10, 9),
        7: (11, 0),
        8: (11, 5),
    }

    assert day_11.sum_distances(galaxies_1) == 374

    row_adjustments, column_adjustments = day_11.create_adjustments(
        non_empty_rows, non_empty_columns, 10
    )

    galaxies_2 = day_11.apply_adjustments(
        galaxies.copy(), row_adjustments, column_adjustments
    )

    assert day_11.sum_distances(galaxies_2) == 1030

    row_adjustments, column_adjustments = day_11.create_adjustments(
        non_empty_rows, non_empty_columns, 100
    )

    galaxies_3 = day_11.apply_adjustments(
        galaxies.copy(), row_adjustments, column_adjustments
    )

    assert day_11.sum_distances(galaxies_3) == 8410
