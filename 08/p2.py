import sys


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)


# Storing circuits by tracking which circuit each box is a member of. Since
# we also want to quickly find the size of each circuit, store that too.
# Each entry in the circuits list is a tuple of (circuit_id, circuit_size)
# where circuit_size is non-zero only for the lowest-indexed box in the
# circuit
def merge_circuits(box0, box1, circuits):
    base = min(circuits[box0][0], circuits[box1][0])
    branch = max(circuits[box0][0], circuits[box1][0])
    # Break out early if the two boxes are already in the same circuit
    if base == branch:
        return
    new_size = circuits[base][1] + circuits[branch][1]
    circuits[base] = (base, new_size)
    for i in range(len(circuits)):
        if circuits[i][0] == branch:
            circuits[i] = (base, 0)


pos = []
circuits = []
for i, line in enumerate(lines):
    x, y, z = line.split(",")
    pos.append((int(x), int(y), int(z)))
    circuits.append((i, 1))

# When the graph is fully connected, the first circuit will look like this
fully_connected_circuit = (0, len(pos))

# Actually storing the squared distances between each pair, since all we do
# with them is compare them to each other, we don't need to take square roots
distances = []
for i in range(len(pos)):
    for j in range(i + 1, len(pos)):
        dx = pos[j][0] - pos[i][0]
        dy = pos[j][1] - pos[i][1]
        dz = pos[j][2] - pos[i][2]
        distances.append((i, j, dx * dx + dy * dy + dz * dz))

# Sort distances in descending order to make popping the closest pair more
# efficient
distances.sort(key=lambda x: x[2], reverse=True)

# Merge circuits using the shortest available connections until the graph is
# fully connected
while circuits[0] != fully_connected_circuit:
    d = distances.pop()
    merge_circuits(d[0], d[1], circuits)

print(f"Result: {pos[d[0]][0] * pos[d[1]][0]}")
