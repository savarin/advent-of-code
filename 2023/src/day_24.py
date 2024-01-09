from typing import Optional, Tuple
import dataclasses

import helpers


@dataclasses.dataclass(frozen=True)
class Vector:
    x: int
    y: int
    z: int


@dataclasses.dataclass(frozen=True)
class Hailstone:
    position: Vector
    velocity: Vector


def parse_hailstone(line: str) -> Hailstone:
    line_index = 0
    item_counter = 0

    items = []

    while line_index < len(line):
        match item_counter:
            # expect: digits comma space
            case 0 | 1:
                digits, line_index = helpers.parse_digits(line, line_index)
                items.append(int(digits))
                item_counter += 1

                line_index = helpers.expect(line, line_index, ",")
                line_index = helpers.expect(line, line_index, " ")

            # expect: digits space at space
            case 2:
                digits, line_index = helpers.parse_digits(line, line_index)
                items.append(int(digits))
                item_counter += 1

                line_index = helpers.expect(line, line_index, " ")
                line_index = helpers.expect(line, line_index, "@")
                line_index = helpers.expect(line, line_index, " ")

            # expect: digits comma space
            case 3 | 4:
                digits, line_index = helpers.parse_digits(line, line_index)
                items.append(int(digits))
                item_counter += 1

                line_index = helpers.expect(line, line_index, ",")
                line_index = helpers.expect(line, line_index, " ")

            # expect: digits EOL
            case 5:
                digits, line_index = helpers.parse_digits(line, line_index)
                items.append(int(digits))

                if line_index != len(line):
                    raise ValueError("Expected EOL after item 5.")

            case _:
                raise ValueError("Expected exactly 6 items.")

    position = Vector(*items[:3])
    velocity = Vector(*items[3:])
    return Hailstone(position, velocity)


def calculate_line_coefficients_2d(h: Hailstone) -> Tuple[float, float]:
    # y = mx + c
    # m = v_y / v_x
    # c = p_y - m * p_x
    slope = h.velocity.y / h.velocity.x
    y_intercept = h.position.y - slope * h.position.x

    return slope, y_intercept


def calculate_intersection_2d(
    h_1: Hailstone, h_2: Hailstone
) -> Optional[Tuple[float, float]]:
    m_1, c_1 = calculate_line_coefficients_2d(h_1)
    m_2, c_2 = calculate_line_coefficients_2d(h_2)

    if m_1 == m_2:
        return None

    # Inverse matrix representing
    #   y = m_1 * x + c_1
    #   y = m_2 * x + c_2
    determinant = -m_1 + m_2
    x = (c_1 - c_2) / determinant
    y = (m_2 * c_1 - m_1 * c_2) / determinant

    return x, y


if __name__ == "__main__":
    lines = helpers.generate_lines("2023/data/day_04.txt")
    hailstones = []

    for line in lines:
        hailstones.append(parse_hailstone(line))

    counter = 0

    for i, h_1 in enumerate(hailstones):
        for h_2 in hailstones[i + 1 :]:
            intersection = calculate_intersection_2d(h_1, h_2)

            if (
                intersection is not None
                and intersection[0] >= 200000000000000
                and intersection[0] <= 400000000000000
                and intersection[1] >= 200000000000000
                and intersection[1] <= 400000000000000
                and (intersection[0] - h_1.position.x) / h_1.velocity.x > 0
                and (intersection[0] - h_2.position.x) / h_2.velocity.x > 0
            ):
                counter += 1

    print(counter)
