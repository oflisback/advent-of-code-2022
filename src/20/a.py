lines = open("input.txt").read().splitlines()

numbers = [int(x) for x in lines]

org_order_nodes = list(range(len(numbers)))

head = {"value": numbers[0]}

nodes_in_order = [head]

cur = head
for i in range(1, len(numbers)):
    cur["next"] = {"value": numbers[i]}
    prev = cur
    cur = cur["next"]
    cur["prev"] = prev
    nodes_in_order.append(cur)
cur["next"] = head
head["prev"] = cur

for n_index, node in enumerate(nodes_in_order):
    if n_index % 100 == 0:
        print(n_index / len(numbers))
    for _ in range(abs(node["value"])):
        if node["value"] < 0:
            prevprev = node["prev"]["prev"]
            prev = node["prev"]
            next = node["next"]

            prevprev["next"] = node
            node["prev"] = prevprev
            node["next"] = prev
            prev["prev"] = node
            prev["next"] = next
            next["prev"] = prev
        elif node["value"] > 0:
            prev = node["prev"]
            next = node["next"]
            nextnext = node["next"]["next"]

            prev["next"] = next
            next["prev"] = prev
            next["next"] = node
            node["prev"] = next
            node["next"] = nextnext
            nextnext["prev"] = node

node = nodes_in_order[0]
for _ in range(len(numbers)):
    if node["value"] == 0:
        break
    node = node["next"]
for _ in range(1000):
    node = node["next"]
values = []
print("Value at 1000: ", node["value"])
values.append(node["value"])
for _ in range(1000):
    node = node["next"]
print("Value at 2000: ", node["value"])
values.append(node["value"])
for _ in range(1000):
    node = node["next"]
print("Value at 3000: ", node["value"])
values.append(node["value"])
print(sum(values))
