lines = open("input.txt").read().splitlines()

cubes = []
for line in lines:
    cubes.append([int(v) for v in line.split(",")])

[xr, yr, zr] = [v for v in zip(*cubes)]

y = 1
surfaces = 0
for z in range(min(zr), max(zr) + 1):
    surfaces_on_z_plane = 0
    for y in range(min(yr), max(yr) + 1):
        surfaces_on_row = 0
        cubes_by_x_on_row = sorted(
            [c for c in cubes if c[1] == y and c[2] == z], key=lambda x: x[0]
        )
        gaps = 0
        for c_i, c in enumerate(cubes_by_x_on_row):
            if c[0] - cubes_by_x_on_row[c_i - 1][0] > 1:
                gaps += 1
        s = 0 if len(cubes_by_x_on_row) == 0 else gaps * 2 + 2
        if s > 0:
            print("Adding surfaces on row: ", s)
        surfaces_on_z_plane += s
    for x in range(min(xr), max(xr) + 1):
        surfaces_on_col = 0
        cubes_by_y_on_col = sorted(
            [c for c in cubes if c[0] == x and c[2] == z], key=lambda x: x[1]
        )
        gaps = 0
        for c_i, c in enumerate(cubes_by_y_on_col):
            if c[1] - cubes_by_y_on_col[c_i - 1][1] > 1:
                gaps += 1
        s = 0 if len(cubes_by_y_on_col) == 0 else gaps * 2 + 2
        if s > 0:
            print("Adding surfaces on col: ", s)
        surfaces_on_z_plane += s
    surfaces += surfaces_on_z_plane

for x in range(min(xr), max(xr) + 1):
    surfaces_on_x_plane = 0
    for y in range(min(yr), max(yr) + 1):
        cubes_by_z_depth = sorted(
            [c for c in cubes if c[0] == x and c[1] == y], key=lambda x: x[2]
        )
        gaps = 0
        for c_i, c in enumerate(cubes_by_z_depth):
            if c[2] - cubes_by_z_depth[c_i - 1][2] > 1:
                gaps += 1
        s = 0 if len(cubes_by_z_depth) == 0 else gaps * 2 + 2
        if s > 0:
            print("Adding surfaces on depth: ", s)
        surfaces_on_x_plane += s
    surfaces += surfaces_on_x_plane


print(surfaces)
