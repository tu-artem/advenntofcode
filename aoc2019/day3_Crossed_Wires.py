"""
For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........
Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.
"""
from typing import List, Tuple, Set

from utils import read_input


class StaticDict(dict):
    def __setitem__(self, k, v):
        if k in self:
            pass
        else:
            super().__setitem__(k, v)


def fill_wire(wire: List[str]) -> Set[Tuple[int, int]]:
    x, y = 0, 0
    path = 0
    coords = StaticDict()
    for p in wire:
        directon, path_len = p[0], int(p[1:])
        if directon == "R":
            for dx in range(x + 1, x+path_len + 1):
                path += 1
                coords[(dx, y)] = path
            x = dx
        elif directon == "U":
            for dy in range(y + 1, y+path_len + 1):
                path += 1
                coords[(x, dy)] = path
            y = dy
        elif directon == "L":
            for dx in range(x - 1, x-path_len - 1, -1):
                path += 1
                coords[(dx, y)] = path
            x = dx
        elif directon == "D":
            for dy in range(y - 1, y-path_len - 1, - 1):
                path += 1
                coords[(x, dy)] = path
            y = dy
        else:
            raise ValueError(f"Expected one of R, U, L, D for direction. Got {direction}")

    return coords


def find_crossed_wires(wire1: List[str], wire2: List[str]) -> int:
    w1_coords = set(fill_wire(wire1))
    w2_coords = set(fill_wire(wire2))

    intersected = w1_coords.intersection(w2_coords)

    return min(sum(map(abs, coord)) for coord in intersected if coord != (0, 0))


def find_closed_by_path(wire1, wire2) -> int:
    w1_coords = fill_wire(wire1)
    w2_coords = fill_wire(wire2)

    intersected = set(w1_coords).intersection(set(w2_coords))

    return min(w1_coords[c] + w2_coords[c] for c in intersected if c != (0, 0))

wire1 = "R8,U5,L5,D3".split(",")
wire2 = "U7,R6,D4,L4".split(",")

assert find_crossed_wires(wire1, wire2) == 6
assert find_closed_by_path(wire1, wire2) == 30

wire1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(",")
wire2 = "U62,R66,U55,R34,D71,R55,D58,R83".split(",")
assert find_crossed_wires(wire1, wire2) == 159
assert find_closed_by_path(wire1, wire2) == 610
wire1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(",")
wire2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(",")
assert find_crossed_wires(wire1, wire2) == 135
assert find_closed_by_path(wire1, wire2) == 410



if __name__ == "__main__":
    raw_input = read_input(day=3, part=1)
    wire1 = raw_input[0].split(",")
    wire2 = raw_input[1].split(",")
    print("Part 1")
    print(find_crossed_wires(wire1, wire2))

    print("Part 2")
    print(find_closed_by_path(wire1, wire2))
