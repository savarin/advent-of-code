import day_10


def test_solve_loop() -> None:
    document = """\
.....
.S-7.
.|.|.
.L-J.
....."""

    assert day_10.solve_loop(document.split("\n")) == 4

    document = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

    assert day_10.solve_loop(document.split("\n")) == 4

    document = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

    assert day_10.solve_loop(document.split("\n")) == 8

    document = """\
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

    assert day_10.solve_loop(document.split("\n")) == 8
