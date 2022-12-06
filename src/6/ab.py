l = open("input.txt").read()


def print_first_unique(window_len):
    window = []
    for index, c in enumerate(l):
        window.append(c)
        if len(window) > window_len:
            window.pop(0)
        if len(window) == window_len and len(set(window)) == window_len:
            print(str(index + 1))
            break


print_first_unique(4)
print_first_unique(14)
