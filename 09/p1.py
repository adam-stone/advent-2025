import itertools
import sys


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


tiles = [
    (int(x), int(y))
    for x, y in [
        line.split(",")
        for line in slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)
    ]
]

# The total possible set of rectangles contains all possible pairings of tiles
rectangles = []
for i0, i1 in itertools.combinations(range(len(tiles)), 2):
    x0, y0 = tiles[i0]
    x1, y1 = tiles[i1]
    area = (abs(x1 - x0) + 1) * (abs(y1 - y0) + 1)
    rectangles.append((i0, i1, area))

rectangles.sort(key=lambda x: x[2], reverse=True)

print(f"Largest rectangle is {tiles[rectangles[0][0]]} to {tiles[rectangles[0][1]]}")
print(f"Area: {rectangles[0][2]}")
