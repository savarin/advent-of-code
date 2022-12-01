if __name__ == "__main__":
    max_sum, current_sum = 0, 0

    with open("data/day_01.txt", "r") as f:
        for line in f:
            if line.strip() == "":
                if current_sum > max_sum:
                    max_sum = current_sum

                current_sum = 0
                continue

            current_sum += int(line)

    print(max_sum)

    first_sum, second_sum, third_sum, current_sum = 0, 0, 0, 0

    with open("data/day_01.txt", "r") as f:
        for line in f:
            if line.strip() == "":
                if current_sum > first_sum:
                    third_sum = second_sum
                    second_sum = first_sum
                    first_sum = current_sum

                elif current_sum > second_sum:
                    third_sum = second_sum
                    second_sum = current_sum

                elif current_sum > third_sum:
                    third_sum = current_sum

                current_sum = 0
                continue

            current_sum += int(line)

    print(first_sum + second_sum + third_sum)
