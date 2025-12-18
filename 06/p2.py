import math
import sys


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)

# Values are not right padded, so we need to know where the longest line ends
# to get the justification of the last argument right
max_len = max([len(x) for x in lines])

problems = []

# Extract the operations from the last line of input, along with the position
# where each column of values begins
for i, op in [x for x in enumerate(lines[-1]) if x[1] != " "]:
    problems.append({"op": op, "pos": i, "raw_args": []})

# Take a second pass through the problems and fill in the end position of
# each column other than the last
for i, p in enumerate(problems[:-1]):
    p["end"] = problems[i + 1]["pos"] - 1

# For the last column, fill in a width property so we know how much padding to
# add
problems[-1]["width"] = max_len - problems[-1]["pos"]

# Extract the arguments as strings to preserve justification. For the last
# item in the column, add padding on the right to fill the column width
for line in lines[:-1]:
    for p in problems:
        if "end" in p:
            p["raw_args"].append(line[p["pos"] : p["end"]])
        else:
            val = line[p["pos"] :]
            val = val + " " * (p["width"] - len(val))
            p["raw_args"].append(val)

# Parse the real arguments for each problem column-wise
for p in problems:
    # Sanity check: all raw_args are the same length, right?
    raw = p["raw_args"]
    width = len(raw[0])
    if not all(len(x) == width for x in raw):
        print(f"Failed to justify args: {raw}")
        exit(1)

    # Join the digits in each column, from most significat to least and convert
    # to int
    args = []
    for i in range(width):
        args.append(int("".join(x[i] for x in raw)))
    p["args"] = args

answers = []

# Do the math for each problem
for p in problems:
    if p["op"] == "+":
        func = sum
    elif p["op"] == "*":
        func = math.prod
    answers.append(func(p["args"]))

print(f"Grand total: {sum(answers)}")
