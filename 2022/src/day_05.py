from typing import DefaultDict, List, Tuple
import collections
import copy


if __name__ == "__main__":
    stack_by_stack_number: DefaultDict[int, List[str]] = collections.defaultdict(list)
    instructions: List[Tuple[int, int, int]] = []

    with open("data/day_05.txt", "r") as f:
        for line in f:
            if line[0] == "[":
                for i, char in enumerate(line.rstrip("\n")):
                    if (i - 1) % 4 == 0:
                        if char != " ":
                            stack_by_stack_number[((i - 1) // 4) + 1].append(char)

            if line[0] == "m":
                contents = line.rstrip("\n").split(" ")
                instructions.append(
                    (int(contents[1]), int(contents[3]), int(contents[5]))
                )

    # Reverse order of items in each stack.
    for stack_number, stack in stack_by_stack_number.items():
        stack_by_stack_number[stack_number] = stack_by_stack_number[stack_number][::-1]

    stack_by_stack_number_copy = copy.deepcopy(stack_by_stack_number)

    # Move item one-by-one.
    for instruction in instructions:
        count, from_stack, to_stack = instruction

        for i in range(count):
            item = stack_by_stack_number[from_stack].pop()
            stack_by_stack_number[to_stack].append(item)

    print("".join([stack[-1] for _, stack in sorted(stack_by_stack_number.items())]))

    # Move multiple items at a time.
    for instruction in instructions:
        count, from_stack, to_stack = instruction

        items = stack_by_stack_number_copy[from_stack][-count:]
        stack_by_stack_number_copy[from_stack] = stack_by_stack_number_copy[from_stack][
            :-count
        ]
        stack_by_stack_number_copy[to_stack] += items

    print(
        "".join([stack[-1] for _, stack in sorted(stack_by_stack_number_copy.items())])
    )
