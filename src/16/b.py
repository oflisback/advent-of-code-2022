from misc import get_graph
from worker import Worker
from itertools import product, zip_longest


best_team = None
M = 26


def log_team(best_team, reason):
    print("Team score: ", best_team["acc_points"][-1])
    print(reason, best_team)


def get_acc_points(workers):
    points_at_minute = [w.points_at_minute for w in workers]
    combined_points = [i + j for i, j in zip_longest(*points_at_minute, fillvalue=0)]
    acc = 0
    acc_points = []
    for points in combined_points:
        acc += points
        acc_points.append(acc)
    return acc_points


def set_best_team(workers, open_valves, reason):
    global best_team
    best_team = {
        "acc_points": get_acc_points(workers),
        "nbr_open_valves": len(open_valves),
        "paths": [w.path for w in workers],
        "points_at_minute": [w.points_at_minute for w in workers],
    }
    log_team(best_team, reason)


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


def check_for_useless_loop(worker, dead_ends):
    points = sum(worker.points_at_minute)
    if points > 0 and points == worker.node_sum_map[worker.cur]:
        # We've been here before! And we were venting just as much last time, that must have been a
        # useless path let's never go there again.
        reversed_path = worker.path[::-1]
        for i in range(1, len(reversed_path)):
            if reversed_path[i] == worker.cur:
                dead_ends.update(reversed_path[1:i])
                break
    else:
        worker.node_sum_map[worker.cur] = points


def total_sum(workers):
    s = 0
    for l in [w.points_at_minute for w in workers]:
        s += sum(l)
    return s


# Apparently there's a bug resulting in workers visisting the sam node
# and opening it at the same time, don't fix it, work around it!
def cheating(workers):
    w_index = 0 if len(workers[0].path) < len(workers[1].path) else 1
    o_index = 1 - w_index
    for pos_index, w_pos in enumerate(workers[w_index].path):
        # Same position
        if w_pos == workers[o_index].path[pos_index]:
            # They both scored points this minute, that's odd
            if all(w.points_at_minute[pos_index] > 0 for w in workers):
                return True
    return False


def get_candidate_pairs_for_workers(
    workers, open_valves, dead_ends, dont_go_back=False
):
    candidates = []
    for worker in workers:
        candidates.append(get_candidates(worker, open_valves, dead_ends))
    # Remove dupes in potential_nexts
    in_both = set(candidates[0]).intersection(set(candidates[1]))
    for dupe in in_both:
        if len(candidates[0]) >= len(candidates[1]):
            candidates[0].remove(dupe)
        else:
            candidates[1].remove(dupe)

    if dont_go_back:
        for i, worker in enumerate(workers):
            if get_prev(worker) in candidates[i]:
                candidates[i].remove(get_prev(worker))
    return product(candidates[0], candidates[1])


def step(workers, open_valves, dead_ends):
    dead_ends = dead_ends.copy()
    open_valves = open_valves.copy()
    for worker in workers:
        check_for_useless_loop(worker, dead_ends)

    if cheating(workers):
        return

    if not best_team or total_sum(workers) > best_team["acc_points"][-1]:
        set_best_team(workers, open_valves, "T")

    for worker in workers:
        if best_team and worker.minute > 10:
            best_at_this_minute = best_team["acc_points"][
                min(worker.minute, len(best_team["acc_points"]) - 1)
            ]
            if total_sum(workers) < 0.65 * best_at_this_minute:
                return
        if best_team and worker.minute > 20:
            best_at_this_minute = best_team["acc_points"][
                min(worker.minute, len(best_team["acc_points"]) - 1)
            ]
            if total_sum(workers) < 0.8 * best_at_this_minute:
                return

    if all([w.minute > M for w in workers]):
        return

    workers_that_can_open = []
    for w in workers:
        this_valve_points = G.nodes[w.cur]["rate"] * (M - w.minute)
        if w.cur not in open_valves and this_valve_points > 0:
            workers_that_can_open.append(w)
    if len(workers_that_can_open) == 2 and workers[0].cur != workers[1].cur:
        # Both opens and goes to next
        for candidate_pairs in get_candidate_pairs_for_workers(
            workers, open_valves, dead_ends
        ):
            edge_weights = [
                G.get_edge_data(workers[0].cur, candidate_pairs[0])["weight"],
                G.get_edge_data(workers[1].cur, candidate_pairs[1])["weight"],
            ]
            step(
                [
                    Worker(
                        candidate_pairs[w_index],
                        w.path + [candidate_pairs[w_index]],
                        w.points_at_minute + [G.nodes[w.cur]["rate"] * (M - w.minute)],
                        w.minute + 1 + edge_weights[w_index],
                        w.node_sum_map,
                    )
                    for w_index, w in enumerate(workers)
                ],
                open_valves.union({workers[0].cur, workers[1].cur}),
                dead_ends,
            )
    # Go down in a single one, if possible, but not the other
    for w_opener_index, w_opener in enumerate(workers):
        this_valve_points = G.nodes[w_opener.cur]["rate"] * (M - w_opener.minute)
        w_not_opener = workers[1 - w_opener_index]
        if w_opener.cur not in open_valves and this_valve_points > 0:
            for candidate_pairs in get_candidate_pairs_for_workers(
                [w_opener, w_not_opener], open_valves, dead_ends
            ):
                step(
                    [
                        Worker(
                            candidate_pairs[0],
                            w_opener.path + [candidate_pairs[0]],
                            w_opener.points_at_minute + [this_valve_points],
                            w_opener.minute
                            + 1
                            + G.get_edge_data(w_opener.cur, candidate_pairs[0])[
                                "weight"
                            ],
                            w_opener.node_sum_map,
                        ),
                        Worker(
                            candidate_pairs[1],
                            w.path + [candidate_pairs[1]],
                            w.points_at_minute + [0],
                            w.minute
                            + G.get_edge_data(w_not_opener.cur, candidate_pairs[1])[
                                "weight"
                            ],
                            w.node_sum_map,
                        ),
                    ],
                    open_valves.union({w_opener.cur}),
                    dead_ends,
                )

    candidate_pairs = [get_candidates(w, open_valves, dead_ends) for w in workers]
    for candidate_pairs in get_candidate_pairs_for_workers(
        workers, open_valves, dead_ends, dont_go_back=True
    ):
        edge_weights = [
            G.get_edge_data(workers[0].cur, candidate_pairs[0])["weight"],
            G.get_edge_data(workers[1].cur, candidate_pairs[1])["weight"],
        ]
        step(
            [
                Worker(
                    candidate_pairs[w_index],
                    w.path + [candidate_pairs[w_index]],
                    w.points_at_minute + [0],
                    w.minute + edge_weights[w_index],
                    w.node_sum_map,
                )
                for w_index, w in enumerate(workers)
            ],
            open_valves,
            dead_ends,
        )


step([Worker(), Worker()], set(), set())
print(best_team)
