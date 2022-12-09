from typing import List, Optional


def get_visibility(grid: List[List[int]], x: int, y: int) -> List[Optional[bool]]:
    z = grid[y][x]

    x_max = len(grid[0]) - 1
    y_max = len(grid) - 1

    visible: List[Optional[bool]] = [None, None, None, None]

    for a in range(1, x + 1):
        if grid[y][x - a] >= z:
            visible[0] = False
            break

        if a == x:
            visible[0] = True

    for b in range(1, x_max - x + 1):
        if grid[y][x + b] >= z:
            visible[1] = False
            break

        if b == x_max - x:
            visible[1] = True

    for c in range(1, y + 1):
        if grid[y - c][x] >= z:
            visible[2] = False
            break

        if c == y:
            visible[2] = True

    for d in range(1, y_max - y + 1):
        if grid[y + d][x] >= z:
            visible[3] = False
            break

        if d == y_max - y:
            visible[3] = True

    return visible


def get_viewability(grid: List[List[int]], x: int, y: int) -> List[Optional[int]]:
    z = grid[y][x]

    x_max = len(grid[0]) - 1
    y_max = len(grid) - 1

    viewable: List[Optional[int]] = [None, None, None, None]

    for a in range(1, x + 1):
        if grid[y][x - a] >= z or a == x:
            viewable[0] = a
            break

    for b in range(1, x_max - x + 1):
        if grid[y][x + b] >= z or b == x_max - x:
            viewable[1] = b
            break

    for c in range(1, y + 1):
        if grid[y - c][x] >= z or c == y:
            viewable[2] = c
            break

    for d in range(1, y_max - y + 1):
        if grid[y + d][x] >= z or d == y_max - y:
            viewable[3] = d
            break

    return viewable


def test_get_visibility() -> None:
    grid = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]

    assert get_visibility(grid, 1, 1) == [True, False, True, False]
    assert get_visibility(grid, 1, 2) == [False, True, False, False]
    assert get_visibility(grid, 1, 3) == [False, False, False, False]
    assert get_visibility(grid, 2, 1) == [False, True, True, False]
    assert get_visibility(grid, 2, 2) == [False, False, False, False]
    assert get_visibility(grid, 2, 3) == [True, False, False, True]
    assert get_visibility(grid, 3, 1) == [False, False, False, False]
    assert get_visibility(grid, 3, 2) == [False, True, False, False]
    assert get_visibility(grid, 3, 3) == [False, False, False, False]


def test_get_viewability() -> None:
    grid = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]

    assert get_viewability(grid, 2, 1) == [1, 2, 1, 2]
    assert get_viewability(grid, 2, 3) == [2, 2, 2, 1]


if __name__ == "__main__":
    test_get_visibility()
    test_get_viewability()

    grid = []

    with open("data/day_08.txt", "r") as f:
        for line in f:
            grid.append([int(item) for item in list(line.rstrip("\n"))])

    visible = 0

    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            visible += (
                sum([item for item in get_visibility(grid, i, j) if item is not None])
                == 0
            )

    print(len(grid[0]) * len(grid) - visible)

    viewable = 0

    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            a, b, c, d = get_viewability(grid, i, j)
            assert a is not None and b is not None and c is not None and d is not None
            product = a * b * c * d

            if product > viewable:
                viewable = product

    print(viewable)
