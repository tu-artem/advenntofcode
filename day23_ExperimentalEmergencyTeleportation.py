import re
from typing import NamedTuple, List

RAW = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1"""


class Nanobot(NamedTuple):
    x: int
    y: int
    z: int
    r: int

    @staticmethod
    def from_string(raw: str) -> "Nanobot":
        rgx = r"pos=<(.*)>, r=([0-9]+)"
        pos, radius = re.match(rgx, raw).groups()
        x, y, z = [int(c) for c in pos.split(",")]

        return Nanobot(x, y, z, int(radius))

    def manhattan_distance(self, other: "Nanobot") -> int:
        return (abs(self.x - other.x)
              + abs(self.y - other.y)
              + abs(self.z - other.z))

BOTS = [Nanobot.from_string(line) for line in RAW.split("\n")]

STRONGEST = max(BOTS, key=lambda x: x.r)


assert len([bot for bot in BOTS if bot.manhattan_distance(STRONGEST) <= STRONGEST.r]) == 7



with open("day23.txt") as f:
    raw = [line.strip() for line in f]

bots = [Nanobot.from_string(line) for line in raw]


strongest = max(bots, key=lambda x: x.r)


print(len([bot for bot in bots if bot.manhattan_distance(strongest) <= strongest.r]))
