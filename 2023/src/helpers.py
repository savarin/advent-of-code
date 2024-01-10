from typing import Generator, Tuple


def generate_lines(filename: str) -> Generator[str, None, None]:
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()


def expect(line: str, line_index: int, chars: str) -> int:
    for char in chars:
        if char == line[line_index]:
            line_index += 1
            continue

        raise ValueError(f"Expected {char} but found {line[line_index]}.")

    return line_index


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


def parse_whitespace(line: str, line_index: int) -> int:
    while line[line_index].isspace():
        line_index += 1

        if line_index == len(line):
            break

    return line_index
