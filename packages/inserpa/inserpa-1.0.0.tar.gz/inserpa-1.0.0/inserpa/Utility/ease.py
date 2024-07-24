from inserpa.Utility.easing_functions import EasingFunctions


def get_ease_function(string):
    return getattr(EasingFunctions, string.replace(' ', '_'))


def ease(base: list, easing: str, steps):
    if easing is None: easing = 'linear'
    if steps is None: steps = len(base)

    func = get_ease_function(easing)

    percentage_step = len(base) / (steps - 1)

    result = []

    for i in range(steps):
        percentage = func(min(percentage_step * (i / steps), 1))

        index = int(percentage * (len(base) - 1))
        index = max(min(index, len(base) - 1), 0)

        result.append(base[index])

    return result
