from typing import List, Set
import dataclasses

import helpers


@dataclasses.dataclass
class Card:
    id: int
    n_winners: dataclasses.InitVar[int] = None
    entries: dataclasses.InitVar[List[int]] = None

    def __post_init__(self, n_winners: int, entries: List[int]) -> None:
        self.winners: Set[int] = set(entries[:n_winners])
        self.selects: Set[int] = set(entries[n_winners:])


def parse_card(line: str) -> Card:
    line_index = 0
    item_counter = 0

    items: List[int] = []

    while line_index < len(line):
        match item_counter:
            case 0:
                line_index = helpers.expect(line, line_index, "C")
                line_index = helpers.expect(line, line_index, "a")
                line_index = helpers.expect(line, line_index, "r")
                line_index = helpers.expect(line, line_index, "d")
                line_index = helpers.parse_whitespace(line, line_index)
                card_id, line_index = helpers.parse_digits(line, line_index)
                line_index = helpers.expect(line, line_index, ":")
                line_index = helpers.parse_whitespace(line, line_index)

                item_counter += 1

            case 1:
                if line[line_index] == "|":
                    n_winners = len(items)

                    line_index += 1
                    line_index = helpers.parse_whitespace(line, line_index)

                    item_counter += 1
                    continue

                winner, line_index = helpers.parse_digits(line, line_index)
                items.append(int(winner))

                line_index = helpers.parse_whitespace(line, line_index)

            case 2:
                selection, line_index = helpers.parse_digits(line, line_index)
                items.append(int(selection))

                if line_index == len(line):
                    break

                line_index = helpers.parse_whitespace(line, line_index)

            case _:
                raise ValueError("Expected sequence of digits.")

    return Card(int(card_id), n_winners, items)


def count_points(card: Card) -> int:
    counter = 0

    for select in card.selects:
        if select in card.winners:
            counter += 1

    points = 0 if counter == 0 else 2 ** (counter - 1)
    assert isinstance(points, int)

    return points


if __name__ == "__main__":
    lines = helpers.generate_lines("2023/data/day_04.txt")
    total = 0

    for line in lines:
        total += count_points(parse_card(line))

    print(total)
