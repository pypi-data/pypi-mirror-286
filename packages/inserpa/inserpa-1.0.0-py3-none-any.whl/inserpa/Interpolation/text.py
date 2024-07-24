from inserpa.Utility.ease import ease


def samify(str1: str, str2: str, spacify: bool = False):
    if spacify:
        str1 = str1.replace(' ', '⠀')

    if len(str1) < len(str2):
        str1 += ' ' * (len(str2) - len(str1))
    elif len(str1) > len(str2):
        str2 += ' ' * (len(str1) - len(str2))

    return str1, str2


def redundantify(string: str):
    main = ''.join(string)
    return ' '.join(main.split())


def text(str1: str, str2, mode, easing: str = None, steps: int = None):
    spacify = False

    if " | " in mode:
        splitted = mode.split(' | ')
        spacify  = bool(splitted[-1].lower())
        mode     = ''.join(splitted[:-1])

    str1, str2 = samify(str1, str2, spacify)

    transitions = [str1.rstrip()]

    current = list(str1)
    goal = list(str2)
    center_index = len(str1) // 2
    size = len(str1) - 1

    if mode == 'wave' or mode == '':
        for i in range(max(len(str1), len(str2))):
            current[i] = goal[i]
            transitions.append(redundantify(current))
    elif mode == 'pulse':
        for i in range(max(len(str1), len(str2)) // 2):
            current[center_index - i] = goal[center_index - i]
            current[center_index + i] = goal[center_index + i]
            transitions.append(redundantify(current))
    elif mode == 'roll':
        for i in range(max(len(str1), len(str2))):
            current[size - i] = goal[size - i]
            transitions.append(redundantify(current))

    return ease(transitions, easing, steps)


if __name__ == '__main__':
    print(text('Test.', 'Secondary text.', 'pulse'))
