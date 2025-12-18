import math
import sys


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)

problems = []

for op in lines[-1].split():
    problems.append({"op": op, "args": []})

for line in lines[:-1]:
    for i, val in enumerate(line.split()):
        problems[i]["args"].append(int(val))

answers = []

for p in problems:
    if p["op"] == "+":
        func = sum
    elif p["op"] == "*":
        func = math.prod
    answers.append(func(p["args"]))

print(f"Grand total: {sum(answers)}")
