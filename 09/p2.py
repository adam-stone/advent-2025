import itertools
import sys

###############################################################################
# Assumptions:
# - Assumes no contiguous collinear segments, meaning no more than two tiles
#   in the input sequence may be in the same row or column
# - Assumes the area enclosed by the sequence of tiles forms a single
#   contiguous area, meaning none of the line segments cross
#
# These assumptions were validated on the input set using the check_tiles.py
# script found in this directory
#
# Known issues:
# - Does not find rectangles with width or height of 1. I assumed the final
#   puzzle solution would not be long and skinny, but if it were, this method
#   would not work
###############################################################################


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

horizontal_lines = []
vertical_lines = []
for t0, t1 in itertools.pairwise(tiles + [tiles[0]]):
    if t0[0] == t1[0]:
        vertical_lines.append(tuple(sorted([t0, t1])))
    elif t0[1] == t1[1]:
        horizontal_lines.append(tuple(sorted([t0, t1])))
    else:
        print(f"Found non-axis-aligned line between {t0} and {t1}")
        exit(1)

horizontal_lines.sort(key=lambda x: x[0][1])
vertical_lines.sort(key=lambda x: x[0][0])

# The total possible set of rectangles contains all possible pairings of tiles
rectangles = []
for i0, i1 in itertools.combinations(range(len(tiles)), 2):
    x0, y0 = tiles[i0]
    x1, y1 = tiles[i1]
    area = (abs(x1 - x0) + 1) * (abs(y1 - y0) + 1)
    rectangles.append((i0, i1, area))

# Examine the largest rectangles first
rectangles.sort(key=lambda x: x[2], reverse=True)

for i0, i1, area in rectangles:
    v0 = tiles[i0]
    v1 = tiles[i1]
    xmin = min(v0[0], v1[0])
    xmax = max(v0[0], v1[0])
    ymin = min(v0[1], v1[1])
    ymax = max(v0[1], v1[1])

    # Filter the horizontal lines that enter the rectangle's x-extent from the
    # left side
    onleft = [
        x[0][1]
        for x in filter(
            lambda line: line[0][0] <= xmin and line[1][0] > xmin, horizontal_lines
        )
    ]
    # To be fully within the valid area, there must be an odd number of lines
    # in the x-extent before the rectangle's y-min, and there must be no lines
    # that cross into the rectangle's y-extent
    count_lt = len([y for y in onleft if y <= ymin])
    count_gt = len([y for y in onleft if y >= ymax])
    if count_lt % 2 == 0 or count_lt + count_gt != len(onleft):
        continue

    # Filter the horizontal lines that enter the rectangle's x-extent from the
    # right side
    onright = [
        x[0][1]
        for x in filter(
            lambda line: line[0][0] < xmax and line[1][0] >= xmax, horizontal_lines
        )
    ]
    # To be fully within the valid area, there must be an odd number of lines
    # in the x-extent before the rectangle's y-min, and there must be no lines
    # that cross into the rectangle's y-extent
    count_lt = len([y for y in onright if y <= ymin])
    count_gt = len([y for y in onright if y >= ymax])
    if count_lt % 2 == 0 or count_lt + count_gt != len(onright):
        continue

    # Filter the vertical lines that enter the rectangle's y-extent from the
    # top side
    ontop = [
        x[0][0]
        for x in filter(
            lambda line: line[0][1] <= ymin and line[1][1] > ymin, vertical_lines
        )
    ]
    # To be fully within the valid area, there must be an odd number of lines
    # in the y-extent before the rectangle's x-min, and there must be no lines
    # that cross into the rectangle's x-extent
    count_lt = len([x for x in ontop if x <= xmin])
    count_gt = len([x for x in ontop if x >= xmax])
    if count_lt % 2 == 0 or count_lt + count_gt != len(ontop):
        continue

    # Filter the vertical lines that enter the rectangle's y-extent from the
    # bottom side
    onbottom = [
        x[0][0]
        for x in filter(
            lambda line: line[0][1] < ymax and line[1][1] >= ymax, vertical_lines
        )
    ]
    # To be fully within the valid area, there must be an odd number of lines
    # in the y-extent before the rectangle's x-min, and there must be no lines
    # that cross into the rectangle's x-extent
    count_lt = len([x for x in onbottom if x <= xmin])
    count_gt = len([x for x in onbottom if x >= xmax])
    if count_lt % 2 == 0 or count_lt + count_gt != len(onbottom):
        continue

    # The first valid rectangle is the largest
    print(f"Found valid rectangle: ({xmin},{ymin}) to ({xmax},{ymax}) with area {area}")
    break
else:
    print("No valid rectangle found")
