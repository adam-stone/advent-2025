import sys


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


roll_neighbors = {}

lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "@":
            roll_neighbors[(x, y)] = 0


def count_neighbors():
    adjacency_offsets = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]
    for x, y in roll_neighbors.keys():
        roll_neighbors[(x, y)] = 0
        for dx, dy in adjacency_offsets:
            if (x + dx, y + dy) in roll_neighbors:
                roll_neighbors[(x, y)] += 1


removals = []

while True:
    count_neighbors()
    dead_rolls = []
    for pos, neighbors in roll_neighbors.items():
        if neighbors < 4:
            dead_rolls.append(pos)
    if len(dead_rolls) == 0:
        break
    removals.append(len(dead_rolls))
    for pos in dead_rolls:
        del roll_neighbors[pos]

print(f"Removals: {removals}")
print(f"Total removed: {sum(removals)}")
