from typing import Dict, Iterable, Tuple
import helpers


LOCATION_LENGTH = 3


def scan_map(lines: Iterable[str]) -> Tuple[str, Dict[str, Tuple[str, str]]]:
    section_counter = 0
    directions = {}

    for line in lines:
        if len(line) == 0:
            continue

        match section_counter:
            case 0:
                instructions = line
                section_counter += 1

            case 1:
                line_index = 0
                key = line[:LOCATION_LENGTH]
                line_index += LOCATION_LENGTH

                line_index = helpers.parse_whitespace(line, line_index)
                line_index = helpers.expect(line, line_index, "=")
                line_index = helpers.parse_whitespace(line, line_index)
                line_index = helpers.expect(line, line_index, "(")

                left = line[line_index : line_index + LOCATION_LENGTH]
                line_index += LOCATION_LENGTH
                line_index = helpers.parse_whitespace(line, line_index)
                line_index = helpers.expect(line, line_index, ",")
                line_index = helpers.parse_whitespace(line, line_index)

                right = line[line_index : line_index + LOCATION_LENGTH]
                line_index += LOCATION_LENGTH
                line_index = helpers.expect(line, line_index, ")")

                directions[key] = (left, right)

    return instructions, directions


def follow_directions_single(
    instructions: str, directions: Dict[str, Tuple[str, str]]
) -> int:
    current_location = "AAA"
    step_counter = 0

    while current_location != "ZZZ":
        next_direction = instructions[step_counter % len(instructions)]
        next_index = "LR".index(next_direction)

        next_location = directions[current_location][next_index]
        current_location = next_location
        step_counter += 1

    return step_counter


if __name__ == "__main__":
    lines = list(helpers.generate_lines("2023/data/day_08.txt"))

    instructions, directions = scan_map(lines)
    print(follow_directions_single(instructions, directions))
