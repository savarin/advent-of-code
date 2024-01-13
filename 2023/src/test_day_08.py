import day_08


def test_follow_directions_single() -> None:
    document = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

    instructions, directions = day_08.scan_map(document.split("\n"))
    assert (
        day_08.follow_directions_single(
            instructions, directions, "AAA", lambda x: x != "ZZZ"
        )
        == 2
    )

    document = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

    instructions, directions = day_08.scan_map(document.split("\n"))
    assert (
        day_08.follow_directions_single(
            instructions, directions, "AAA", lambda x: x != "ZZZ"
        )
        == 6
    )


def test_follow_directions_multiple() -> None:
    document = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

    instructions, directions = day_08.scan_map(document.split("\n"))
    assert day_08.follow_directions_multiple(instructions, directions) == 6
