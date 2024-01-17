import day_12


def test_filter_possibilities() -> None:
    initial_condition = "???.###"
    arrangement = [1, 1, 3]

    possibilities = day_12.generate_possibilities(initial_condition)

    assert possibilities == [
        "....###",
        "..#.###",
        ".#..###",
        ".##.###",
        "#...###",
        "#.#.###",
        "##..###",
        "###.###",
    ]

    conditions = day_12.filter_possibilities(possibilities, arrangement)

    assert conditions == ["#.#.###"]


def test_calculate_total() -> None:
    document = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

    pairs = day_12.scan_conditions(document.split("\n"))

    assert day_12.calculate_total(pairs) == 21
