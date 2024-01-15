"""
This module is developed to solve the "Pipe Maze" challenge from the 2023 Advent
of Code, Day 10. It provides a comprehensive solution for navigating a complex
maze of interconnected pipes, determining the longest path within a loop, and
identifying enclosed areas.

The challenge presents a grid of pipes where different symbols represent various
pipe bends and connections. The module includes functions to interpret this
grid, navigate through the pipes, and find the longest path in a continuous loop
starting from a specified position. Additionally, it calculates the number of
tiles enclosed by the loop, which is crucial for the second part of the
challenge.

Key functionalities include identifying the starting point, calculating
directional changes based on pipe types, and implementing a breadth-first search
algorithm to explore the maze. The module also identifies 'islands' or enclosed
areas within the loop, crucial for understanding the maze's layout and solving
the challenge.

The narrative involves following an animal through the maze, requiring a
strategic approach to trace its path and explore enclosed areas. This module is
a vital tool for players to solve the puzzle efficiently and enhance their
understanding of complex pathfinding algorithms.

https://adventofcode.com/2023/day/10

Functions:
- init_redirection: Initializes direction mapping for different pipe types.
- find_start_location: Finds the starting point in the grid.
- resolve_location: Calculates the next location based on direction and pipe
  type.
- reverse_direction: Determines the opposite direction for a given direction.
- count_steps: Counts the number of steps in the loop from the start location.
- solve_loop: Solves the main loop of the maze to find the farthest point from
  the start.
- get_islands: Identifies and groups tiles within the loop's boundaries.
- count_tiles: Counts the number of tiles enclosed within the loop.
"""

from typing import Deque, Dict, List, Optional, Tuple
import collections
import enum

import helpers


class Direction(enum.Enum):
    """
    Enum representing the four cardinal directions: North, South, East and West.
    Used for navigating through the grid of pipes in the Pipe Maze.
    """

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
    """
    Initialize the redirection dictionary for a given pipe type.

    Args:
        from_north, from_south, from_east, from_west (Optional[Direction]): The
        direction from which the pipe is entered.

    Returns:
        Dict[Direction, Optional[Direction]]: A dictionary mapping each entry
        direction to its exit direction.
    """
    return {
        Direction.NORTH: from_north,
        Direction.SOUTH: from_south,
        Direction.EAST: from_east,
        Direction.WEST: from_west,
    }


# Global dictionary defining how each pipe type redirects the flow from each
# possible entry direction.
REDIRECTION = {
    "|": init_redirection(Direction.SOUTH, Direction.NORTH, None, None),
    "-": init_redirection(None, None, Direction.WEST, Direction.EAST),
    "L": init_redirection(Direction.EAST, None, Direction.NORTH, None),
    "J": init_redirection(Direction.WEST, None, None, Direction.NORTH),
    "7": init_redirection(None, Direction.WEST, None, Direction.SOUTH),
    "F": init_redirection(None, Direction.EAST, Direction.SOUTH, None),
}


def find_start_location(lines: List[str]) -> Optional[Tuple[int, int]]:
    """
    Find the starting location (marked 'S') in the grid of pipes.

    Args:
        lines (List[str]): The grid represented as a list of strings.

    Returns:
        Optional[Tuple[int, int]]: The coordinates of the start location, or
        None if not found.
    """
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
    """
    Calculate the next location based on the current location and the direction
    of movement.

    Args:
        current_location (Tuple[int, int]): The current coordinates.
        next_direction (Direction): The direction in which to move.
        max_row, max_column (int): The maximum row and column indices in the
        grid.

    Returns:
        Optional[Tuple[int, int]]: The next location, or None if it would be out
        of bounds.
    """
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
            # Raises an exception if an undefined direction is encountered
            raise Exception("Invalid direction encountered")

    # Calculate and return the new location based on the direction of movement
    return (current_location[0] + diff[0], current_location[1] + diff[1])


def reverse_direction(direction: Direction) -> Direction:
    """
    Reverse the given direction. Used to determine the incoming direction at a
    pipe junction.

    Args:
        direction (Direction): The current direction.

    Returns:
        Direction: The opposite direction.
    """
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
    """
    Count the number of steps from the start location to each point in the loop,
    and track the path taken.

    Args:
        lines (List[str]): The grid of pipes.
        start_location (Tuple[int, int]): Starting coordinates.
        direction (Direction): Starting direction.
        max_row, max_column (int): Maximum row and column indices in the grid.

    Returns:
        Tuple[Optional[int], List[Tuple[int, int]]]: The number of steps and the
        path taken (as coordinates).
    """
    # Initialize queue with step count, start location, and direction
    queue = [(0, start_location, direction)]

    # List to track the path taken
    path = []

    # Iterate through the queue until it's empty
    while queue:
        counter, current_location, next_direction = queue.pop(0)

        # Add current location to the path
        path.append(current_location)

        # Determine the next location based on current location and direction
        next_location = resolve_location(
            current_location, next_direction, max_row, max_column
        )

        # Check for out-of-bounds or returning to start location
        if next_location is None:
            print("Out of bounds!")
            continue

        elif next_location == start_location:
            return counter, path

        # Identify the type of the next pipe and handle redirection
        next_pipe = lines[next_location[0]][next_location[1]]

        if next_pipe not in REDIRECTION:
            print(f"Invalid next pipe {next_pipe}!")
            continue

        from_direction = reverse_direction(next_direction)
        to_direction = REDIRECTION[next_pipe][from_direction]

        # If no valid direction to move, continue to the next iteration
        if to_direction is None:
            print(
                f"Next pipe {next_pipe}, from direction {from_direction}, to direction null!"
            )
            continue

        # Append the next location and direction to the queue
        queue.append((counter + 1, next_location, to_direction))

    # Return None and the path if the loop is not closed
    return None, path


