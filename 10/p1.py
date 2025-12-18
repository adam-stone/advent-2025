import re
import sys
from collections import deque


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)


class Machine:
    def __init__(
        self,
        target: tuple[bool, ...],
        wiring: tuple[tuple[int, ...], ...],
        power: tuple[int, ...],
    ):
        assert len(target) == len(power)
        self.target = target
        self.wiring = wiring
        self.power = power

    def push_button(
        self, button_idx: int, lights: tuple[bool, ...]
    ) -> tuple[bool, ...]:
        new_lights = list(lights)
        for light_idx in self.wiring[button_idx]:
            new_lights[light_idx] = not new_lights[light_idx]
        return tuple(new_lights)


def parse_line(line: str) -> Machine:
    m = re.match(r"\[([\.#]+)\] ([ \d\(\)\,]+) \{([\d,]+)\}", line)
    assert m is not None, f"Line does not match expected format: {line}"
    target_str, wiring_str, power_str = m.groups()
    target = tuple(c == "#" for c in target_str)
    wiring = tuple(
        tuple(int(x) for x in block.strip(" ()").split(","))
        for block in wiring_str.split()
    )
    power = tuple(int(x) for x in power_str.split(","))
    return Machine(target, wiring, power)


machines: list[Machine] = []

for line in lines:
    machines.append(parse_line(line))

min_presses = []
for m in machines:
    start_lights = tuple(False for _ in m.target)
    press_distance = {start_lights: 0}
    to_visit = deque([start_lights])
    while to_visit:
        lights = to_visit.popleft()
        presses = press_distance[lights]
        for button_idx in range(len(m.wiring)):
            new_lights = m.push_button(button_idx, lights)
            new_presses = presses + 1
            if m.target in press_distance and press_distance[m.target] <= new_presses:
                continue
            if (
                new_lights not in press_distance
                or new_presses < press_distance[new_lights]
            ):
                press_distance[new_lights] = new_presses
                to_visit.append(new_lights)
    min_presses.append(press_distance[m.target])

for i, m in enumerate(min_presses):
    print(f"Machine {i}: {m} presses")
print(f"Total presses: {sum(min_presses)}")
