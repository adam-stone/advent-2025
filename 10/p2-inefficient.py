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
        wiring: tuple[tuple[int, ...], ...],
        power: tuple[int, ...],
    ):
        self.wiring = wiring
        self.power = power
        self.memo = {}

    def push_button(
        self, button_idx: int, count: int, power: tuple[int, ...]
    ) -> tuple[int, ...]:
        new_power = list(power)
        for power_idx in self.wiring[button_idx]:
            new_power[power_idx] += count
        return tuple(new_power)

    def find_min_presses(self) -> int:
        power = [0 for _ in range(len(self.power))]
        self.memo[tuple(power)] = 0

        to_visit = deque([tuple(power)])
        while to_visit:
            current_power = to_visit.popleft()
            new_press_count = self.memo[current_power] + 1
            for button_idx in range(len(self.wiring)):
                new_power = self.push_button(button_idx, 1, current_power)
                if all(
                    map(lambda res, target: res <= target, new_power, self.power)
                ) and (
                    new_power not in self.memo or self.memo[new_power] > new_press_count
                ):
                    self.memo[new_power] = new_press_count
                    if new_power not in to_visit:
                        to_visit.append(new_power)
        if self.power not in self.memo:
            print("Could not reach power target")
            return -1
        else:
            return self.memo[self.power]


def parse_line(line: str) -> Machine:
    m = re.match(r"\[([\.#]+)\] ([ \d\(\)\,]+) \{([\d,]+)\}", line)
    assert m is not None, f"Line does not match expected format: {line}"
    _, wiring_str, power_str = m.groups()
    wiring = tuple(
        tuple(int(x) for x in block.strip(" ()").split(","))
        for block in wiring_str.split()
    )
    power = tuple(int(x) for x in power_str.split(","))
    return Machine(wiring, power)


machines: list[Machine] = []

for line in lines:
    machines.append(parse_line(line))

min_presses = []
for i, m in enumerate(machines):
    print(f"Processing machine {i}...")
    min_presses.append(m.find_min_presses())

for i, m in enumerate(min_presses):
    print(f"Machine {i}: {m} presses")
print(f"Total presses: {sum(min_presses)}")
