from parse import search

lines = open("input.txt").read().splitlines()

pairs = []

for l in lines:
    [s_x, s_y, c_x, c_y] = search(
        "Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}", l
    )
    pairs.append(((s_x, s_y), (c_x, c_y)))


def get_coverage_on_row(row, pair):
    sensor = pair[0]
    closest_beacon = pair[1]
    manhattan_distance_to_beacon = abs(sensor[1] - closest_beacon[1]) + abs(
        sensor[0] - closest_beacon[0]
    )
    horizontal_stretch_on_row = manhattan_distance_to_beacon - abs(sensor[1] - row)
    if horizontal_stretch_on_row > 0:
        coverage_on_row = range(
            sensor[0] - horizontal_stretch_on_row,
            sensor[0] + horizontal_stretch_on_row + 1,
        )
    else:
        coverage_on_row = []

    return coverage_on_row


coverage_on_200000 = set()
for pair in pairs:
    coverage_on_200000.update(get_coverage_on_row(2000000, pair))

# Remove beacons from coverage
for pair in pairs:
    try:
        if pair[1][1] == 2000000:
            coverage_on_200000.remove(pair[1][0])
    except KeyError:
        pass


print(len(coverage_on_200000))
