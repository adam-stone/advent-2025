import sys
from collections import defaultdict


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)

# Here we store an array of vertical positions on the grid. Each element of
# the array contains a dictionary mapping the beam position at that row to the
# number of distinct paths that reach that position
beam_loc = [{lines[0].index("S"): 1}]

for line in lines[1:]:
    incoming_loc = beam_loc[-1]
    outbound_loc = defaultdict(int)

    for beam, path_count in incoming_loc.items():
        if line[beam] == "^":
            outbound_loc[beam - 1] += path_count
            outbound_loc[beam + 1] += path_count
        else:
            outbound_loc[beam] += path_count
    beam_loc.append(outbound_loc)

print(f"Total paths: {sum(beam_loc[-1].values())}")
