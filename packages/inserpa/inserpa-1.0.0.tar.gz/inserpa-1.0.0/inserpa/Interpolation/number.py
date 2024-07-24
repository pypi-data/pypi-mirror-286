from inserpa.Utility.ease import ease


def better_range(value1: int, value2: int):
    if value1 < value2:
        return list(range(value1, value2 + 1))
    elif value1 > value2:
        return list(range(value1, value2 - 1, -1))
    else:
        return [value1, value2]


def number(value1: int, value2: int, easing: str = None, steps: int = None):
    numbers = better_range(value1, value2)
    return ease(numbers, easing, steps)


if __name__ == '__main__':
    print(number(20, 10))
