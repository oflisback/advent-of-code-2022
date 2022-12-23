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


elves_moved = 1
round = 0
while elves_moved > 0:
    print("Last round", round, elves_moved, "elves moved")
    round += 1
    elves_moved = 0
    proposed_targets_1 = set()
    proposed_targets_2 = set()
    elf_positions = [e["pos"] for e in elves]
    # First half!
    for e in elves:
        pos = e["pos"]
        e["proposition"] = None
        neighbors = False
        for dir in check_order:
            offsets = offsets_for_direction(dir)
            places_to_check = [(pos[0] + o[0], pos[1] + o[1]) for o in offsets]
            nbr_elfs_in_direction = len(
                [p for p in places_to_check if p in elf_positions]
            )
            if nbr_elfs_in_direction > 0:
                neighbors = True
                if e["proposition"] is not None:
                    break
                continue
            if nbr_elfs_in_direction == 0 and e["proposition"] is None:
                move_offset = move_suggestion(dir)
                e["proposition"] = (
                    pos[0] + move_offset[0],
                    pos[1] + move_offset[1],
                )
                if neighbors:
                    break
        if neighbors:
            if e["proposition"] in proposed_targets_1:
                proposed_targets_2.add(e["proposition"])
            else:
                proposed_targets_1.add(e["proposition"])
        else:
            e["proposition"] = None
    # Second half!
    for e in [e for e in elves if e["proposition"] is not None]:
        if e["proposition"] not in proposed_targets_2:
            e["pos"] = e["proposition"]
            elves_moved += 1
        e["proposition"] = None
    # Finally
    check_order = check_order[1:] + [check_order[0]]

print(round)
