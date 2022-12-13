from functools import cmp_to_key

non_empty_lines = filter(None, open("input.txt").read().splitlines())
packages = [(*eval(l),) for l in non_empty_lines]
debug = False


def list_cmp(a, b, level=0):
    level += 1
    while True:
        if len(a) > len(b) == 0:
            return -1
        if len(b) > len(a) == 0:
            return 1
        if len(a) == len(b) == 0:
            return 0
        val_a, *a = a
        val_b, *b = b
        res = 0
        if type(val_a) is not list and type(val_b) is not list:
            if val_a < val_b:
                res = 1
            if val_a > val_b:
                res = -1
        if isinstance(val_a, list) and isinstance(val_b, list):
            res = list_cmp(val_a, val_b, level + 1)
        if isinstance(val_a, list) and not isinstance(val_b, list):
            res = list_cmp(val_a, [val_b], level + 1)
        if not isinstance(val_a, list) and isinstance(val_b, list):
            res = list_cmp([val_a], val_b, level + 1)
        if res != 0:
            return res


right_order_indices = []
for i in range(0, len(packages), 2):
    if list_cmp(packages[i], packages[i + 1], 0) > 0:
        right_order_indices.append((i // 2) + 1)
print(sum(right_order_indices))

divs = [([2]), ([6])]
packages = sorted(packages + divs, key=cmp_to_key(list_cmp), reverse=True)
divider_positions = list(
    filter(
        None,
        map(lambda e: e[0] + 1 if e[1] in divs else 0, enumerate(packages)),
    )
)
print(divider_positions[0] * divider_positions[1])
