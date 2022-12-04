def convert_to_int(s: str) -> int:
    result = 0

    start, end = [int(item) for item in s.split("-")]
    assert end >= start

    for position in range(start, end + 1):
        result = result | (1 << position)

    return result


def is_fully_covered(a: int, b: int) -> bool:
    if a == 0 or b == 0:
        return False

    return a | b == a or a | b == b


def has_overlap(a: int, b: int) -> bool:
    if a == 0 or b == 0:
        return False

    return a & b > 0


def test_convert_to_int() -> None:
    assert convert_to_int("1-1") == 2
    assert convert_to_int("1-2") == 6


def test_is_fully_covered() -> None:
    assert is_fully_covered(1, 3)
    assert is_fully_covered(3, 1)

    assert not is_fully_covered(1, 2)
    assert not is_fully_covered(2, 1)

    assert not is_fully_covered(1, 0)
    assert not is_fully_covered(0, 1)


def test_has_overlap() -> None:
    assert has_overlap(1, 3)
    assert not has_overlap(1, 2)


if __name__ == "__main__":
    test_is_fully_covered()
    test_convert_to_int()
    test_has_overlap()

    count = 0

    with open("data/day_04.txt", "r") as f:
        for line in f:
            first, second = line.rstrip("\n").split(",")

            count += int(
                is_fully_covered(convert_to_int(first), convert_to_int(second))
            )

    print(count)

    count = 0

    with open("data/day_04.txt", "r") as f:
        for line in f:
            first, second = line.rstrip("\n").split(",")

            count += int(has_overlap(convert_to_int(first), convert_to_int(second)))

    print(count)
