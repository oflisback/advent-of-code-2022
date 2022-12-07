lines = open("input.txt").read().splitlines()

structure = {}
current = []

for l in lines:
    if l[0] == "$":
        if l[2:4] == "cd":
            arg = l[5:]
            if arg == "..":
                current.pop()
            else:
                current.append(arg)
        if l[2:4] == "ls":
            structure["/".join(current) + "/"] = 0
    elif l[:3] == "dir":
        continue
    else:
        [size, _] = l.split(" ")
        structure["/".join(current) + "/"] += int(size)

sizes = {}
for dir_1 in structure.keys():
    size = 0
    for dir_2 in structure.keys():
        if dir_2.startswith(dir_1):
            size += structure[dir_2]
    sizes[dir_1] = size

sum_under_100000 = 0
for s in sizes.values():
    if s <= 100000:
        sum_under_100000 += s
print(sum_under_100000)

unused_space = 70000000 - sizes["//"]
required_to_free = 30000000 - unused_space

ds = 10000000000
for s in sizes.values():
    if s < ds and s >= required_to_free:
        ds = s
print(ds)
