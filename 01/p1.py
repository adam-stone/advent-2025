import sys


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


moves = slurp_lines(sys.argv[1])

dial_pos = 50  # given start position
DIAL_SIZE = 100  # given dial size

dial_history = []

for move in moves:
    dir = move[0]
    dist = int(move[1:])

    dial_pos = (dial_pos + dist if dir == "R" else dial_pos - dist) % DIAL_SIZE

    dial_history.append(dial_pos)

# Count the number of times the dial lands on zero
print(dial_history.count(0))
