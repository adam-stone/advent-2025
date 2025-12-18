import functools
import itertools
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
    for id in range(start, end + 1):
        s = str(id)

        for i in range(1, len(s) // 2 + 1):
            if len(s) % i != 0:
                continue
            if all(
                map(
                    lambda x: "".join(x) == s[:i],
                    itertools.batched(s[i:], i, strict=True),
                )
            ):
                invalid_ids.append(id)
                break

sum = functools.reduce(operator.add, invalid_ids, 0)
print(f"Total: {sum}")
