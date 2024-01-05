from typing import Generator


def generate_lines(filename: str) -> Generator[str, None, None]:
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()
