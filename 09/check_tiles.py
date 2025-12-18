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

lines = list(itertools.pairwise(tiles + [tiles[0]]))


def line_axis(t0, t1):
    x0, y0 = t0
    x1, y1 = t1
    if x0 == x1:
        return "x"
    elif y0 == y1:
        return "y"
    else:
        raise Exception(f"Found non-axis-aligned line between {t0} and {t1}")


vertical_lines = []
horizontal_lines = []

last_line_axis = line_axis(lines[0][0], lines[0][1])
if last_line_axis == "x":
    vertical_lines.append(lines[0])
else:
    horizontal_lines.append(lines[0])

for t0, t1 in lines[1:]:
    axis = line_axis(t0, t1)
    if axis == last_line_axis:
        print(f"Found non-alternating lines between {t0} and {t1}")
        exit(1)
    if axis == "x":
        vertical_lines.append((t0, t1))
    else:
        horizontal_lines.append((t0, t1))
    last_line_axis = axis

print("All lines are axis-aligned and alternate correctly")

for v in vertical_lines:
    for h in horizontal_lines:
        if v[0] == h[0] or v[0] == h[1] or v[1] == h[0] or v[1] == h[1]:
            continue
        v0 = min(v)
        v1 = max(v)
        h0 = min(h)
        h1 = max(h)
        if h0[0] <= v0[0] <= h1[0] and v0[1] <= h0[1] <= v1[1]:
            print(
                f"Found intersection at ({v0[0]},{h0[1]}) between {v0}-{v1} and {h0}-{h1}"
            )
            exit(1)

print("No intersections found")
