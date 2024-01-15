from typing import Deque, Dict, List, Optional, Tuple
import collections
import enum

import helpers


class Direction(enum.Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


def init_redirection(
    from_north: Optional[Direction],
    from_south: Optional[Direction],
    from_east: Optional[Direction],
    from_west: Optional[Direction],
) -> Dict[Direction, Optional[Direction]]:
    return {
        Direction.NORTH: from_north,
        Direction.SOUTH: from_south,
        Direction.EAST: from_east,
        Direction.WEST: from_west,
    }


# Next position depending on entry, in order: north, south, east, west
REDIRECTION = {
    "|": init_redirection(Direction.SOUTH, Direction.NORTH, None, None),
    "-": init_redirection(None, None, Direction.WEST, Direction.EAST),
    "L": init_redirection(Direction.EAST, None, Direction.NORTH, None),
    "J": init_redirection(Direction.WEST, None, None, Direction.NORTH),
    "7": init_redirection(None, Direction.WEST, None, Direction.SOUTH),
    "F": init_redirection(None, Direction.EAST, Direction.SOUTH, None),
}


def find_start_location(lines: List[str]) -> Optional[Tuple[int, int]]:
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "S":
                return (i, j)

    return None


def resolve_location(
    current_location: Tuple[int, int],
    next_direction: Direction,
    max_row: int,
    max_column: int,
) -> Optional[Tuple[int, int]]:
    diff = None

    match next_direction:
        case Direction.NORTH:
            if current_location[0] == 0:
                return None

            diff = (-1, 0)

        case Direction.SOUTH:
            if current_location[0] == max_row:
                return None

            diff = (1, 0)

        case Direction.EAST:
            if current_location[1] == max_column:
                return None

            diff = (0, 1)

        case Direction.WEST:
            if current_location[1] == 0:
                return None

            diff = (0, -1)

        case _:
            raise Exception

    return (current_location[0] + diff[0], current_location[1] + diff[1])


def reverse_direction(direction: Direction) -> Direction:
    match direction:
        case Direction.NORTH:
            return Direction.SOUTH

        case Direction.SOUTH:
            return Direction.NORTH

        case Direction.EAST:
            return Direction.WEST

        case Direction.WEST:
            return Direction.EAST


def count_steps(
    lines: List[str],
    start_location: Tuple[int, int],
    direction: Direction,
    max_row: int,
    max_column: int,
) -> Tuple[Optional[int], List[Tuple[int, int]]]:
    queue = [(0, start_location, direction)]
    path = []

    while queue:
        counter, current_location, next_direction = queue.pop(0)
        path.append(current_location)

        next_location = resolve_location(
            current_location, next_direction, max_row, max_column
        )

        if next_location is None:
            print("Out of bounds!")
            continue

        elif next_location == start_location:
            return counter, path

        next_pipe = lines[next_location[0]][next_location[1]]

        if next_pipe not in REDIRECTION:
            print(f"Invalid next pipe {next_pipe}!")
            continue

        from_direction = reverse_direction(next_direction)
        to_direction = REDIRECTION[next_pipe][from_direction]

        if to_direction is None:
            print(
                f"Next pipe {next_pipe}, from direction {from_direction}, to direction null!"
            )
            continue

        queue.append((counter + 1, next_location, to_direction))

    return None, path


def solve_loop(lines: List[str]) -> Tuple[int, List[Tuple[int, int]]]:
    max_row = len(lines) - 1
    max_column = len(lines[0]) - 1

    start_location = find_start_location(lines)
    assert start_location is not None

    null_counter = 0
    steps_list = []
    path = None

    for next_direction in [
        Direction.NORTH,
        Direction.SOUTH,
        Direction.EAST,
        Direction.WEST,
    ]:
        print(f"\nNext direction {next_direction}:")
        steps, current_path = count_steps(
            lines, start_location, next_direction, max_row, max_column
        )

        if steps is None:
            null_counter += 1
            continue

        steps_list.append(steps)
        path = current_path

    assert len(steps_list) == 2
    assert steps_list[0] == steps_list[1]

    assert path is not None
    return (steps_list[0] + 1) // 2, [start_location] + path


def get_islands(
    lines: List[str], boundary: List[Tuple[int, int]]
) -> Dict[int, List[Tuple[int, int]]]:
    row_count, column_count = len(lines), len(lines[0])

    visit = set(boundary)
    counter = 0

    islands: Dict[int, List[Tuple[int, int]]] = {}

    def bfs(row_index: int, column_index: int, counter: int) -> None:
        visit.add((row_index, column_index))

        queue: Deque[Tuple[int, int]] = collections.deque()
        queue.append((row_index, column_index))

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue:
            current_row_index, current_column_index = queue.popleft()

            for row_direction, column_direction in directions:
                row_index = current_row_index + row_direction
                column_index = current_column_index + column_direction

                if (
                    row_index in range(row_count)
                    and column_index in range(column_count)
                    and (row_index, column_index) not in visit
                ):
                    queue.append((row_index, column_index))
                    visit.add((row_index, column_index))
                    islands[counter].append((row_index, column_index))

    for row_index in range(row_count):
        for column_index in range(column_count):
            if (row_index, column_index) not in visit:
                islands[counter] = [(row_index, column_index)]
                bfs(row_index, column_index, counter)

                counter += 1

    return islands


def count_tiles(
    lines: List[str],
    islands: Dict[int, List[Tuple[int, int]]],
    boundary_list: List[Tuple[int, int]],
) -> int:
    tiles = 0
    boundary = set(boundary_list)

    for _, island in islands.items():
        row_index, column_index = island[0]

        boundary_count = 0
        is_f_boundary, is_l_boundary = False, False

        for j in range(column_index):
            if (row_index, j) in boundary:
                if lines[row_index][j] == "|":
                    boundary_count += 1

                elif lines[row_index][j] in {"F", "S"}:
                    is_f_boundary = True

                elif lines[row_index][j] == "L":
                    is_l_boundary = True

                elif is_f_boundary:
                    if lines[row_index][j] in "J":
                        boundary_count += 1
                        is_f_boundary = False

                    elif lines[row_index][j] == "7":
                        is_f_boundary = False

                elif is_l_boundary:
                    if lines[row_index][j] == "7":
                        boundary_count += 1
                        is_l_boundary = False

                    elif lines[row_index][j] == "J":
                        is_f_boundary = False

        if boundary_count % 2 == 1:
            tiles += len(island)

    return tiles


if __name__ == "__main__":
    lines = list(helpers.generate_lines("2023/data/day_10.txt"))

    solution, boundary = solve_loop(lines)
    print(solution)

    islands = get_islands(lines, boundary)
    print(count_tiles(lines, islands, boundary))
