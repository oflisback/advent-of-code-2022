from networkx import DiGraph, bfs_layers, shortest_path_length

lines = open("input.txt").read().splitlines()
start = target = None
GA = DiGraph()
GB = DiGraph()

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "S":
            start = (x, y)
        if c == "E":
            target = (x, y)
        map = {"S": "a", "E": "z"}
        c = c if not c in map else map[c]
        GA.add_node((x, y), height=c)
        GB.add_node((x, y), height=c)
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if nx < 0 or ny < 0 or ny >= len(lines) or nx >= len(lines[0]):
                continue
            n_char = lines[ny][nx]
            nv = map[n_char] if n_char in map else n_char
            if nv <= chr(ord(c) + 1):
                GA.add_edge((x, y), (nx, ny))
            if chr(ord(nv) + 1) >= c:
                GB.add_edge((x, y), (nx, ny))

print(shortest_path_length(GA, start, target))
for layer_index, layer in enumerate(bfs_layers(GB, target)):
    for node_name in layer:
        if GB.nodes[node_name]["height"] == "a":
            print(layer_index)
            exit(0)
