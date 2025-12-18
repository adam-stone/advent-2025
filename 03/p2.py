import sys


def slurp_lines(filename=sys.argv[1]):
    if filename == "--":
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def max_jolts(bank: str, digits: int) -> int:
    if digits == 1:
        return int(max(bank))

    jolt = 0
    available_bank = bank[: 1 - digits]
    max_char = max(available_bank)

    for e in filter(lambda x: x[1] == max_char, enumerate(available_bank, start=1)):
        j = int(e[1] + str(max_jolts(bank[e[0] :], digits - 1)))
        if j > jolt:
            jolt = j
    return jolt


USABLE_DIGITS = 12
banks = slurp_lines()
jolts = []

for bank in banks:
    jolts.append(max_jolts(bank, USABLE_DIGITS))

# print(f"Jolts: {jolts}")
print(f"Jolt total: {sum(jolts)}")
