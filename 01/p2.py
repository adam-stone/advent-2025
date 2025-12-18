import sys


def slurp_lines(filename="--"):
    if filename == "--":
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


moves = slurp_lines(sys.argv[1])

dial_pos = 50  # given start position
DIAL_SIZE = 100  # given dial size

zero_count = 0

for move in moves:
    dir = move[0]
    dist = int(move[1:])

    move_zeroes = dist // 100
    dist = dist % 100

    if dist > 0:
        if dir == "R":
            raw_pos = dial_pos + dist
        elif dir == "L":
            # Handle wrap-around for left movement
            if dial_pos == 0:
                dial_pos = DIAL_SIZE
            raw_pos = dial_pos - dist
        end_pos = raw_pos % DIAL_SIZE
        if end_pos == 0 or raw_pos != end_pos:
            move_zeroes += 1
        dial_pos = end_pos

    zero_count += move_zeroes
    # print(f"{move} {dial_pos} {move_zeroes}")

# Count the number of times the dial lands on zero
print("\nFinal zero count: ", zero_count)
