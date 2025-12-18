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


def check_freshness(item_lines: list[str]) -> tuple[list[int], list[int]]:
    # This could be done more efficiently by sorting the items and iterating
    # only once through both lists, but that doesn't seem necessary with only
    # ~100 ranges and ~1000 items
    fresh = []
    spoiled = []
    for item in [int(line) for line in item_lines]:
        # Assume spoiled by default, because if we run past the end of the
        # fresh item ranges, it means the item being checked is spoiled
        is_fresh = False
        for start, end in fresh_items:
            if item < start:
                # All of the remaining items in the list are > item, so
                # break out and mark spoiled
                break
            if item >= start and item <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh.append(item)
        else:
            spoiled.append(item)
    return (fresh, spoiled)


setup_fresh_ranges(lines[: lines.index("")])
fresh, spoiled = check_freshness(lines[lines.index("") + 1 :])

print(f"Fresh count: {len(fresh)}")
