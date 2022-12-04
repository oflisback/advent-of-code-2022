from parse import search

lines = open("input.txt").read().splitlines()

full, some = 0, 0
for [s1, e1, s2, e2] in [search("{:d}-{:d},{:d}-{:d}", l) for l in lines]:
    a = set(range(s1, e1 + 1))
    b = set(range(s2, e2 + 1))

    if a <= b or b <= a:
        full += 1
    if a & b:
        some += 1

print(full)
print(some)
