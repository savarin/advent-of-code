import day_08


def test_follow_directions() -> None:
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
    assert day_08.follow_directions_single(instructions, directions) == 2

    document = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

    instructions, directions = day_08.scan_map(document.split("\n"))
    assert day_08.follow_directions_single(instructions, directions) == 6
