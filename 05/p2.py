import functools
import sys


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)

fresh_items: list[tuple[int, int]] = []


def setup_fresh_ranges(fresh_lines: list[str]):
    raw_ranges = [
        (int(r[0]), int(r[1])) for r in map(lambda x: x.split("-"), fresh_lines)
    ]
    raw_ranges.sort()
    open_range = raw_ranges[0]
    for item in raw_ranges[1:]:
        if item[0] > open_range[1]:
            # There is a gap between ranges, so commit the previous open range
            # and use the current item to start a new open range
            fresh_items.append(open_range)
            open_range = item
        elif item[1] > open_range[1]:
            # The item overlaps with the open range and extends it, so update
            # the open range to reflect its new extent
            open_range = (open_range[0], item[1])
        else:
            # In this case, the current item is entirely within the open range
            # so take no action
            pass
    # Commit the last working open item
    fresh_items.append(open_range)


setup_fresh_ranges(lines[: lines.index("")])

fresh_count = functools.reduce(lambda a, x: a + x[1] - x[0] + 1, fresh_items, initial=0)

print(f"Fresh count: {fresh_count}")
