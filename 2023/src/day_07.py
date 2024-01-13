"""
This module is part of the solution to the "Camel Cards" problem from the 2023
Advent of Code. It focuses on evaluating the strength of card hands in a game,
both in normal and wildcard scenarios, and determining the total winnings based
on the ranking of each hand.

The game rules are akin to poker but with some variations specific to Camel
Cards, including the use of wildcards. This module processes a list of hands,
determines their strengths, ranks them, and calculates the total winnings based
on their rankings.

https://adventofcode.com/2023/day/7

Functions:
- scan_hand_bid_pairs(lines): Extracts hands and bids from input lines.
- evaluate_hand_strength(ranked_hand): Determines the strength of a given hand.
- convert_hand_to_hand_type(hand): Converts a hand to a tuple with its strength
  and ranks.
- generate_all_wildcard_hands(non_wildcard_hand): Generates all wildcard hand
  combinations.
- convert_wildcard_hand_to_hand_type(hand): Finds the strongest type for a
  wildcard hand.
- calculate_winnings(lines, is_wildcard_version): Calculates total winnings
  based on hand rankings.
"""

from typing import Iterable, List, Sequence, Tuple
import collections
import dataclasses

import helpers


# Global variables defining card ranks for regular and wildcard hands.
# Wildcard ranks treat 'J' as the weakest card, unlike regular ranks.
RANKS = "..23456789TJQKA"
WILDCARD_RANKS = "..J23456789TQKA"


@dataclasses.dataclass(frozen=True)
class RankCount:
    """
    Data class representing the count of each rank in a hand.

    Attributes:
        count (int): The number of times a particular rank appears in a hand.
        rank (int): The rank of the card, based on its position in the rank
        string.
    """

    count: int
    rank: int


def scan_hand_bid_pairs(lines: Iterable[str]) -> List[Tuple[str, str]]:
    """
    Parses lines containing hand and bid pairs.

    Args:
        lines (Iterable[str]): An iterable collection of strings, each
        representing a line with a hand and a bid.

    Returns:
        List[Tuple[str, str]]: A list of tuples, each containing a hand (str)
        and its corresponding bid (str).
    """
    pairs = []

    for line in lines:
        line_index = 5  # Line index where the hand ends and bid begins.

        hand = line[:line_index]
        line_index = helpers.parse_whitespace(line, line_index)  # Skipping whitespace.
        bid, _ = helpers.parse_digits(line, line_index)  # Parsing the bid.

        pairs.append((hand, bid))

    return pairs


def evaluate_hand_strength(ranked_hand: Sequence[int]) -> int:
    """
    Evaluates the strength of a hand based on the counts of each rank.

    Args:
        ranked_hand (Sequence[int]): A sequence of integers representing the
        ranks of cards in a hand.

    Returns:
        int: An integer representing the hand's strength, where a higher value
        indicates a stronger hand.
    """
    # Counting occurrences of each rank and sorting in reverse order.
    counts = sorted(
        [(v, k) for k, v in collections.Counter(ranked_hand).items()], reverse=True
    )
    rank_counts = [RankCount(item[0], item[1]) for item in counts]

    # Determining hand type based on counts.
    if rank_counts[0].count == 5:
        return 6  # Five of a kind.

    elif rank_counts[0].count == 4:
        assert rank_counts[1].count == 1
        return 5  # Four of a kind.

    elif rank_counts[0].count == 3:
        if rank_counts[1].count == 2:
            return 4  # Full house.

        assert rank_counts[1].count == 1 and rank_counts[2].count == 1
        return 3  # Three of a kind.

    elif rank_counts[0].count == 2:
        if rank_counts[1].count == 2:
            assert rank_counts[2].count == 1
            return 2  # Two pair.

        assert (
            rank_counts[1].count == 1
            and rank_counts[2].count == 1
            and rank_counts[3].count == 1
        )
        return 1  # One pair.

    return 0  # High card.


