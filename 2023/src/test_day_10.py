import day_10


def test_solve_loop() -> None:
    document = """\
.....
.S-7.
.|.|.
.L-J.
....."""

    solution, boundary = day_10.solve_loop(document.split("\n"))
    assert solution == 4

    islands = day_10.get_islands(document.split("\n"), boundary)
    assert day_10.count_tiles(document.split("\n"), islands, boundary) == 1

    document = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

    solution, boundary = day_10.solve_loop(document.split("\n"))
    assert solution == 4

    islands = day_10.get_islands(document.split("\n"), boundary)
    assert day_10.count_tiles(document.split("\n"), islands, boundary) == 1

    document = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

    solution, boundary = day_10.solve_loop(document.split("\n"))
    assert solution == 8

    islands = day_10.get_islands(document.split("\n"), boundary)
    assert day_10.count_tiles(document.split("\n"), islands, boundary) == 1

    document = """\
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

    solution, boundary = day_10.solve_loop(document.split("\n"))
    assert solution == 8

    islands = day_10.get_islands(document.split("\n"), boundary)
    assert day_10.count_tiles(document.split("\n"), islands, boundary) == 1
