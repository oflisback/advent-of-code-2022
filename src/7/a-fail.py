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
            continue
    elif l[:3] == "dir":
        continue
    else:
        [size, _] = l.split(" ")
        key = "/".join(current) + "/"
        if key in structure:
            structure[key] += int(size)
        else:
            structure[key] = int(size)

sizes = {}
for dir_name in structure.keys():
    size = 0
    for dir_name_2 in structure.keys():
        if dir_name_2.startswith(dir_name):
            size += structure[dir_name_2]
    sizes[dir_name] = size

sum_under_100000 = 0
for s in sizes.values():
    if s <= 100000:
        sum_under_100000 += s
print(sum_under_100000)
