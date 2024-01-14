from typing import Iterable, List, Sequence, Generator
import helpers


def scan_values(lines: Iterable[str]) -> Generator[List[int], None, None]:
    for line in lines:
        line_index = 0
        values = []

        while line_index != len(line):
            if line_index != 0:
                line_index = helpers.parse_whitespace(line, line_index)

            value, line_index = helpers.parse_digits(line, line_index)
            values.append(int(value))

        yield values


def extrapolate_next_value(values: Sequence[int]) -> int:
    steps = [values]
    list_count = 1

    while True:
        current_diff = steps[-1]
        all_zeroes = True

        for value in current_diff:
            if value != 0:
                all_zeroes = False
                break

        if all_zeroes:
            break

        next_diff = []

        for i in range(1, len(current_diff)):
            next_diff.append(current_diff[i] - current_diff[i - 1])

        steps.append(next_diff)
        list_count += 1

    current_value = None

    for i in range(list_count, 0, -1):
        if current_value is None:
            current_value = 0
            continue

        current_diff = steps[i - 1]
        current_value += current_diff[-1]

    assert current_value is not None
    return current_value


if __name__ == "__main__":
    lines = list(helpers.generate_lines("2023/data/day_09.txt"))
    total = 0

    for values in scan_values(lines):
        total += extrapolate_next_value(values)

    print(total)
