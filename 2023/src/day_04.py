"""
This module is designed to solve the "Scratchcards" problem from the 2023 Advent
of Code. It involves analyzing a series of scratchcards, each containing a list
of winning numbers and player's numbers. The goal is to calculate the total
points based on the number of matches between these numbers, and in the second
part, to determine the total number of scratchcards including those won through
matching.

Classes:
- Card: Represents a scratchcard with its unique ID, winning numbers, and
  player's numbers.

Functions:
- parse_card(line): Parses a single line of input into a Card object.
- count_match(card): Counts the number of matches between a card's winning and
  player's numbers.
- count_points(card): Calculates the points for a card based on the number of
  matches.
- count_cards(cards): Calculates the total number of cards including any
  additional ones won.
"""

from typing import Counter, List, Sequence, Set
import collections
import dataclasses

import helpers


# Define a dataclass to represent each scratchcard
@dataclasses.dataclass
class Card:
    id: int
    n_winners: dataclasses.InitVar[int] = None
    entries: dataclasses.InitVar[List[int]] = None

    # Initialize the scratchcard with the provided winning and player's numbers
    def __post_init__(self, n_winners: int, entries: List[int]) -> None:
        self.winners: Set[int] = set(entries[:n_winners])
        self.selects: Set[int] = set(entries[n_winners:])


# Parse a line of text into a Card object
def parse_card(line: str) -> Card:
    line_index = 0
    item_counter = 0

    items: List[int] = []

    # Process each character in the line to extract card information
    while line_index < len(line):
        match item_counter:
            case 0:
                # Parse each character of the word "Card" and the card ID
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
                # Parse winning numbers, separated by a vertical bar from
                # player's numbers
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
                # Parse player's numbers
                selection, line_index = helpers.parse_digits(line, line_index)
                items.append(int(selection))

                if line_index == len(line):
                    break

                line_index = helpers.parse_whitespace(line, line_index)

            case _:
                raise ValueError("Expected sequence of digits.")

    return Card(int(card_id), n_winners, items)


# Count the number of matches between winning and player's numbers on a card
def count_match(card: Card) -> int:
    counter = 0

    for select in card.selects:
        if select in card.winners:
            counter += 1

    return counter


# Calculate the points for a card based on the number of matches
def count_points(card: Card) -> int:
    counter = count_match(card)
    points = 0 if counter == 0 else 2 ** (counter - 1)
    assert isinstance(points, int)

    return points


# Calculate the total number of cards including originals and copies won
def count_cards(cards: Sequence[Card]) -> int:
    counts: Counter[int] = collections.Counter()

    for card in cards:
        match = count_match(card)
        copies = counts[card.id]

        # Increment the count for each card ID based on the number of matches
        for i in range(match):
            counts[card.id + i + 1] += 1 + copies

    total_copies = sum([v for _, v in counts.items()])
    return len(cards) + total_copies


if __name__ == "__main__":
    # Process each line to create Card objects and calculate total points and
    # card count
    lines = helpers.generate_lines("2023/data/day_04.txt")
    total = 0
    cards = []

    for line in lines:
        card = parse_card(line)
        total += count_points(card)
        cards.append(card)

    print(total)  # Print the total points from all scratchcards
    print(count_cards(cards))  # Print the total number of scratchcards including copies
