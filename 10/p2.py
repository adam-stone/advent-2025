import re
import sys

# This solution is better than the most naive approach, but still doesn't do
# enough pruning of the state space to run well on my personal machine


def slurp_lines(filename=None):
    if filename is None:
        return sys.stdin.read().splitlines()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


class Machine:
    def __init__(
        self,
        wiring: tuple[tuple[int, ...], ...],
        power: tuple[int, ...],
    ):
        self.wiring = wiring
        self.power = power
        self.power_factors = [
            [0 for _ in range(len(self.wiring))] for _ in range(len(self.power))
        ]
        for i, button in enumerate(wiring):
            for p in button:
                self.power_factors[p][i] = 1
        self.min_presses = None

        self.power_solve_order = []
        buttons = list(self.wiring)
        while any(buttons):
            power_freq = [
                [i in w for w in buttons].count(True) for i in range(len(self.power))
            ]
            self.power_solve_order.extend(
                [
                    i
                    for i in range(len(power_freq))
                    if power_freq[i] == 0 and i not in self.power_solve_order
                ]
            )
            next_power = power_freq.index(min([x for x in power_freq if x != 0]))
            self.power_solve_order.append(next_power)
            dead_buttons = [i for i in range(len(buttons)) if next_power in buttons[i]]
            for i in dead_buttons:
                buttons[i] = ()

    def push_button(
        self, button_idx: int, count: int, power: tuple[int, ...]
    ) -> tuple[int, ...]:
        new_power = list(power)
        for power_idx in self.wiring[button_idx]:
            new_power[power_idx] += count
        return tuple(new_power)

    def find_min_presses(
        self, start_power, start_presses=0, power_solve_idx=0, next_button_idx=0
    ):
        # If there is already a better solution, return
        if self.min_presses is not None and self.min_presses <= start_presses:
            return None

        # If the target has been reached, return
        if all(map(lambda a, b: a == b, start_power, self.power)):
            self.min_presses = start_presses
            return self.min_presses

        if any(map(lambda a, b: a > b, start_power, self.power)):
            return None

        # If there are no more powers to solve, return
        if power_solve_idx >= len(self.power_solve_order):
            return None

        # The next power to set is whichever the solve index points to
        power_to_solve = self.power_solve_order[power_solve_idx]

        # If it's already solved, move on to the next
        if start_power[power_to_solve] == self.power[power_to_solve]:
            return self.find_min_presses(
                start_power, start_presses, power_solve_idx + 1, 0
            )

        # Calculate the max number of times any button can be pressed
        button_limits = [
            min([self.power[p] - start_power[p] for p in w]) for w in self.wiring
        ]

        # Set up a list of buttons that affect the current power to solve and
        # which have not already hit their press limit
        buttons = [
            i
            for i in range(len(self.wiring))
            if i >= next_button_idx
            and power_to_solve in self.wiring[i]
            and button_limits[i] > 0
        ]

        if len(buttons) == 0:
            return None
        elif len(buttons) == 1:
            presses = button_limits[buttons[0]]
            next_power = self.push_button(buttons[0], presses, start_power)
            return self.find_min_presses(
                next_power, start_presses + presses, power_solve_idx + 1, 0
            )
        else:
            min_result = None
            for i in range(button_limits[buttons[0]] + 1):
                next_power = self.push_button(buttons[0], i, start_power)
                result = self.find_min_presses(
                    next_power,
                    start_presses + i,
                    power_solve_idx,
                    buttons[0] + 1,
                )
                if result is not None and (min_result is None or result < min_result):
                    min_result = result
            return min_result


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


def main() -> None:
    lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)
    machines: list[Machine] = []

    for line in lines:
        machines.append(parse_line(line))

    presses = []
    for i, m in enumerate(machines):
        print(f"Processing machine {i}...")
        p = m.find_min_presses([0 for _ in range(len(m.power))])
        if p is None:
            print(f"Could not find solution for machine {i}")
        else:
            print(f"  {p} presses")
        presses.append(p)

    print(f"Sum: {sum(presses)}")


if __name__ == "__main__":
    main()
