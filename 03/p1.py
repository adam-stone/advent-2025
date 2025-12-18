import sys


def slurp_lines(filename=sys.argv[1]):
    if filename == "--":
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


banks = slurp_lines()
jolts = []

for bank in banks:
    jolt = 0
    max_char = max(bank[:-1])
    for e in filter(lambda x: x[1] == max_char, enumerate(bank, start=1)):
        if e[0] < len(bank):
            j = int(e[1] + max(bank[e[0] :]))
            if j > jolt:
                jolt = j
    jolts.append(jolt)

print(f"Jolt total: {sum(jolts)}")
