lines = open("input.txt").read().splitlines()


def snigit_to_dec(snigit):
    if snigit == "-":
        return -1
    elif snigit == "=":
        return -2
    else:
        return int(snigit)


def digit_to_snigit(digit):
    if digit == 4:
        return "-", -1
    if digit == 3:
        return "=", -2
    return str(digit), digit


def snarfu_to_dec(snarfu):
    dec = 0
    for i, c in enumerate(snarfu[::-1]):
        dec += snigit_to_dec(c) * 5**i
    return dec


def dec_to_snarfu(dec):
    base = 5
    snarfu = ""
    mult = 0
    while dec > 0:
        factor = base**mult
        remainder = dec % (factor * 5)
        [snigit, consumed] = digit_to_snigit(remainder // factor)
        snarfu += snigit
        dec -= consumed * factor
        mult += 1
    return snarfu[::-1]


sum = 0
for snarfu in lines:
    sum += snarfu_to_dec(snarfu)
print(sum)

print(dec_to_snarfu(sum))
