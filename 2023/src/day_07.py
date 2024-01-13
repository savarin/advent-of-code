from typing import DefaultDict, Iterable, List, Sequence, Tuple
import collections
import dataclasses


import helpers


RANKS = "..23456789TJQKA"
WILDCARD_RANKS = "..J23456789TQKA"


@dataclasses.dataclass(frozen=True)
class RankCount:
    count: int
    rank: int


def scan_hand_bid_pairs(lines: Iterable[str]) -> List[Tuple[str, str]]:
    pairs = []

    for line in lines:
        line_index = 5

        hand = line[:line_index]
        line_index = helpers.parse_whitespace(line, line_index)
        bid, _ = helpers.parse_digits(line, line_index)

        pairs.append((hand, bid))

    return pairs


def evaluate_hand_strength(ranked_hand: Sequence[int]) -> int:
    counts = sorted(
        [(v, k) for k, v in collections.Counter(ranked_hand).items()], reverse=True
    )
    rank_counts = [RankCount(item[0], item[1]) for item in counts]

    if rank_counts[0].count == 5:
        return 6

    elif rank_counts[0].count == 4:
        assert rank_counts[1].count == 1
        return 5

    elif rank_counts[0].count == 3:
        if rank_counts[1].count == 2:
            return 4

        assert rank_counts[1].count == 1 and rank_counts[2].count == 1
        return 3

    elif rank_counts[0].count == 2:
        if rank_counts[1].count == 2:
            assert rank_counts[2].count == 1
            return 2

        assert (
            rank_counts[1].count == 1
            and rank_counts[2].count == 1
            and rank_counts[3].count == 1
        )
        return 1

    return 0


def convert_hand_to_hand_type(hand: str) -> Tuple[int, ...]:
    ranked_hand = [RANKS.index(char) for char in hand]
    hand_strength = evaluate_hand_strength(ranked_hand)

    return (hand_strength, *ranked_hand)


def generate_all_wildcard_hands(non_wildcard_hand: str) -> List[str]:
    if len(non_wildcard_hand) == 5:
        return [non_wildcard_hand]

    elif non_wildcard_hand == "":
        return ["AAAAA"]

    stack = [""]
    hands = []

    wildcard_count = 5 - len(non_wildcard_hand)

    while stack:
        item = stack.pop(0)

        for char in set(non_wildcard_hand):
            hand = item + char

            if len(hand) == wildcard_count:
                hands.append(hand)
                continue

            stack.append(hand)

    return [hand + non_wildcard_hand for hand in hands]


def convert_wildcard_hand_to_hand_type(hand: str) -> Tuple[int, ...]:
    ranked_hand = []
    non_wildcard_hand = ""

    for char in hand:
        ranked_hand.append(WILDCARD_RANKS.index(char))

        if char != "J":
            non_wildcard_hand += char

    all_hands = generate_all_wildcard_hands(non_wildcard_hand)
    max_hand_strength = None

    for hand in all_hands:
        hand_strength = convert_hand_to_hand_type(hand)[0]

        if max_hand_strength is None or max_hand_strength < hand_strength:
            max_hand_strength = hand_strength

    assert max_hand_strength is not None
    return (max_hand_strength, *ranked_hand)


def calculate_winnings(lines: Iterable[str], is_wildcard_version: bool) -> int:
    hand_bid_pairs = scan_hand_bid_pairs(lines)
    type_bid_pairs = []

    for hand, bid in hand_bid_pairs:
        if not is_wildcard_version:
            hand_type = convert_hand_to_hand_type(hand)

        else:
            hand_type = convert_wildcard_hand_to_hand_type(hand)

        type_bid_pairs.append((hand_type, int(bid)))

    type_bid_pairs = sorted(type_bid_pairs, key=lambda x: x[0])

    winnings = 0

    for i, type_bid_pair in enumerate(type_bid_pairs, start=1):
        winnings += type_bid_pair[1] * i

    return winnings


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
    lines = list(helpers.generate_lines("2023/data/day_07.txt"))

    print(calculate_winnings(lines, False))
    print(calculate_winnings(lines, True))
