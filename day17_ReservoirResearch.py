

import re
from itertools import product
from typing import NamedTuple, List, Tuple, Set

from itertools import chain

class Clay(NamedTuple):
    x: int
    y: int

    def coords(self):
        return self.x, self.y

RAW = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""

rgx = r"=([0-9]+)$|([0-9]+)\.\.([0-9]+)$"

def from_line(line: str) -> List[Clay]:
    x_raw, y_raw = sorted(line.split(", "))
    
    xs = [int(x) for x in re.search(rgx, x_raw).groups() if x]
    ys = [int(y) for y in re.search(rgx, y_raw).groups() if y]



    coords = product(range(min(xs), max(xs)+1), range(min(ys), max(ys)+1))

    return [Clay(*coord) for coord in coords]


LINES = RAW.split("\n")

CLAY = []

for line in LINES:
    CLAY.extend(from_line(line))


SPGING = (500, 0)

def plot_clay(clays: List[Clay], water: List[Tuple[int, int]]) -> str:
    coords = {clay.coords() for clay in clays}

    x_min = min([clay.x for clay in clays])
    x_max = max([clay.x for clay in clays])
    y_min = min([clay.y for clay in clays])
    y_max = max([clay.y for clay in clays])

    grid = []

    for y in range(y_min - 1, y_max+1):
        for x in range(x_min - 1, x_max+1):
            if (x, y) == SPGING:
                grid.append("+")
            elif (x, y) in water:
                grid.append("|")
            elif (x, y) in coords:
                grid.append("#")
            else:
                grid.append(".")
        grid.append("\n")
    return "".join(grid)


#print(plot_clay(CLAY))



def clay_below(current: Tuple[int, int], clays: List[Clay], water):
    in_clays =  (current[0], current[1] + 1) in {clay.coords() for clay in clays}
    in_water =  (current[0], current[1] + 1) in set(water)
    return in_clays or in_water

def hit_ground(current: Tuple[int, int], clays: List[Clay], water) -> Tuple[int, int]:
    
    hit = min(chain(
        [clay.y for clay in clays if clay.x == current[0] and clay.y > current[1]],
        [w[1] for w in water if w[0] == current[0] and w[1] > current[1]])
        )
    return current[0], hit - 1


def one_up(current: Tuple[int, int]) -> Tuple[int, int]:
    x, y = current
    return x, y - 1


def fall_down(current: Tuple[int, int]) -> Tuple[int, int]:
    x, y = current
    return x, y + 1

def settle_right(current: Tuple[int, int]) -> Tuple[int, int]:
    x, y = current
    return x + 1, y

def settle_left(current: Tuple[int, int]) -> Tuple[int, int]:
    x, y = current
    return x - 1, y

def fill_up(left, right, clays):
    assert left[1] == right[1]
    water_cells = []
    y = left[1]

   
    for x in range(left[0]+1, right[0]):
        water_cells.append((x, y))
    
    return water_cells

CLAY_COORDS: Set[Tuple[int, int]] =  {clay.coords() for clay in CLAY}


def waterfall(current: Tuple[int, int], clays: List[Clay], water=[]):
    print(current)
    clay_coords = {clay.coords() for clay in clays}
    try:
        hit = hit_ground(current, clays, water)
     #   print("hit: ", hit)
    except ValueError:
        return []
    to_the_right = settle_right(hit)
    to_the_left = settle_left(hit)
    right = None
    ## Moving right from hit
    while True:
        if not clay_below(to_the_right, clays, water):
         #   print(f"ready to move down from right {to_the_right}")
            # print([Clay(x,y) for (x,y) in clay_coords.union(all_water)],  clay_coords.union(all_water))
            right = None
            water.extend(waterfall(to_the_right, clays, water))
            break
        elif to_the_right in clay_coords:
            right = to_the_right
            break
        to_the_right = settle_right(to_the_right)

    left = None
    ## Moving left from hit
    while True:
        if not clay_below(to_the_left, clays, water):
         #   print("ready to move down from left")
            left = None
            water.extend(waterfall(to_the_left, clays,  water))
            break
        elif to_the_left in clay_coords:
            left = to_the_left
            break
        to_the_left = settle_left(to_the_left)

    if right and left:
        water.extend(fill_up(left, right, clays))
        # print(plot_clay(clays, water))
        water.extend(waterfall(current, clays,  water))
    
    return water

waterfall((500,0), CLAY, [])



with open("day17_input.txt") as f:
    lines = [line.strip() for line in f]


clay = []

for line in lines:
    clay.extend(from_line(line))



waters = waterfall((500, 0), clay, [])

# print(plot_clay(clay, []))

