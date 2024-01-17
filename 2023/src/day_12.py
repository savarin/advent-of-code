from typing import List, Tuple
import helpers


def scan_conditions(lines: List[str]) -> List[Tuple[str, List[int]]]:
    pairs = []

    for line in lines:
        condition, record = line.split(" ")
        arrangement = [int(item) for item in record.split(",")]

        pairs.append((condition, arrangement))

    return pairs


def generate_possibilities(initial_condition: str) -> List[str]:
    queue = [(initial_condition, 0)]
    possibilities = []

    while queue:
        condition, index = queue.pop(0)

        if index == len(condition):
            possibilities.append(condition)
            continue

        if condition[index] != "?":
            queue.append((condition, index + 1))
            continue

        condition_operational = condition[:index] + "." + condition[index + 1 :]
        condition_damaged = condition[:index] + "#" + condition[index + 1 :]

        queue.append((condition_operational, index + 1))
        queue.append((condition_damaged, index + 1))

    return possibilities


def convert_condition(condition: str) -> List[int]:
    damaged_counter = 0
    arrangement = []

    for i, char in enumerate(condition):
        if char == "#":
            damaged_counter += 1

        if damaged_counter > 0 and (
            char == "." or (char == "#" and i == len(condition) - 1)
        ):
            arrangement.append(damaged_counter)
            damaged_counter = 0

    return arrangement


def filter_possibilities(possibilities: List[str], arrangement: List[int]) -> List[str]:
    conditions = []

    for condition in possibilities:
        if convert_condition(condition) == arrangement:
            conditions.append(condition)

    return conditions


def calculate_total(pairs: List[Tuple[str, List[int]]]) -> int:
    total = 0

    for initial_condition, arrangement in pairs:
        possibilities = generate_possibilities(initial_condition)
        conditions = filter_possibilities(possibilities, arrangement)

        total += len(conditions)

    return total


if __name__ == "__main__":
    lines = helpers.generate_lines("2023/data/day_12.txt")

    pairs = scan_conditions(lines)
    print(calculate_total(pairs))
