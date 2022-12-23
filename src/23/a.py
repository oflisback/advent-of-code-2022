lines = open("input.txt").read().splitlines()


elves = []

for l_i, line in enumerate(lines):
    for c_i, char in enumerate(line):
        if char == "#":
            elves.append({"pos": (c_i, l_i), "proposition": None})

check_order = ["N", "S", "W", "E"]


def offsets_for_direction(direction):
    if direction == "N":
        return [(-1, -1), (0, -1), (1, -1)]
    elif direction == "S":
        return [(-1, 1), (0, 1), (1, 1)]
    elif direction == "E":
        return [(1, -1), (1, 0), (1, 1)]
    elif direction == "W":
        return [(-1, -1), (-1, 0), (-1, 1)]


def move_suggestion(direction):
    if direction == "N":
        return (0, -1)
    elif direction == "S":
        return (0, 1)
    elif direction == "E":
        return (1, 0)
    elif direction == "W":
        return (-1, 0)


def draw_elves(elves):
    min_x = min([e["pos"][0] for e in elves])
    max_x = max([e["pos"][0] for e in elves])
    min_y = min([e["pos"][1] for e in elves])
    max_y = max([e["pos"][1] for e in elves])
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in [e["pos"] for e in elves]:
                print("#", end="")
            else:
                print(".", end="")
        print()


print("== Initial State ==")
draw_elves(elves)
print()
print()

for round in range(10):
    proposed_targets = []
    elf_positions = [e["pos"] for e in elves]
    print("Starting round, check_order will be: ", check_order)
    print()
    # First half!
    for e in elves:
        # Check if there are elves around, if not, we shouldn't move or propose a move
        pos = e["pos"]
        no_neighbors = True
        for dir in check_order:
            offsets = offsets_for_direction(dir)
            places_to_check = [(pos[0] + o[0], pos[1] + o[1]) for o in offsets]
            if any([p in elf_positions for p in places_to_check]):
                no_neighbors = False
                break
        if no_neighbors:
            print("Elf at {} has no neighbors, will not move".format(pos))
        else:
            # Consider the positions around
            for dir in check_order:
                places_to_check = [
                    (pos[0] + o[0], pos[1] + o[1]) for o in offsets_for_direction(dir)
                ]
                if all([p not in elf_positions for p in places_to_check]):
                    move_offset = move_suggestion(dir)
                    e["proposition"] = (
                        pos[0] + move_offset[0],
                        pos[1] + move_offset[1],
                    )
                    proposed_targets.append(e["proposition"])
                    print(
                        "Elf at {} proposes move {} to {}".format(
                            pos, dir, e["proposition"]
                        )
                    )
                    break
            if e["proposition"] is None:
                print("Elf at {} has no move".format(e["pos"]))
    # Second half!
    for e in elves:
        if e["proposition"] is not None:
            if proposed_targets.count(e["proposition"]) == 1:
                print("Elf at {} moves to {}".format(e["pos"], e["proposition"]))
                e["pos"] = e["proposition"]
            else:
                print("Elf at {} does not move".format(e["pos"]))
            e["proposition"] = None
    # Finally
    check_order = check_order[1:] + [check_order[0]]
    #    draw_elves(elves)
    #    print()
    print("== End of Round {} ==".format(round + 1))
#    print()

min_x = min([e["pos"][0] for e in elves])
max_x = max([e["pos"][0] for e in elves])
min_y = min([e["pos"][1] for e in elves])
max_y = max([e["pos"][1] for e in elves])

free_space = 0
elf_positions = [e["pos"] for e in elves]
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        if (x, y) not in elf_positions:
            free_space += 1
print(free_space)
