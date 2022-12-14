# from copy import deepcopy

lines = open("input.txt").read().splitlines()

min_x = 10000
max_x = min_y = max_y = 0

X = 0
Y = 1

paths = []
for l in lines:
    path = [c.strip().split(",") for c in l.split("->")]
    path = [(int(c[0]), int(c[1])) for c in path]
    path_min_x = min([c[X] for c in path])
    min_x = path_min_x if path_min_x < min_x else min_x
    path_max_x = max([c[X] for c in path])
    max_x = path_max_x if path_max_x > max_x else max_x
    path_min_y = min([c[Y] for c in path])
    min_y = path_min_y if path_min_y < min_y else min_y
    path_max_y = max([c[Y] for c in path])
    max_y = 2 + path_max_y if path_max_y > max_y else max_y
    paths.append(path)

min_x -= max_y
max_x += max_y


def fill_grid_from_paths(grid, paths):
    for path in paths:
        for coord_index, coord in enumerate(path):
            grid[coord[Y]][coord[X] - min_x] = 1
            if coord_index == len(path) - 1:
                break
            if path[coord_index + 1][X] > path[coord_index][X]:
                for cx in range(0, path[coord_index + 1][X] - path[coord_index][X]):
                    grid[coord[Y]][coord[X] + cx - min_x] = 1
            elif path[coord_index + 1][X] < path[coord_index][X]:
                for cx in range(0, path[coord_index + 1][X] - path[coord_index][X], -1):
                    grid[coord[Y]][coord[X] + cx - min_x] = 1
            elif path[coord_index + 1][Y] > path[coord_index][Y]:
                for cy in range(0, path[coord_index + 1][Y] - path[coord_index][Y]):
                    grid[coord[Y] + cy][coord[X] - min_x] = 1
            else:
                for cy in range(0, path[coord_index + 1][Y] - path[coord_index][Y], -1):
                    grid[coord[Y] + cy][coord[X] - min_x] = 1
    for cx in range(0, max_x - min_x + 1):
        grid[max_y][cx] = 1


grid = [] * (max_y + 1)
for _ in range(min_y, max_y + 1):
    grid.append([0] * (max_x - min_x + 1))
fill_grid_from_paths(grid, paths)
grid[0][500 - min_x] = 2
found_first = False


def add_and_step_sand(grid, sand_coord_start, min_x):
    global found_first
    sand_coord = sand_coord_start
    while True:
        if grid[sand_coord[Y] + 1][sand_coord[X] - min_x] == 0:
            sand_coord = (sand_coord[X], sand_coord[Y] + 1)
        elif grid[sand_coord[Y] + 1][sand_coord[X] - min_x - 1] == 0:
            sand_coord = (sand_coord[X] - 1, sand_coord[Y] + 1)
        elif grid[sand_coord[Y] + 1][sand_coord[X] - min_x + 1] == 0:
            sand_coord = (sand_coord[X] + 1, sand_coord[Y] + 1)
        elif sand_coord[X] == 500 and sand_coord[Y] == 0:
            raise IndexError
        else:
            break
    if not found_first and sand_coord[Y] == max_y - 1:
        print("First outside edge: ", nbr_sand - 1)
        found_first = True
    grid[sand_coord[Y]][sand_coord[X] - min_x] = 3


nbr_sand = 0
while True:
    nbr_sand += 1
    try:
        add_and_step_sand(grid, (500, 0), min_x)
    except IndexError:
        print("Nbr sand to reach source coord: ", nbr_sand)
        break
