from typing import DefaultDict, Iterable, List, Tuple
import collections
import dataclasses


import helpers


RANKS = "..23456789TJQKA"


def calculate_winnings(lines: Iterable[str]) -> int:
    hand_bid_pairs = scan_hand_bid_pairs(lines)
    type_bid_pairs = []

    for hand, bid in hand_bid_pairs:
        hand_type = convert_hand_to_custom_type(hand)
        type_bid_pairs.append((hand_type, int(bid)))

    type_bid_pairs = sorted(type_bid_pairs, key=lambda x: x[0])

    winnings = 0

    for i, type_bid_pair in enumerate(type_bid_pairs, start=1):
        winnings += type_bid_pair[1] * i

    return winnings


def scan_hand_bid_pairs(lines: Iterable[str]) -> List[Tuple[str, str]]:
    pairs = []

    for line in lines:
        line_index = 5

        hand = line[:line_index]
        line_index = helpers.parse_whitespace(line, line_index)
        bid, _ = helpers.parse_digits(line, line_index)

        pairs.append((hand, bid))

    return pairs


def convert_hand_to_custom_type(hand: str) -> Tuple[int, ...]:
    count: DefaultDict[int, int] = collections.defaultdict(int)
    custom_hand = []

    for char in hand:
        char_rank = RANKS.index(char)
        custom_hand.append(char_rank)
        count[char_rank] += 1

    reverse_count = sorted([(v, k) for k, v in count.items()], reverse=True)
    reverse = [RankCount(*item) for item in reverse_count]

    if reverse[0].count == 5:
        return (6, *custom_hand)

    elif reverse[0].count == 4:
        assert reverse[1].count == 1
        return (5, *custom_hand)

    elif reverse[0].count == 3:
        if reverse[1].count == 2:
            return (4, *custom_hand)

        assert reverse[1].count == 1 and reverse[2].count == 1
        return (3, *custom_hand)

    elif reverse[0].count == 2:
        if reverse[1].count == 2:
            assert reverse[2].count == 1
            return (2, *custom_hand)

        assert reverse[1].count == 1 and reverse[2].count == 1 and reverse[3].count == 1
        return (1, *custom_hand)

    return (0, *custom_hand)


@dataclasses.dataclass(frozen=True)
class RankCount:
    count: int
    rank: int


def convert_hand_to_reverse_rank_count(hand: str) -> List[RankCount]:
    count: DefaultDict[int, int] = collections.defaultdict(int)

    for char in hand:
        count[RANKS.index(char)] += 1

    reverse_count = sorted([(v, k) for k, v in count.items()], reverse=True)
    return [RankCount(*item) for item in reverse_count]


def convert_reverse_rank_count_to_hand_type(
    reverse: List[RankCount],
) -> Tuple[int, ...]:
    if reverse[0].count == 5:
        return (6, reverse[0].rank, 0, 0, 0, 0)

    elif reverse[0].count == 4:
        assert reverse[1].count == 1
        return (5, reverse[0].rank, reverse[1].rank, 0, 0, 0)

    elif reverse[0].count == 3:
        if reverse[1].count == 2:
            return (4, reverse[0].rank, reverse[1].rank, 0, 0, 0)

        assert reverse[1].count == 1 and reverse[2].count == 1
        return (3, reverse[0].rank, reverse[1].rank, reverse[2].rank, 0, 0)

    elif reverse[0].count == 2:
        if reverse[1].count == 2:
            assert reverse[2].count == 1
            return (2, reverse[0].rank, reverse[1].rank, reverse[2].rank, 0, 0)

        assert reverse[1].count == 1 and reverse[2].count == 1 and reverse[3].count == 1
        return (
            1,
            reverse[0].rank,
            reverse[1].rank,
            reverse[2].rank,
            reverse[3].rank,
            0,
        )

    return (
        0,
        reverse[0].rank,
        reverse[1].rank,
        reverse[2].rank,
        reverse[3].rank,
        reverse[4].rank,
    )


if __name__ == "__main__":
    lines = helpers.generate_lines("2023/data/day_07.txt")
    print(calculate_winnings(lines))