def convert_hand_to_hand_type(hand: str) -> Tuple[int, ...]:
    """
    Converts a hand of cards to a tuple representing its type and ranks.

    Args:
        hand (str): A string representing a hand of cards.

    Returns:
        Tuple[int, ...]: A tuple where the first element is the hand's strength,
        followed by the ranks of the cards in the hand.
    """
    ranked_hand = [RANKS.index(char) for char in hand]  # Convert hand to ranks.
    hand_strength = evaluate_hand_strength(ranked_hand)

    return (hand_strength, *ranked_hand)


def generate_all_wildcard_hands(non_wildcard_hand: str) -> List[str]:
    """
    Generates all possible wildcard hands given a partial hand.

    Args:
        non_wildcard_hand (str): A string representing a partial hand without
        wildcards.

    Returns:
        List[str]: A list of all possible hands completed with wildcard
        characters.
    """
    if len(non_wildcard_hand) == 5:
        return [non_wildcard_hand]

    elif non_wildcard_hand == "":
        return ["AAAAA"]  # Hand with all wildcards.

    stack = [""]
    hands = []

    wildcard_count = 5 - len(non_wildcard_hand)  # Number of wildcards to be added.

    while stack:
        item = stack.pop(0)

        for char in set(non_wildcard_hand):
            hand = item + char

            if len(hand) == wildcard_count:
                hands.append(hand)
                continue

            stack.append(hand)

    # Appending the non-wildcard part to each wildcard combination.
    return [hand + non_wildcard_hand for hand in hands]


def convert_wildcard_hand_to_hand_type(hand: str) -> Tuple[int, ...]:
    """
    Converts a wildcard hand to a tuple representing its strongest possible type
    and ranks.

    Args:
        hand (str): A string representing a wildcard hand.

    Returns:
        Tuple[int, ...]: A tuple where the first element is the hand's strength,
        followed by the ranks of the cards in the hand.
    """
    ranked_hand = []
    non_wildcard_hand = ""

    for char in hand:
        ranked_hand.append(WILDCARD_RANKS.index(char))

        if char != "J":  # Excluding wildcards ('J') from non-wildcard part.
            non_wildcard_hand += char

    all_hands = generate_all_wildcard_hands(non_wildcard_hand)
    max_hand_strength = None

    # Finding the strongest hand type among all wildcard combinations.
    for hand in all_hands:
        hand_strength = convert_hand_to_hand_type(hand)[0]

        if max_hand_strength is None or max_hand_strength < hand_strength:
            max_hand_strength = hand_strength

    assert max_hand_strength is not None
    return (max_hand_strength, *ranked_hand)


def calculate_winnings(lines: Iterable[str], is_wildcard_version: bool) -> int:
    """
    Calculates total winnings based on hand strengths and bids.

    Args:
        lines (Iterable[str]): An iterable collection of strings, each
        representing a line with a hand and a bid.
        is_wildcard_version (bool): A flag indicating if wildcard rules should
        be applied.

    Returns:
        int: The total winnings calculated based on hand rankings and
        corresponding bids.
    """
    hand_bid_pairs = scan_hand_bid_pairs(lines)
    type_bid_pairs = []

    for hand, bid in hand_bid_pairs:
        if not is_wildcard_version:
            hand_type = convert_hand_to_hand_type(hand)

        else:
            hand_type = convert_wildcard_hand_to_hand_type(hand)

        type_bid_pairs.append((hand_type, int(bid)))

    # Sorting hand types for ranking.
    type_bid_pairs = sorted(type_bid_pairs, key=lambda x: x[0])

    winnings = 0

    for i, type_bid_pair in enumerate(type_bid_pairs, start=1):
        winnings += type_bid_pair[1] * i  # Calculating winnings based on rank.

    return winnings


if __name__ == "__main__":
    # Main execution block.
    lines = list(helpers.generate_lines("2023/data/day_07.txt"))

    # Calculate and print winnings for both regular and wildcard versions.
    print(calculate_winnings(lines, False))
    print(calculate_winnings(lines, True))
