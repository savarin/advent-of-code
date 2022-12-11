from typing import Callable, List, Tuple
import dataclasses


def convert_to_action(
    level: int,
    operation: Callable[[int], int],
    divisor: int,
    receivers: Tuple[int, int],
) -> Tuple[int, int]:
    level = operation(level) // 3

    if level % divisor == 0:
        return level, receivers[0]

    return level, receivers[1]


@dataclasses.dataclass
class Agent:
    operation: Callable[[int], int]
    divisor: int
    receivers: Tuple[int, int]
    levels: List[int]

    def __post_init__(self) -> None:
        self.counter: int = 0

    def play(self) -> Tuple[int, int]:
        self.counter += 1
        return convert_to_action(
            self.levels.pop(0), self.operation, self.divisor, self.receivers
        )


def test_agent_play():
    agents = {}
    agents[0] = Agent(
        operation=lambda x: x * 19, divisor=23, receivers=(2, 3), levels=[79, 98]
    )
    agents[1] = Agent(
        operation=lambda x: x + 6, divisor=19, receivers=(2, 0), levels=[54, 65, 75, 75]
    )
    agents[2] = Agent(
        operation=lambda x: x * x, divisor=13, receivers=(1, 3), levels=[79, 60, 97]
    )
    agents[3] = Agent(
        operation=lambda x: x + 3, divisor=17, receivers=(0, 1), levels=[74]
    )

    for i in range(4):
        while len(agents[i].levels):
            level, recipient = agents[i].play()
            agents[recipient].levels.append(level)

    assert agents[0].levels == [20, 23, 27, 27]
    assert agents[1].levels == [2080, 25, 167, 207, 401, 1046]
    assert agents[2].levels == []
    assert agents[3].levels == []

    for i in range(4):
        while len(agents[i].levels):
            level, recipient = agents[i].play()
            agents[recipient].levels.append(level)

    assert agents[0].levels == [695, 10, 71, 135, 350]
    assert agents[1].levels == [43, 49, 58, 58, 362]
    assert agents[2].levels == []
    assert agents[3].levels == []


if __name__ == "__main__":
    test_agent_play()

    agents = {}
    agents[0] = Agent(
        operation=lambda x: x * 3,
        divisor=13,
        receivers=(6, 2),
        levels=[89, 73, 66, 57, 64, 80],
    )
    agents[1] = Agent(
        operation=lambda x: x + 1,
        divisor=3,
        receivers=(7, 4),
        levels=[83, 78, 81, 55, 81, 59, 69],
    )
    agents[2] = Agent(
        operation=lambda x: x * 13, divisor=7, receivers=(1, 4), levels=[76, 91, 58, 85]
    )
    agents[3] = Agent(
        operation=lambda x: x * x,
        divisor=2,
        receivers=(6, 0),
        levels=[71, 72, 74, 76, 68],
    )
    agents[4] = Agent(
        operation=lambda x: x + 7, divisor=19, receivers=(5, 7), levels=[98, 85, 84]
    )
    agents[5] = Agent(
        operation=lambda x: x + 8, divisor=5, receivers=(3, 0), levels=[78]
    )
    agents[6] = Agent(
        operation=lambda x: x + 4,
        divisor=11,
        receivers=(1, 2),
        levels=[86, 70, 60, 88, 88, 78, 74, 83],
    )
    agents[7] = Agent(
        operation=lambda x: x + 5, divisor=17, receivers=(3, 5), levels=[81, 58]
    )

    for _ in range(20):
        for i in range(8):
            while len(agents[i].levels):
                level, recipient = agents[i].play()
                agents[recipient].levels.append(level)

    targets = sorted([agents[i].counter for i in range(8)], reverse=True)[:2]
    print(targets[0] * targets[1])
