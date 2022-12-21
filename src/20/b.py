lines = open("input.txt").read().splitlines()

key = 811589153

numbers = [int(x) * key for x in lines]
nbr_values = len(numbers)

short_numbers = []
for i in range(nbr_values):
    if numbers[i] >= 0:
        short_numbers.append(numbers[i] % (nbr_values - 1))
    else:
        meh = -1 * (-1 * numbers[i] % (nbr_values - 1))
        short_numbers.append(meh)

head = {"value": short_numbers[0], "org": numbers[0], "head": True}


def get_zero_node(node):
    for _ in range(len(numbers)):
        if node["value"] == 0:
            return node
        node = node["next"]


nodes_in_order = [head]

cur = head
for i in range(1, len(numbers)):
    cur["next"] = {"org": numbers[i], "value": short_numbers[i]}
    prev = cur
    cur = cur["next"]
    cur["prev"] = prev
    nodes_in_order.append(cur)
cur["next"] = head
head["prev"] = cur


node = head
for _ in range(len(numbers)):
    node = node["next"]


for i in range(10):
    print("Starting round:", i + 1)
    for n_index, node in enumerate(nodes_in_order):
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
        n = get_zero_node(nodes_in_order[0])
    n = get_zero_node(nodes_in_order[0])

node = nodes_in_order[0]
for _ in range(len(numbers)):
    if node["value"] == 0:
        break
    node = node["next"]
for _ in range(1000):
    node = node["next"]
values = []
print("Value at 1000: ", node["org"])
values.append(node["org"])
for _ in range(1000):
    node = node["next"]
print("Value at 2000: ", node["org"])
values.append(node["org"])
for _ in range(1000):
    node = node["next"]
print("Value at 3000: ", node["org"])
values.append(node["org"])

print(sum(values))
