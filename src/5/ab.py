from copy import deepcopy
from parse import search

lines = open("input.txt").read().splitlines()

startingStacks = []
instructions = []
stage = 0

for line in lines:
    if line == "":
        stage = 1
        continue
    if stage == 0:
        startingStacks.append(line)
    if stage == 1:
        instructions.append(line)

startingStacks.pop()
startingStacks.reverse()


def getNbrStacksFromStartingLine(line):
    return int((len(line[0]) + 1) / 4)


stacks = {}
nbrStacks = getNbrStacksFromStartingLine(startingStacks)
for i in range(nbrStacks):
    stacks[i] = []

for line in startingStacks:
    stackIndex = 0
    while len(line):
        if line.startswith("   "):
            stackIndex += 1
            line = line[4:]
        if line.startswith("["):
            stacks[stackIndex].append(line[1])
            line = line[4:]
            stackIndex += 1


def move_one(stacks, f, t, n):
    for n in range(n):
        val = stacks[f].pop()
        stacks[t].append(val)


def move_n(stacks, f, t, n):
    val = stacks[f][len(stacks[f]) - n : len(stacks[f])]
    stacks[f] = stacks[f][:-n]
    [stacks[t].append(v) for v in val]


def move(stacks, move_fn):
    st = deepcopy(stacks)
    for inst in instructions:
        [n, f, t] = search("move {:d} from {:d} to {:d}", inst)
        move_fn(st, f - 1, t - 1, n)
    print("".join([str(st[i].pop()) for i in range(nbrStacks)]))


move(stacks, move_one)
move(stacks, move_n)
