from typing import List, Optional


def update_tail(head: List[int], tail: List[int]) -> List[int]:
    result: List[Optional[int]] = [None, None]

    x_diff = head[1] - tail[1]
    y_diff = head[0] - tail[0]

    if abs(x_diff) == 2 and abs(y_diff) == 0:
        result[0] = tail[0]
        result[1] = tail[1] + x_diff // 2

    elif abs(x_diff) == 0 and abs(y_diff) == 2:
        result[0] = tail[0] + y_diff // 2
        result[1] = tail[1]

    elif abs(x_diff) == 2 and abs(y_diff) == 1:
        result[0] = tail[0] + y_diff
        result[1] = tail[1] + x_diff // 2

    elif abs(x_diff) == 1 and abs(y_diff) == 2:
        result[0] = tail[0] + y_diff // 2
        result[1] = tail[1] + x_diff

    elif abs(x_diff) == 2 and abs(y_diff) == 2:
        result[0] = tail[0] + y_diff // 2
        result[1] = tail[1] + x_diff // 2

    else:
        result = [item for item in tail if item is not None]

    return [item for item in result if item is not None]


def run_simple_instructions(instructions: List[str]) -> int:
    head, tail = [0, 0], [0, 0]
    locations = set()

    for instruction in instructions:
        direction, count = instruction.split(" ")

        for _ in range(int(count)):
            if direction == "R":
                head[1] += 1

            elif direction == "L":
                head[1] -= 1

            elif direction == "U":
                head[0] -= 1

            elif direction == "D":
                head[0] += 1

            else:
                raise Exception("Exhaustive switch error.")

            tail = update_tail(head, tail)
            locations.add(tuple(tail))

    return len(locations)


def run_complex_instructions(instructions: List[str], size: int) -> int:
    knots = [[0, 0] for _ in range(size)]
    locations = set()

    for instruction in instructions:
        direction, count = instruction.split(" ")

        for _ in range(int(count)):
            if direction == "R":
                knots[0][1] += 1

            elif direction == "L":
                knots[0][1] -= 1

            elif direction == "U":
                knots[0][0] -= 1

            elif direction == "D":
                knots[0][0] += 1

            else:
                raise Exception("Exhaustive switch error.")

            for i in range(1, size):
                knots[i] = update_tail(knots[i - 1], knots[i])

            locations.add(tuple(knots[-1]))

    return len(locations)


def test_run_simple_instructions():
    instructions = [
        "R 4",
        "U 4",
        "L 3",
        "D 1",
        "R 4",
        "D 1",
        "L 5",
        "R 2",
    ]

    assert run_simple_instructions(instructions) == 13


def test_run_complex_instructions():
    instructions = [
        "R 5",
        "U 8",
        "L 8",
        "D 3",
        "R 17",
        "D 10",
        "L 25",
        "U 20",
    ]

    assert run_complex_instructions(instructions, 10) == 36


if __name__ == "__main__":
    test_run_simple_instructions()
    test_run_complex_instructions()

    instructions = []

    with open("data/day_09.txt", "r") as f:
        for line in f:
            instructions.append(line.rstrip("\n"))

    print(run_simple_instructions(instructions))
    print(run_complex_instructions(instructions, 10))
