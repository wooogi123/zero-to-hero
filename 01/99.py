def get_multiplier(target: int):
    return [target * i for i in range(1, 10)]


def print_multipliers(target: int, multipliers: list[int]):
    for index, multiple in enumerate(multipliers):
        print(f"{target} * {index} = {multiple}")


def main():
    target = int(input("Enter number: "))
    print_multipliers(target=target, multipliers=get_multiplier(target))


if __name__ == "__main__":
    main()
