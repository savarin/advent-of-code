from typing import Dict, Iterable, Tuple

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


def validate_line(line: str) -> Tuple[str, str]:
    prefix, all_draws_string = line.split(": ")
    assert prefix[:5] == "Game "

    for char in prefix[5:]:
        assert char.isdigit()

    return prefix, all_draws_string


def add_valid_games(limits: Dict[str, int], lines: Iterable[str]) -> int:
    total = 0

    for line in lines:
        prefix, all_draws_string = validate_line(line)
        game_id = int(prefix[5:])

        is_valid = True

        for draws_string in all_draws_string.split("; "):
            if not verify_within_limits(limits, convert_to_draws_dict(draws_string)):
                is_valid = False
                break

        if is_valid:
            total += game_id

    return total


def add_set_powers(lines: Iterable[str]) -> int:
    total = 0

    for line in lines:
        prefix, all_draws_string = validate_line(line)
        max_draws_dict: Dict[str, int] = {}

        for draws_string in all_draws_string.split("; "):
            draws_dict = convert_to_draws_dict(draws_string)

            for k, v in draws_dict.items():
                if k not in max_draws_dict or max_draws_dict[k] < v:
                    max_draws_dict[k] = v

        power = 1

        for _, v in max_draws_dict.items():
            power *= v

        total += power

    return total


if __name__ == "__main__":
    lines = helpers.generate_lines("2023/data/day_02.txt")

    print(add_valid_games({"red": 12, "green": 13, "blue": 14}, lines))
    print(add_set_powers(lines))
