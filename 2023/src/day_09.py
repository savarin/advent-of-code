from typing import Generator, Iterable, List, Sequence, Tuple
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


def create_steps(values: Sequence[int]) -> List[Sequence[int]]:
    steps = [values]

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

    return steps


def extrapolate_next_value(values: Sequence[int]) -> Tuple[int, int]:
    steps = create_steps(values)
    next_value = 0

    prior_starts = [0]

    for i in range(len(steps) - 1, 0, -1):
        current_diff = steps[i - 1]
        next_value += current_diff[-1]

        prior_starts.append(current_diff[0] - prior_starts[-1])

    return next_value, prior_starts[-1]


if __name__ == "__main__":
    lines = list(helpers.generate_lines("2023/data/day_09.txt"))
    next_total, prior_total = 0, 0

    for values in scan_values(lines):
        next_item, prior_item = extrapolate_next_value(values)
        next_total += next_item
        prior_total += prior_item

    print(next_total)
    print(prior_total)
