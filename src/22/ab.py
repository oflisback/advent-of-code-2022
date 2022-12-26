import pygame
from collections import defaultdict

lines = open("input.txt").read().splitlines()

headless = True

if not headless:
    pygame.init()


delimiter_index = lines.index("")
map_lines = lines[:delimiter_index]
instruction = lines[delimiter_index + 1]

height = 80
square_size = 5
screen_size = (1000, 1050)

if not headless:
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Calibri", 25, True, False)

nodes_on_each_line = []

max_row_width = 0
for line in map_lines:
    if len(line) > max_row_width:
        max_row_width = len(line)


def print_map(nodes_on_each_line):
    for nodes_on_line in nodes_on_each_line:
        for node in nodes_on_line:
            if not node:
                print(" ", end="")
                continue
            if node["last_visit"]:
                print(node["last_visit"], end="")
            else:
                print("#" if node["blocked"] else ".", end="")
        print()


for line_index, line in enumerate(map_lines):
    nodes_on_this_line = []
    prev_node = None
    first_node_on_line = None
    for col_index, c in enumerate(list(line)):
        if c == " ":
            nodes_on_this_line.append(None)
            continue

        node = {
            "blocked": c == "#",
            "col_index": col_index,
            "inst_index": None,
            "last_visit": None,
            "line_index": line_index,
            "right": None,
            "left": prev_node if prev_node else None,
            "up": None,
            "down": None,
        }
        if first_node_on_line is None:
            first_node_on_line = node
        nodes_on_this_line.append(node)
        if prev_node:
            node["left"] = prev_node
            prev_node["right"] = node
        prev_node = node
    if len(nodes_on_this_line) < max_row_width:
        nodes_on_this_line += [None] * (max_row_width - len(nodes_on_this_line))

    nodes_on_each_line.append(nodes_on_this_line)
    prev_line_nodes = nodes_on_this_line


nbr_cols = len(nodes_on_each_line[0])
nbr_rows = len(nodes_on_each_line)


def verify_grid():
    nbr_none = 0
    nbr_blocks = 0
    nbr_space = 0
    nbr_not_fully_connected = 0
    for row in range(nbr_rows):
        for column in range(nbr_cols):
            node = nodes_on_each_line[row][column]
            if node is None:
                nbr_none += 1
                continue
            if (
                node["up"] is None
                or node["down"] is None
                or node["left"] is None
                or node["right"] is None
            ):
                nbr_not_fully_connected += 1
                print(
                    "Not fully connected, col: ",
                    column,
                    " row: ",
                    row,
                    node["up"] is not None,
                    node["right"] is not None,
                    node["down"] is not None,
                    node["left"] is not None,
                )
            if node["blocked"]:
                nbr_blocks += 1
            else:
                nbr_space += 1

    pointers_dict = defaultdict(lambda: 0)
    for row in range(nbr_rows):
        for column in range(nbr_cols):
            node = nodes_on_each_line[row][column]
            if node is None:
                continue
            for n in [node["up"], node["right"], node["down"], node["left"]]:
                pointers_dict[(n["line_index"], n["col_index"])] += 1
    print("Max nbr pointers to a node: ", max(list(pointers_dict.values())))
    print("Min nbr pointers to a node: ", min(list(pointers_dict.values())))

    print("Nbr rows: ", nbr_rows)
    print("Nbr cols: ", nbr_cols)

    print("nbr none", nbr_none)
    print("nbr blocks", nbr_blocks)
    print("nbr space", nbr_space)
    print("nbr not fully connected", nbr_not_fully_connected)


def get_next_direction(cur_direction, instruction):
    if instruction == "R":
        if cur_direction == "up":
            return "right"
        elif cur_direction == "right":
            return "down"
        elif cur_direction == "down":
            return "left"
        elif cur_direction == "left":
            return "up"
    elif instruction == "L":
        if cur_direction == "up":
            return "left"
        elif cur_direction == "left":
            return "down"
        elif cur_direction == "down":
            return "right"
        elif cur_direction == "right":
            return "up"


direction_indicator = {
    "up": "^",
    "right": ">",
    "down": "v",
    "left": "<",
}


SIDE = 50


def debug_print_line(line):
    meh = []
    for node in line:
        if node is not None:
            meh.append("node")
        else:
            meh.append("None")
    print("Meh: ", meh)