def solve_loop(lines: List[str]) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Solve the main loop of the pipe maze. It finds the farthest point from the
    start within the loop.

    Args:
        lines (List[str]): The grid of pipes as a list of strings.

    Returns:
        Tuple[int, List[Tuple[int, int]]]: The maximum number of steps from the
        start to the farthest point, and the path to that point.
    """
    max_row = len(lines) - 1
    max_column = len(lines[0]) - 1

    start_location = find_start_location(lines)
    assert start_location is not None, "Start location not found in the grid"

    # Counter for directions leading to no result

    null_counter = 0
    # List to store the number of steps for each direction

    steps_list = []
    # Variable to store the successful path
    path = None

    # Iterating over all four cardinal directions to find the loop
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

        # If a valid path is found, store its steps and path
        if steps is not None:
            steps_list.append(steps)
            path = current_path

        else:
            null_counter += 1

    assert (
        len(steps_list) == 2
    ), "The main loop should have exactly two valid directions"
    assert (
        steps_list[0] == steps_list[1]
    ), "The number of steps should be the same in both valid directions"

    assert path is not None, "No valid path found in the maze"
    return (steps_list[0] + 1) // 2, [start_location] + path


def get_islands(
    lines: List[str], boundary: List[Tuple[int, int]]
) -> Dict[int, List[Tuple[int, int]]]:
    """
    Identify and group the 'islands' of tiles within the boundaries of the main
    loop.

    Args:
        lines (List[str]): The grid of pipes as a list of strings.
        boundary (List[Tuple[int, int]]): The coordinates forming the boundary
        of the main loop.

    Returns:
        Dict[int, List[Tuple[int, int]]]: A dictionary where each key is an
        island index and the value is a list of coordinates.
    """
    row_count, column_count = len(lines), len(lines[0])

    # Set of coordinates already visited
    visit = set(boundary)

    # Counter to assign unique IDs to each island
    counter = 0

    # Dictionary to store islands and their coordinates
    islands: Dict[int, List[Tuple[int, int]]] = {}

    def bfs(row_index: int, column_index: int, counter: int) -> None:
        """
        Perform a Breadth-First Search (BFS) to explore and mark all tiles of an island.

        Args:
            row_index, column_index (int): Starting tile coordinates for the BFS.
            counter (int): Island identifier.
        """
        visit.add((row_index, column_index))

        queue: Deque[Tuple[int, int]] = collections.deque()
        queue.append((row_index, column_index))

        # Possible directions to move (N, S, E, W)
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

    # Iterate over every tile in the grid
    for row_index in range(row_count):
        for column_index in range(column_count):
            # If the tile has not been visited, it's a new island
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
    """
    Count the number of tiles enclosed by the loop in the pipe maze.

    Args:
        lines (List[str]): The grid of pipes as a list of strings.
        islands (Dict[int, List[Tuple[int, int]]]): The islands identified
        within the loop.
        boundary_list (List[Tuple[int, int]]): The boundary of the main loop.

    Returns:
        int: The total number of tiles enclosed by the loop.
    """
    # Counter for the number of enclosed tiles
    tiles = 0

    # Convert the boundary list to a set for efficient lookup
    boundary = set(boundary_list)

    # Iterate through each island
    for _, island in islands.items():
        row_index, column_index = island[0]

        boundary_count = 0
        is_f_boundary, is_l_boundary = False, False

        # Check each tile to the left of the starting point of the island
        for j in range(column_index):
            if (row_index, j) in boundary:
                # Different conditions based on the type of pipe encountered
                if lines[row_index][j] == "|":
                    boundary_count += 1

                # TODO: Fix hack on replacing "S"
                elif lines[row_index][j] in {"F", "S"}:
                    is_f_boundary = True

                elif lines[row_index][j] == "L":
                    is_l_boundary = True

                elif is_f_boundary:
                    if lines[row_index][j] == "J":
                        boundary_count += 1
                        is_f_boundary = False

                    elif lines[row_index][j] == "7":
                        is_f_boundary = False

                elif is_l_boundary:
                    if lines[row_index][j] == "7":
                        boundary_count += 1
                        is_l_boundary = False

                    elif lines[row_index][j] == "J":
                        is_l_boundary = False

        # Add the number of tiles in the island if the boundary count is odd
        if boundary_count % 2 == 1:
            tiles += len(island)

    return tiles


if __name__ == "__main__":
    lines = list(helpers.generate_lines("2023/data/day_10.txt"))

    solution, boundary = solve_loop(lines)
    print(solution)

    islands = get_islands(lines, boundary)
    print(count_tiles(lines, islands, boundary))
