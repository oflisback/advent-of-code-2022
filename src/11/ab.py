import re
from math import prod


def play(nbr_rounds, monkeys, op, num):
    denominators = [m["divby"] for m in monkeys]
    num = num if num is not None else prod(denominators)

    for _ in range(nbr_rounds):
        for m in monkeys:
            while len(m["items"]) > 0:
                item = m["items"].pop(0)
                m["nbr_inspect"] += 1
                new_value = eval(f"({m['expr']}){op}{num}".replace("old", str(item)))
                to = m["to_true"] if new_value % m["divby"] == 0 else m["to_false"]
                monkeys[int(to)]["items"].append(new_value)
    nbr_inspect = sorted([m["nbr_inspect"] for m in monkeys], reverse=True)

    return prod(nbr_inspect[:2])


def text_block_to_monkey(block):
    e = "items:(?P<items>[\S\s]*?)$[\s\S]*=(?P<expr>[\s\S]*?)$[\s\S]*?(?P<divby>[\d]+)[\s\S]*?(?P<to_true>[\d]+)[\s\S]*?(?P<to_false>[\d]+)"
    m = re.search(e, block, re.MULTILINE).groupdict()
    m["items"] = [int(i) for i in m["items"].split(",")]
    m["divby"] = int(m["divby"])

    return m | {"nbr_inspect": 0}


blocks = open("input.txt").read().split("\n\n")
for n, op, num in [(20, "//", 3), (10000, "%", None)]:
    monkeys = list(map(text_block_to_monkey, blocks))
    print(play(n, monkeys, op, num))
