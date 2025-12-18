import functools
import operator
import sys


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)

graph = {}

for line in lines:
    node, connections = line.split(":", maxsplit=2)
    graph[node] = connections.split()


@functools.cache
def count_paths(node, terminal):
    if node == terminal:
        return (1, 0, 0, 0)
    else:
        res = [0, 0, 0, 0]
        for connection in graph[node]:
            res = list(map(operator.add, res, count_paths(connection, terminal)))
        if node == "dac":
            return (0, res[0] + res[1], 0, res[2] + res[3])
        elif node == "fft":
            return (0, 0, res[0] + res[2], res[1] + res[3])
        else:
            return tuple(res)


no_markers, dac_only, fft_only, both = count_paths("svr", "out")
print(f"Neither: {no_markers}")
print(f"DAC only: {dac_only}")
print(f"FFT only: {fft_only}")
print(f"Both DAC and FFT: {both}")
print(f"Total: {no_markers + dac_only + fft_only + both}")
