from typing import List, Tuple


def run_instructions(instructions: List[str], cycles: List[int]) -> Tuple[int, str]:
    register = 1
    counter = 1
    add = None
    position = (0, 1, 2)

    strength = 0
    pixels = ""

    while True:
        pixels += "#" if (counter - 1) % 40 in position else "."

        if add is not None:
            register += add
            add = None
            counter += 1
            position = (register - 1, register, register + 1)

        else:
            items = instructions.pop(0).split(" ")

            if items[0] == "noop":
                counter += 1

            elif items[0] == "addx":
                add = int(items[1])
                counter += 1

            else:
                raise Exception("Exhaustive switch error.")

        if len(cycles) > 0 and cycles[0] == counter:
            strength += counter * register
            cycles.pop(0)

        if len(instructions) == 0 and add is None:
            break

    return strength, pixels


def test_run_instructions() -> None:
    instructions = [
        "addx 15",
        "addx -11",
        "addx 6",
        "addx -3",
        "addx 5",
        "addx -1",
        "addx -8",
        "addx 13",
        "addx 4",
        "noop",
        "addx -1",
        "addx 5",
        "addx -1",
        "addx 5",
        "addx -1",
        "addx 5",
        "addx -1",
        "addx 5",
        "addx -1",
        "addx -35",
        "addx 1",
        "addx 24",
        "addx -19",
        "addx 1",
        "addx 16",
        "addx -11",
        "noop",
        "noop",
        "addx 21",
        "addx -15",
        "noop",
        "noop",
        "addx -3",
        "addx 9",
        "addx 1",
        "addx -3",
        "addx 8",
        "addx 1",
        "addx 5",
        "noop",
        "noop",
        "noop",
        "noop",
        "noop",
        "addx -36",
        "noop",
        "addx 1",
        "addx 7",
        "noop",
        "noop",
        "noop",
        "addx 2",
        "addx 6",
        "noop",
        "noop",
        "noop",
        "noop",
        "noop",
        "addx 1",
        "noop",
        "noop",
        "addx 7",
        "addx 1",
        "noop",
        "addx -13",
        "addx 13",
        "addx 7",
        "noop",
        "addx 1",
        "addx -33",
        "noop",
        "noop",
        "noop",
        "addx 2",
        "noop",
        "noop",
        "noop",
        "addx 8",
        "noop",
        "addx -1",
        "addx 2",
        "addx 1",
        "noop",
        "addx 17",
        "addx -9",
        "addx 1",
        "addx 1",
        "addx -3",
        "addx 11",
        "noop",
        "noop",
        "addx 1",
        "noop",
        "addx 1",
        "noop",
        "noop",
        "addx -13",
        "addx -19",
        "addx 1",
        "addx 3",
        "addx 26",
        "addx -30",
        "addx 12",
        "addx -1",
        "addx 3",
        "addx 1",
        "noop",
        "noop",
        "noop",
        "addx -9",
        "addx 18",
        "addx 1",
        "addx 2",
        "noop",
        "noop",
        "addx 9",
        "noop",
        "noop",
        "noop",
        "addx -1",
        "addx 2",
        "addx -37",
        "addx 1",
        "addx 3",
        "noop",
        "addx 15",
        "addx -21",
        "addx 22",
        "addx -6",
        "addx 1",
        "noop",
        "addx 2",
        "addx 1",
        "noop",
        "addx -10",
        "noop",
        "noop",
        "addx 20",
        "addx 1",
        "addx 2",
        "addx 2",
        "addx -6",
        "addx -11",
        "noop",
        "noop",
        "noop",
    ]

    strength, pixels = run_instructions(instructions, [20, 60, 100, 140, 180, 220])
    assert strength == 13140

    assert pixels[0:40] == "##..##..##..##..##..##..##..##..##..##.."
    assert pixels[40:80] == "###...###...###...###...###...###...###."
    assert pixels[80:120] == "####....####....####....####....####...."
    assert pixels[120:160] == "#####.....#####.....#####.....#####....."
    assert pixels[160:200] == "######......######......######......####"
    assert pixels[200:240] == "#######.......#######.......#######....."


if __name__ == "__main__":
    test_run_instructions()

    instructions = []

    with open("data/day_10.txt", "r") as f:
        for line in f:
            instructions.append(line.rstrip("\n"))

    strength, pixels = run_instructions(instructions, [20, 60, 100, 140, 180, 220])

    print(strength)

    for i in range(6):
        print(pixels[i * 40 : (i + 1) * 40])
