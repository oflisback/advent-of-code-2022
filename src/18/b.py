import sys

sys.setrecursionlimit(50000)

lines = open("input.txt").read().splitlines()

cubes = set()
for line in lines:
    cubes.add(tuple([int(v) for v in line.split(",")]))
[xr, yr, zr] = [v for v in zip(*cubes)]

surfaces = 0

direction = ["Up", "Left", "Down", "Right", "Front", "Back"]

# Populeras med (x,y,z,r) där r är en direction
found_surfaces = set()
# holds (x, y, z)
visited_non_cubes = set()

[bounds_x, bounds_y, bounds_z] = [
    [min(xr) - 1, max(xr) + 1],
    [min(yr) - 1, max(yr) + 1],
    [min(zr) - 1, max(zr) + 1],
]


def visit(x, y, z, d):
    print("Visiting ", x, y, z, d)
    if (x, y, z) in visited_non_cubes and (x, y, z) not in cubes:
        return
    visited_non_cubes.add((x, y, z))
    if (x, y, z) in cubes:
        if (x, y, z, d) not in found_surfaces:
            found_surfaces.add((x, y, z, d))
        return

    candidates = [
        (x, y, z + 1, "front"),
        (x, y, z - 1, "back"),
        (x - 1, y, z, "left"),
        (x + 1, y, z, "right"),
        (x, y + 1, z, "up"),
        (x, y - 1, z, "down"),
    ]
    for c in candidates:
        if (
            c[0] in range(bounds_x[0], bounds_x[1] + 1)
            and c[1] in range(bounds_y[0], bounds_y[1] + 1)
            and c[2] in range(bounds_z[0], bounds_z[1] + 1)
        ):
            visit(*c)


visit(min(xr) - 1, min(yr) - 1, min(zr) - 1, "front")

print("Nbr visited non cubes: ", len(visited_non_cubes))
print("Nbr found surfaces: ", len(found_surfaces))
