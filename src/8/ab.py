from copy import copy

lines = open("input.txt").read().splitlines()


def get_reversed_index(length, index):
    return length - index - 1


def get_visible_indices(tree_heights):
    base_height = -1
    visible_indices = []
    for i in range(len(tree_heights)):
        if tree_heights[i] > base_height:
            visible_indices.append(i)
            base_height = tree_heights[i]
    return visible_indices


def get_column(heights, i):
    col = []
    for row in range(len(heights[0])):
        col.append(heights[row][i])
    return col


heights = []
for l in lines:
    heights.append([int(c) for c in list(l)])

global_visible_indices = []

for row in range(len(heights)):
    # left to right
    visible = get_visible_indices(heights[row])
    for vx in visible:
        global_visible_indices.append((vx, row))
    # right to left
    rev_row = copy(heights[row])
    rev_row.reverse()
    visible = get_visible_indices(rev_row)
    reversed = [get_reversed_index(len(rev_row), v) for v in visible]
    for vx in reversed:
        global_visible_indices.append((vx, row))
for col_index in range(len(heights[0])):
    # top to bottom
    col = get_column(heights, col_index)
    visible = get_visible_indices(col)
    for vy in visible:
        global_visible_indices.append((col_index, vy))
    # bottom to top
    rev_col = copy(col)
    rev_col.reverse()
    visible = get_visible_indices(rev_col)
    reversed = [get_reversed_index(len(rev_col), v) for v in visible]
    for vy in reversed:
        global_visible_indices.append((col_index, vy))

print(len(list(set(global_visible_indices))))


def get_scenic_score(x_start, y_start):
    # right
    start_height = heights[y_start][x_start]
    left_score = 0
    right_score = 0
    up_score = 0
    down_score = 0
    x = x_start + 1
    while x < len(heights[0]):
        if heights[y_start][x] < start_height:
            right_score += 1
            x += 1
        else:
            right_score += 1
            break
    x = x_start - 1
    while x >= 0:
        if heights[y_start][x] < start_height:
            left_score += 1
            x -= 1
        else:
            left_score += 1
            break
    y = y_start + 1
    while y < len(heights):
        if heights[y][x_start] < start_height:
            down_score += 1
            y += 1
        else:
            down_score += 1
            break
    y = y_start - 1
    while y >= 0:
        if heights[y][x_start] < start_height:
            up_score += 1
            y -= 1
        else:
            up_score += 1
            break
    return right_score * left_score * up_score * down_score


max_scenic_score = 0
for y in range(1, len(heights) - 1):
    for x in range(1, len(heights) - 1):
        score = get_scenic_score(x, y)
        if score > max_scenic_score:
            max_scenic_score = score

print(max_scenic_score)
