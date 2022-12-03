if __name__ == "__main__":
    outcome_by_choice_pair = {
        ("A", "X"): 3,
        ("A", "Y"): 6,
        ("A", "Z"): 0,
        ("B", "X"): 0,
        ("B", "Y"): 3,
        ("B", "Z"): 6,
        ("C", "X"): 6,
        ("C", "Y"): 0,
        ("C", "Z"): 3,
    }

    point_by_choice = {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }

    points = 0

    with open("data/day_02.txt", "r") as f:
        for line in f:
            opponent_choice, self_choice = line.strip().split(" ")
            points += (
                outcome_by_choice_pair[(opponent_choice, self_choice)]
                + point_by_choice[self_choice]
            )

    print(points)

    self_choice_by_outcome_pair = {
        ("A", "X"): "Z",
        ("A", "Y"): "X",
        ("A", "Z"): "Y",
        ("B", "X"): "X",
        ("B", "Y"): "Y",
        ("B", "Z"): "Z",
        ("C", "X"): "Y",
        ("C", "Y"): "Z",
        ("C", "Z"): "X",
    }

    point_by_outcome = {
        "X": 0,
        "Y": 3,
        "Z": 6,
    }

    points = 0

    with open("data/day_02.txt", "r") as f:
        for line in f:
            opponent_choice, outcome = line.strip().split(" ")
            self_choice = self_choice_by_outcome_pair[(opponent_choice, outcome)]

            points += point_by_outcome[outcome] + point_by_choice[self_choice]

    print(points)
