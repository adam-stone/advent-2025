import functools
import operator
import sys


def slurp_input(filename="--"):
    if filename == "--":
        return sys.stdin.read()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


ranges = slurp_input(sys.argv[1]).split(",")
invalid_ids = []
for r in ranges:
    start, end = map(int, r.split("-"))
    for i in range(start, end + 1):
        s = str(i)
        c = len(s)
        if c % 2 == 1:
            continue
        if s[: c // 2] == s[c // 2 :]:
            invalid_ids.append(i)

sum = functools.reduce(operator.add, invalid_ids, 0)
print(f"Total: {sum}")