# For each column, traverse it and update up and down links
for column in range(nbr_cols):
    first_node_on_col = None
    last_node_on_col = None
    for row in range(nbr_rows):
        line = nodes_on_each_line[row]
        node = line[column]
        if first_node_on_col is None and node is not None:
            first_node_on_col = node
        if node is not None:
            last_node_on_col = node
    for row in range(nbr_rows):
        node = nodes_on_each_line[row][column]
        if node is None:
            continue
        if row > 0:
            above_node = nodes_on_each_line[row - 1][column]
            node["up"] = above_node if above_node is not None else last_node_on_col
        if row < nbr_rows - 1:
            below_node = nodes_on_each_line[row + 1][column]
            node["down"] = below_node if below_node is not None else first_node_on_col


def is_tp_move(node1, node2):
    return (
        abs(node1["col_index"] - node2["col_index"]) > 1
        or abs(node1["line_index"] - node2["line_index"]) > 1
    )


def get_tp_direction(node, prev_node):
    if is_tp_move(node, node["up"]) and node["up"] == prev_node:
        return "up"
    if is_tp_move(node, node["right"]) and node["right"] == prev_node:
        return "right"
    if is_tp_move(node, node["down"]) and node["down"] == prev_node:
        return "down"
    if is_tp_move(node, node["left"]) and node["left"] == prev_node:
        return "left"


def opposite(direction):
    if direction == "up":
        return "down"
    if direction == "right":
        return "left"
    if direction == "down":
        return "up"
    if direction == "left":
        return "right"


def step_game(cur_node, cur_direction, inst_index, cur_number):
    if inst_index < len(instruction):

        if instruction[inst_index].isdigit():
            if cur_number is None:
                cur_number = instruction[inst_index]
            else:
                cur_number = cur_number + instruction[inst_index]
            inst_index += 1
            return [cur_node, cur_direction, inst_index, cur_number, False]
        else:
            if cur_number is not None:
                cur_number = int(cur_number)

                while cur_number > 0:
                    if cur_node[cur_direction]["blocked"]:
                        cur_number = 0
                        continue
                    if is_tp_move(cur_node, cur_node[cur_direction]):
                        did_tp_move = True
                    else:
                        did_tp_move = False
                    prev_node = cur_node
                    cur_node = cur_node[cur_direction]
                    if did_tp_move:
                        # Update direction, it happens to be the opposite of this node's tp direction
                        cur_direction = opposite(get_tp_direction(cur_node, prev_node))
                    cur_node["last_visit"] = direction_indicator[cur_direction]
                    cur_node["inst_index"] = inst_index
                    cur_number -= 1
                cur_number = None
            if instruction[inst_index] == "R":
                cur_direction = get_next_direction(cur_direction, "R")
                cur_node["last_visit"] = direction_indicator[cur_direction]
            elif instruction[inst_index] == "L":
                cur_direction = get_next_direction(cur_direction, "L")
                cur_node["last_visit"] = direction_indicator[cur_direction]
            cur_node["inst_index"] = inst_index
            inst_index += 1
            return [cur_node, cur_direction, inst_index, cur_number, False]
    if inst_index >= len(instruction):
        if cur_number:
            cur_number = int(cur_number)
            while cur_number > 0:
                if cur_node[cur_direction]["blocked"]:
                    cur_number = 0
                    continue
                cur_node = cur_node[cur_direction]
                cur_node["last_visit"] = direction_indicator[cur_direction]
                cur_node["inst_index"] = inst_index
                cur_number -= 1
            cur_number = None

        facing_point = {
            "right": 0,
            "down": 1,
            "left": 2,
            "up": 3,
        }

        result = (
            1000 * (cur_node["line_index"] + 1)
            + (cur_node["col_index"] + 1) * 4
            + facing_point[cur_direction]
        )
        print(result)
        return [cur_node, cur_direction, inst_index, cur_number, True]


def draw_square(node, y, x, inst_index):
    color = (0, 255, 0)
    if node["blocked"]:
        color = (0, 0, 0)
    if (
        node["last_visit"] is not None
        and "inst_index" in node
        and node["inst_index"] is not None
        and node["inst_index"] > inst_index - 100
    ):
        color = (255, 0, 0)
    if (
        node["last_visit"] is not None
        and "inst_index" in node
        and node["inst_index"] is not None
        and node["inst_index"] > inst_index - 10
    ):
        color = (0, 0, 255)

    pygame.draw.rect(
        screen,
        color,
        (
            100 + x * square_size,
            30 + square_size * y,
            square_size,
            square_size,
        ),
    )


