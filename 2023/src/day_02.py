from typing import Dict, Iterable

from . import helpers


def convert_to_draws_dict(draws_string: str) -> Dict[str, int]:
    draws = {}

    for item in draws_string.split(", "):
        count, color = item.split(" ")
        draws[color] = int(count)

    return draws


def verify_within_limits(limits: Dict[str, int], draws: Dict[str, int]) -> bool:
    for k, v in draws.items():
        if v > limits[k]:
            return False

    return True


def add_valid_games(limits: Dict[str, int], lines: Iterable[str]) -> int:
    total = 0

    for line in lines:
        is_valid = True

        prefix, all_draws_string = line.split(": ")

        assert prefix[:5] == "Game "

        for char in prefix[5:]:
            assert char.isdigit()

        game_id = int(prefix[5:])

        for draws_string in all_draws_string.split("; "):
            if not verify_within_limits(limits, convert_to_draws_dict(draws_string)):
                is_valid = False
                break

        if is_valid:
            total += game_id

    return total


if __name__ == "__main__":
    filename = "2023/data/day_02.txt"
    limits = {"red": 12, "green": 13, "blue": 14}

    print(add_valid_games(limits, helpers.generate_lines(filename)))
