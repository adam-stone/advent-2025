import sys


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)

beam_loc = []
splits = []

beam_loc.append({lines[0].index("S")})
splits.append(0)

for line in lines[1:]:
    split_count = 0
    incoming_loc = beam_loc[-1]
    outbound_loc = set()

    for beam in incoming_loc:
        if line[beam] == "^":
            split_count += 1
            outbound_loc.add(beam - 1)
            outbound_loc.add(beam + 1)
        else:
            outbound_loc.add(beam)
    beam_loc.append(outbound_loc)
    splits.append(split_count)

for i in range(len(lines)):
    print(f"{splits[i]:2d}: {sorted(beam_loc[i])}")
print(f"Total splits: {sum(splits)}")
