# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "scipy>=1.16.3",
# ]
# ///

import re
import sys

from scipy.optimize import linprog


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
    print("Starting")
    lines = slurp_lines(sys.argv[1] if len(sys.argv) > 1 else None)
    machines: list[Machine] = []

    for line in lines:
        machines.append(parse_line(line))

    presses = []
    for i, m in enumerate(machines):
        print(f"Processing machine {i}...")
        res = linprog(
            c=[1] * len(m.wiring),
            A_eq=m.power_factors,
            b_eq=list(m.power),
            integrality=1,
        )
        if res.success:
            presses.append(round(res.fun))
        else:
            print(f"Could not solve machine {i}\n{res}")
            exit(1)

    print(f"Sum: {sum(presses)}")


if __name__ == "__main__":
    main()
