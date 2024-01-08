from typing import Tuple

import dataclasses


@dataclasses.dataclass(frozen=True)
class Vector:
    x: int
    y: int
    z: int


@dataclasses.dataclass(frozen=True)
class Hailstone:
    position: Vector
    velocity: Vector


def expect(line: str, line_index: int, char: str) -> int:
    if char == line[line_index]:
        return line_index + 1

    raise ValueError(f"Expected {char} but found {line[line_index]}")


def parse_digits(line: str, line_index: int) -> Tuple[str, int]:
    char_buffer = ""

    if line[line_index] == "-":
        char_buffer += "-"
        line_index += 1

    while line[line_index].isdigit():
        char_buffer += line[line_index]
        line_index += 1

        if line_index == len(line):
            break

    return char_buffer, line_index


def parse_hailstone(line: str) -> Hailstone:
    line_index = 0
    item_counter = 0

    items = []

    while line_index < len(line):
        match item_counter:
            # expect: digits comma space
            case 0 | 1:
                digits, line_index = parse_digits(line, line_index)
                items.append(int(digits))
                item_counter += 1

                line_index = expect(line, line_index, ",")
                line_index = expect(line, line_index, " ")

            # expect: digits space at space
            case 2:
                digits, line_index = parse_digits(line, line_index)
                items.append(int(digits))
                item_counter += 1

                line_index = expect(line, line_index, " ")
                line_index = expect(line, line_index, "@")
                line_index = expect(line, line_index, " ")

            # expect: digits comma space
            case 3 | 4:
                digits, line_index = parse_digits(line, line_index)
                items.append(int(digits))
                item_counter += 1

                line_index = expect(line, line_index, ",")
                line_index = expect(line, line_index, " ")

            # expect: digits EOL
            case 5:
                digits, line_index = parse_digits(line, line_index)
                items.append(int(digits))

                if line_index != len(line):
                    raise ValueError("Expected EOL after item 5")

            case _:
                raise ValueError("Expected exactly 6 items.")

    position = Vector(*items[:3])
    velocity = Vector(*items[3:])
    return Hailstone(position, velocity)


if __name__ == "__main__":
    line = "19, 13, 30 @ -2, 1, -2"
    print(parse_hailstone(line))
