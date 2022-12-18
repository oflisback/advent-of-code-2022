from misc import get_graph
from worker import Worker

best_path = None
M = 30


def log_path(path, reason):
    print(
        reason,
        "sum_points_at_minute:",
        sum(path["points_at_minute"]),
        "points_at_minute:",
        path["points_at_minute"],
        "len points_at_minute: ",
        len(path["points_at_minute"]),
    )


def get_acc_points(points_at_minute):
    acc_points = [None] * len(points_at_minute)
    acc = 0
    for i in range(len(points_at_minute)):
        acc += points_at_minute[i]
        acc_points[i] = acc
    return acc_points


def set_best(worker, reason):
    global best_path
    best_path = {
        "acc_points": get_acc_points(worker.points_at_minute),
        "path": worker.path,
        "points_at_minute": worker.points_at_minute,
    }
    log_path(best_path, reason)


G, nbr_vents_to_open = get_graph()


def get_prev(worker):
    return worker.path[-2] if len(worker.path) >= 2 else None


def get_candidates(worker, open_valves, dead_ends):
    candidates = []
    prev = get_prev(worker)
    for neigh in G.neighbors(worker.cur):
        if neigh not in dead_ends:
            candidates.append(neigh)
        # Remove prev_node if this node isn't open or if node value is 0,
        # it doesn't make sense to just go in and out again.
        if prev in candidates:
            if worker.cur in open_valves or G.nodes[worker.cur]["rate"] == 0:
                candidates.remove(prev)

    if len(candidates) == 1 and candidates == prev:
        # We are at a dead end, let's not go there again.
        dead_ends.add(worker.cur)

    if prev in dead_ends and len(candidates) == 1:
        # This will also be a dead end, add it
        dead_ends.add(worker.cur)
    return candidates


def check_for_useless_loop(worker):
    if (
        sum(worker.points_at_minute) > 0
        and sum(worker.points_at_minute) == worker.node_sum_map[worker.cur]
    ):
        # We've been here before! And we were venting just as much last time, that must have been a
        # useless path let's never go there again.
        reversed_path = worker.cur_path[::-1]
        for i in range(1, len(reversed_path)):
            if reversed_path[i] == worker.cur:
                # We have been here before.
                if worker.node_sum_map[worker.cur] == sum(worker.points_at_minute):
                    # Last time we were here the path points were the same.
                    dead_ends.update(reversed_path[1:i])
                    break


def handle_done_walking(worker):
    while worker.minute < M:
        worker.minute += 1
        worker.points_at_minute += [0]
    if not best_path or sum(worker.points_at_minute) > sum(
        best_path["points_at_minute"]
    ):
        set_best(worker, "D")


def step(worker, open_valves, dead_ends):
    check_for_useless_loop(worker)

    if worker.minute >= M:
        if not best_path or sum(worker.points_at_minute) > best_path["acc_points"][-1]:
            set_best(worker, "T")
        return

    if best_path and worker.minute > 10:
        best_at_this_minute = best_path["acc_points"][
            min(worker.minute, len(best_path["acc_points"]) - 1)
        ]
        if sum(worker.points_at_minute) < 0.8 * best_at_this_minute:
            return

    worker.node_sum_map[worker.cur] = worker.points_at_minute
    candidates = get_candidates(worker, open_valves, dead_ends)

    if len(candidates) == 0 or nbr_vents_to_open == len(open_valves):
        handle_done_walking(worker)
        return

    this_valve_points = G.nodes[worker.cur]["rate"] * (M - worker.minute)
    if worker.cur not in open_valves and this_valve_points > 0:
        for candidate in candidates:
            edge_weight = G.get_edge_data(worker.cur, candidate)["weight"]
            step(
                Worker(
                    candidate,
                    worker.path + [candidate],
                    worker.points_at_minute + [this_valve_points],
                    worker.minute + 1 + edge_weight,
                    worker.node_sum_map,
                ),
                open_valves.union({worker.cur}),
                dead_ends,
            )
    prev = get_prev(worker)
    if prev in candidates:
        # Don't go directly back to prev in the did-not-open case
        # This is also a huge time-saver
        candidates.remove(prev)
    for candidate in candidates:
        edge_weight = G.get_edge_data(worker.cur, candidate)["weight"]
        step(
            Worker(
                candidate,
                worker.path + [candidate],
                worker.points_at_minute + [0],
                worker.minute + edge_weight,
                worker.node_sum_map,
            ),
            open_valves,
            dead_ends,
        )


step(Worker(), open_valves=set(), dead_ends=set())
print(best_path)
print("Result: ", best_path["acc_points"][-1])
