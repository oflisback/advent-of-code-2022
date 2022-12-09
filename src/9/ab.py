def follow(cur, par):
    should_move = (abs(par[0] - cur[0]) > 1) or (abs(par[1] - cur[1]) > 1)
    if not should_move:
        return cur

    cur = (cur[0] + 1, cur[1]) if par[0] - cur[0] >= 1 else cur
    cur = (cur[0] - 1, cur[1]) if cur[0] - par[0] >= 1 else cur
    cur = (cur[0], cur[1] + 1) if par[1] - cur[1] >= 1 else cur
    cur = (cur[0], cur[1] - 1) if cur[1] - par[1] >= 1 else cur

    return cur


def get_tail_positions(rope_len):
    rope = [(0, 0) for _ in range(rope_len)]
    historical_tail_positions = set()
    for l in open("input.txt").read().splitlines():
        [dir, steps] = l.split()
        for _ in range(int(steps)):
            MD = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
            rope[rope_len - 1] = [c + d for c, d in zip(rope[rope_len - 1], MD[dir])]

            for j in range(rope_len - 2, -1, -1):
                rope[j] = follow(rope[j], rope[j + 1])

            if not rope[0] in historical_tail_positions:
                historical_tail_positions.add(rope[0])
    return len(historical_tail_positions)


print(get_tail_positions(2))
print(get_tail_positions(10))
