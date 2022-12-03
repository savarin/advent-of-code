def convert_to_priority(character: str) -> int:
    if character >= "a" and character <= "z":
        return ord(character) - 97 + 1

    elif character >= "A" and character <= "Z":
        return ord(character) - 65 + 27

    raise Exception("Exhaustive switch error.")


def test_convert_to_priority() -> None:
    assert convert_to_priority("a") == 1
    assert convert_to_priority("b") == 2
    assert convert_to_priority("c") == 3
    assert convert_to_priority("z") == 26
    assert convert_to_priority("A") == 27
    assert convert_to_priority("X") == 50
    assert convert_to_priority("Y") == 51
    assert convert_to_priority("Z") == 52


if __name__ == "__main__":
    test_convert_to_priority()

    priorities = 0

    with open("data/day_03.txt", "r") as f:
        for line in f:
            contents = line.strip()

            assert len(contents) % 2 == 0
            midpoint = len(contents) // 2

            both = set(contents[:midpoint]).intersection(contents[midpoint:])

            for character in both:
                priorities += convert_to_priority(character)

    print(priorities)

    priorities = 0
    lines = []

    with open("data/day_03.txt", "r") as f:
        for i, line in enumerate(f):
            lines.append(line.strip())

            if i % 3 == 2:
                common = (
                    set(lines[0])
                    .intersection(set(lines[1]))
                    .intersection(set(lines[2]))
                )

                assert len(common) == 1
                priorities += convert_to_priority(next(iter(common)))

                lines = []

    print(priorities)
