from copy import deepcopy
from functools import cache

lines = open("input.txt").read().splitlines()

W = len(lines[0])
H = len(lines)

org_valley = []
empty_valley = []

for x in range(W):
    col = []
    empty_valley_col = []
    for y in range(H):
        col.append([lines[y][x]])
        if lines[y][x] == "#":
            empty_valley_col.append(["#"])
        else:
            empty_valley_col.append(["."])
    org_valley.append(col)
    empty_valley.append(empty_valley_col)


def print_valley(valley, p=None):
    for y in range(H):
        for x in range(W):
            if (x, y) == p:
                print("E", end="")
                continue
            if len(valley[x][y]) == 0:
                print(".", end="")
            elif len(valley[x][y]) == 1:
                print(valley[x][y][0], end="")
            else:
                print(len(valley[x][y]), end="")
        print()
    print()


def get_next_valley(prev_valley):
    next_valley = deepcopy(empty_valley)

    for x in range(1, W - 1):
        for y in range(1, H - 1):
            # start off with next_valley[x][y] since it may contain an opposite spawned
            # blizzard already.
            cur = [s for s in next_valley[x][y] if s != "."]
            if "<" in prev_valley[x][y] and prev_valley[x - 1][y] == ["#"]:
                next_valley[W - 2][y].append("<")
            if ">" in prev_valley[x][y] and prev_valley[x + 1][y] == ["#"]:
                next_valley[1][y].append(">")
            if "v" in prev_valley[x][y] and prev_valley[x][y + 1] == ["#"]:
                next_valley[x][1].append("v")
            if "^" in prev_valley[x][y] and prev_valley[x][y - 1] == ["#"]:
                next_valley[x][H - 2].append("^")
            if ">" in prev_valley[x - 1][y]:
                cur.append(">")
            if "<" in prev_valley[x + 1][y]:
                cur.append("<")
            if "v" in prev_valley[x][y - 1]:
                cur.append("v")
            if "^" in prev_valley[x][y + 1]:
                cur.append("^")
            next_valley[x][y] = cur
    return next_valley


@cache
def get_valley_at_minute(minute):
    if minute > 0:
        prev_valley = get_valley_at_minute(minute - 1)
        return get_next_valley(prev_valley)
    return deepcopy(org_valley)


def get_desc(p, prev, minute):
    if minute == 0:
        return "Initial state"
    if p == prev:
        return "Waiting"
    if p[0] < prev[0]:
        return "Moving left"
    if p[0] > prev[0]:
        return "Moving right"
    if p[1] < prev[1]:
        return "Moving up"
    if p[1] > prev[1]:
        return "Moving down"


def mh_to_goal(p, goal):
    return abs(p[0] - goal[0]) + abs(p[1] - goal[1])


def replay_path(path):
    for minute, p in enumerate(path):
        print(
            f"Minute {minute}",
            get_desc(p, path[minute - 1] if minute > 0 else None, minute),
        )
        print_valley(get_valley_at_minute(minute), p)
        input()


best_minute = 10000


@cache
def dfs(start, goal, minute, max_min):
    global best_minute
    [x, y] = start
    if (x, y) == goal:
        if minute < best_minute:
            best_minute = minute
    if minute + mh_to_goal((x, y), goal) > best_minute:
        return
    if minute > max_min:
        return
    if (x, y) in visited:
        if minute < min_min_to_reach[(x, y)]:
            min_min_to_reach[(x, y)] = minute
        elif minute > min_min_to_reach[(x, y)] + 50:
            return
    else:
        visited.add((x, y))
        min_min_to_reach[(x, y)] = minute
    valley = get_valley_at_minute(minute + 1)
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= W or ny < 0 or ny >= H:
            continue
        if valley[nx][ny] == ["#"] or any(
            item in [">", "<", "v", "^"] for item in valley[nx][ny]
        ):
            continue
        dfs((nx, ny), goal, minute + 1, max_min)
    return best_minute


visited = set()
min_min_to_reach = {}


def travel(start, goal, start_min, max_min):
    global best_minute, visited, min_min_to_reach
    # dict of visited to minutes
    global min_min_to_reach
    best_minute = 10000
    min_min_to_reach = {}
    visited = set()
    return dfs(start, goal, start_min, max_min)


start = (1, 0)
goal = (W - 2, H - 1)

minute = travel(start, goal, 0, 300)
print(minute)
minute = travel(goal, start, minute, 600)
minute = travel(start, goal, minute, 900)
print(minute)
