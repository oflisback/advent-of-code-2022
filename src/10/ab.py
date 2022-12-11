lines = open("input.txt").read().splitlines()

x_reg = 1
pipeline = []

for l in lines:
    if l == "noop":
        pipeline.append(["noop", 1, 0])
    else:
        inst, val = l.split()
        pipeline.append(["addx", 2, int(val)])


def print_screen(rows):
    for r in rows:
        print(r)


rows = [["."] * 40 for _ in range(6)]

crt_pos = crt_row = 0

cycle = 0
checkpoints = []
current_instruction = None
while len(pipeline) > 0 or current_instruction is not None:
    cycle += 1
    print("Cycle start: {}, x_reg: {}".format(cycle, x_reg))
    if not current_instruction and len(pipeline) > 0:
        print("Popping new instruction")
        current_instruction = pipeline.pop(0)
    if current_instruction:
        print("Executing: ", current_instruction)
        current_instruction[1] -= 1

    if abs(crt_pos - x_reg) < 2:
        print("Should draw pixel")
        rows[crt_row][crt_pos] = "#"

    print("Cycle end: {}, x_reg: {}".format(cycle, x_reg))
    if cycle == 20 or (cycle - 20) % 40 == 0:
        checkpoints.append(x_reg * cycle)
    if current_instruction:
        if current_instruction[1] == 0:
            print("Execution of {} finished".format(current_instruction))
            [inst, cycles_left, diff] = current_instruction
            current_instruction = None
            if inst == "addx":
                x_reg += diff
    crt_pos += 1
    if crt_pos > 39:
        crt_pos = 0
        crt_row += 1

print(sum(checkpoints))
print_screen(rows)
