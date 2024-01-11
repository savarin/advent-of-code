from typing import Iterable, List, Tuple
import helpers


def scan_race_parameters(lines: Iterable[str]) -> Tuple[List[int], List[int]]:
    section_counter = 0
    times, distances = [], []

    for line in lines:
        line_index = 0

        while line_index < len(line):
            match section_counter:
                # Time: digits
                case 0:
                    if line_index == 0:
                        line_index = helpers.expect(line, line_index, "Time:")
                        continue

                    line_index = helpers.parse_whitespace(line, line_index)
                    time, line_index = helpers.parse_digits(line, line_index)
                    times.append(int(time))

                # Distance: digits
                case 1:
                    if line_index == 0:
                        line_index = helpers.expect(line, line_index, "Distance:")
                        continue

                    line_index = helpers.parse_whitespace(line, line_index)
                    distance, line_index = helpers.parse_digits(line, line_index)
                    distances.append(int(distance))

        section_counter += 1

    assert len(times) == len(distances)
    return times, distances


def count_ways(time: int, distance: int) -> int:
    ways = 0

    # Skip pressing button for zero seconds and the whole time.
    for i in range(1, time):
        current_distance = i * (time - i)

        if current_distance > distance:
            ways += 1

    return ways


if __name__ == "__main__":
    lines = helpers.generate_lines("2023/data/day_06.txt")
    times, distances = scan_race_parameters(lines)

    product = 1

    for i in range(len(times)):
        product *= count_ways(times[i], distances[i])

    print(product)
