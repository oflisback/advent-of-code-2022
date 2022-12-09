def printgrid(rope):
    print(rope)
    print("Head pos: ", rope[9])
    tps = rope.copy()
    tps.reverse()
    for y in range(-10, 10):
        for x in range(-10, 20):
            if (x, y) == rope[9]:
                print("H", end="")
                continue
            if (x, y) in rope[:9]:
                tail_pos = tps.index((x, y))
                print(f"{str(tail_pos)}", end="")
                continue
            print(".", end="")
        print()