def play():
    cur_number = None
    delay = 0
    cur_node = nodes_on_each_line[0][50]
    cur_direction = "right"
    done = False
    inst_index = 0
    cur_node["last_visit"] = direction_indicator[cur_direction]
    prev_draw_tick = 0

    if not headless:
        for col in range(nbr_cols):
            for row in range(nbr_rows):
                if nodes_on_each_line[row][col] is not None:
                    nodes_on_each_line[row][col]["inst_index"] = None
                    nodes_on_each_line[row][col]["last_visit"] = None

    verify_grid()

    while not done:
        if headless:
            [cur_node, cur_direction, inst_index, cur_number, done] = step_game(
                cur_node, cur_direction, inst_index, cur_number
            )
            if done:
                return
            continue

        screen.fill((255, 255, 255))

        # Draw the existing blocks
        for row_index, row in enumerate(nodes_on_each_line):
            for col_index, node in enumerate(row):
                if node != None:
                    draw_square(node, row_index, col_index, inst_index)

        pygame.display.flip()

        cur_tick = pygame.time.get_ticks()
        if cur_tick - prev_draw_tick > delay:
            prev_draw_tick = cur_tick

        [cur_node, cur_direction, inst_index, cur_number, done] = step_game(
            cur_node, cur_direction, inst_index, cur_number
        )

        clock.tick(60)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            done = True
        if keys[pygame.K_LEFT]:
            delay = delay * 1.1
        if keys[pygame.K_RIGHT]:
            delay = delay * 0.9

        pygame.event.pump()


def get_range(reverse=False):
    return range(SIDE) if reverse == False else range(SIDE - 1, -1, -1)


def get_coords(sidespec, reverse=False):
    offset_row = SIDE * sidespec["square"][0]
    offset_col = SIDE * sidespec["square"][1]
    if sidespec["side"] == "up":
        return [(offset_row, offset_col + i) for i in get_range(reverse)]
    if sidespec["side"] == "down":
        return [(offset_row + SIDE - 1, offset_col + i) for i in get_range(reverse)]
    if sidespec["side"] == "left":
        return [(offset_row + i, offset_col) for i in get_range(reverse)]
    if sidespec["side"] == "right":
        return [(offset_row + i, SIDE + offset_col - 1) for i in get_range(reverse)]


# Takes a list of side specs, length 2
# A sidespec is e.g. { "side": "up", "square": (1, 0)}
# where square is the coords in the grid containing the cube squares
def connect(sidespecs, reverse=False):
    coords_1 = get_coords(sidespecs[0], reverse)
    coords_2 = get_coords(sidespecs[1])
    for c_i, coord in enumerate(coords_1):
        [row, col] = coord
        node_1 = nodes_on_each_line[row][col]
        node_2 = nodes_on_each_line[coords_2[c_i][0]][coords_2[c_i][1]]
        node_1[sidespecs[0]["side"]] = node_2
        node_2[sidespecs[1]["side"]] = node_1


# Connect sides for A
connect(
    [{"side": "left", "square": (0, 1)}, {"side": "right", "square": (0, 2)}]
)  # 1 left to 2 right

connect(
    [{"side": "left", "square": (1, 1)}, {"side": "right", "square": (1, 1)}]
)  # 3 left to 3 right

connect(
    [{"side": "left", "square": (2, 0)}, {"side": "right", "square": (2, 1)}]
)  # 4 left to 5 right

connect(
    [{"side": "left", "square": (3, 0)}, {"side": "right", "square": (3, 0)}]
)  # 6 left to 6 right

connect(
    [{"side": "up", "square": (2, 0)}, {"side": "down", "square": (3, 0)}]
)  # 4 up to 6 down
connect(
    [{"side": "up", "square": (0, 1)}, {"side": "down", "square": (2, 1)}]
)  # 1 up to 5 down
connect(
    [{"side": "up", "square": (0, 2)}, {"side": "down", "square": (0, 2)}]
)  # 2 up to 2 down

play()

# Connect sides for b
connect(
    [{"side": "up", "square": (0, 1)}, {"side": "left", "square": (3, 0)}]
)  # 1 up to 6 left
connect(
    [{"side": "up", "square": (0, 2)}, {"side": "down", "square": (3, 0)}]
)  # 2 up to 6 down
connect(
    [{"side": "left", "square": (0, 1)}, {"side": "left", "square": (2, 0)}],
    reverse=True,
)  # 1 left to 4 left
connect(
    [{"side": "right", "square": (0, 2)}, {"side": "right", "square": (2, 1)}],
    reverse=True,
)  # 2 right to 5 right
connect(
    [{"side": "down", "square": (0, 2)}, {"side": "right", "square": (1, 1)}]
)  # 2 down to 3 right
connect(
    [{"side": "left", "square": (1, 1)}, {"side": "up", "square": (2, 0)}]
)  # 3 left to 4 up
connect(
    [{"side": "down", "square": (2, 1)}, {"side": "right", "square": (3, 0)}]
)  # 5 down to 6 right

play()
