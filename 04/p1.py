import sys


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


rolls = set()

lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "@":
            rolls.add((x, y))

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

accessible_count = 0
for x, y in rolls:
    adjacencies = 0
    for dx, dy in adjacency_offsets:
        if (x + dx, y + dy) in rolls:
            adjacencies += 1
    if adjacencies < 4:
        accessible_count += 1

print(f"Accessible rolls: {accessible_count}")
