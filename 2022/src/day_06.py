from typing import Counter, Optional
import collections
import queue


def find_marker(line: str, count: int) -> Optional[int]:
    items: queue.Queue = queue.Queue(count)
    counter: Counter = collections.Counter()

    for i, item_in in enumerate(line):
        if i > 0 and items.full():
            item_out = items.get()

            counter[item_out] -= 1

            if counter[item_out] == 0:
                del counter[item_out]

        items.put(item_in)
        counter[item_in] += 1

        if len(counter) == count:
            return i + 1

    return None


def test_find_marker():
    assert find_marker("abcde", 1) == 1
    assert find_marker("abcde", 3) == 3
    assert find_marker("abcde", 6) is None

    assert find_marker("abacd", 3) == 4
    assert find_marker("abacd", 4) == 5
    assert find_marker("abacd", 5) is None


if __name__ == "__main__":
    test_find_marker()

    with open("data/day_06.txt", "r") as f:
        for line in f:
            print(find_marker(line, 4))

    with open("data/day_06.txt", "r") as f:
        for line in f:
            print(find_marker(line, 14))
