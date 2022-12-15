from parse import search

lines = open("input.txt").read().splitlines()

pairs = []

for l in lines:
    [s_x, s_y, c_x, c_y] = search(
        "Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}", l
    )
    pairs.append(((s_x, s_y), (c_x, c_y)))


def get_coverage_on_row(row, pair):
    [sensor, closest_beacon] = pair
    manhattan_distance_to_beacon = abs(sensor[1] - closest_beacon[1]) + abs(
        sensor[0] - closest_beacon[0]
    )
    horizontal_stretch_on_row = manhattan_distance_to_beacon - abs(sensor[1] - row)
    if horizontal_stretch_on_row > 0:
        coverage = (
            sensor[0] - horizontal_stretch_on_row,
            sensor[0] + horizontal_stretch_on_row,
        )
    else:
        coverage = None

    return coverage


for row in range(0, 4000000 + 1):
    coverage = []
    for pair in pairs:
        c = get_coverage_on_row(row, pair)
        if c is not None:
            coverage.append(c)
    coverage = sorted(coverage, key=lambda x: x[0])
    did_merge = True
    while did_merge:
        i = 0
        clean_coverage = []
        did_merge = False
        while i < len(coverage):
            if i == len(coverage) - 1:
                clean_coverage.append(coverage[i])
                i += 1
                break
            if (
                coverage[i][0] <= coverage[i + 1][0]
                and coverage[i][1] >= coverage[i + 1][1]
            ):
                clean_coverage.append((coverage[i][0], coverage[i][1]))
                did_merge = True
                clean_coverage.extend(coverage[i + 2 :])
                break
            elif (
                coverage[i][0] <= coverage[i + 1][0]
                and coverage[i][1] >= coverage[i + 1][0] - 1
            ):
                clean_coverage.append((coverage[i][0], coverage[i + 1][1]))
                did_merge = True
                clean_coverage.extend(coverage[i + 2 :])
                break
            else:
                clean_coverage.append(coverage[i])
            i += 1
        coverage = clean_coverage

    if len(coverage) > 1:
        print("Coverage on row:", row)
        x = coverage[1][0] - 1
        y = coverage[0][1]
        print(x * 4000000 + row)
