import functools
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
        return 1
    else:
        res = 0
        for connection in graph[node]:
            res += count_paths(connection, terminal)
        return res


path_q = count_paths("svr", "out")
print(f"Total: {path_q}")
