

import re
from itertools import product
from typing import NamedTuple, List, Tuple, Set

from itertools import chain
from collections import deque
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
    water = set(water)
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
                grid.append("~")
            elif (x, y) in coords:
                grid.append("#")
            else:
                grid.append(".")
        grid.append("\n")
    return "".join(grid)


#print(plot_clay(CLAY))



def clay_below(current: Tuple[int, int], clay_coords, water):
    in_clays =  (current[0], current[1] + 1) in set(clay_coords)
    in_water =  (current[0], current[1] + 1) in set(water)
    return in_clays or in_water

def hit_ground(current: Tuple[int, int], clays: List[Clay], water) -> Tuple[int, int]:
    
    hit = min(chain(
        [clay.y for clay in clays if clay.x == current[0] and clay.y > current[1]],
        [w[1] for w in water if w[0] == current[0] and w[1] > current[1]])
        )
    return current[0], hit - 1

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


def waterfall(current: Tuple[int, int], clay_coords, clays: List[Clay], water=[]):
    water = water[:]
    print(current)
   
    try:
        hit = hit_ground(current, clays, water)
     #   print("hit: ", hit)
    except ValueError:
        return []

    new_sources = []

    def find_right(position):
        to_the_right = settle_right(position)
        ## Moving right from hit
        while True:
            if not clay_below(to_the_right, clay_coords, water):
                # print(f"ready to move down from right {to_the_right}")
                # print([Clay(x,y) for (x,y) in clay_coords.union(all_water)],  clay_coords.union(all_water))
                new_sources.append(to_the_right)
                return None
            elif to_the_right in clay_coords:
                return to_the_right
            to_the_right = settle_right(to_the_right)

    def find_left(position):
        to_the_left = settle_left(position)
        ## Moving left from hit
        while True:
            if not clay_below(to_the_left, clay_coords, water):
                # print("ready to move down from left")
                new_sources.append(to_the_left)
                return None
            elif to_the_left in clay_coords:
                return to_the_left
            to_the_left = settle_left(to_the_left)

    
    
    right = find_right(hit)
    left = find_left(hit)
    
    while right and left:
        water.extend(fill_up(left, right, clays))
        hit = hit[0], hit[1] - 1
        right = find_right(hit)
        left = find_left(hit)
    return list(set(water)), new_sources


# settled_water = []


# water, sources = waterfall((500,0),CLAY_COORDS, CLAY, [])
# settled_water.extend(water)

# sources = deque(sources)

# while True:
#     curr = sources.popleft()
#     res = waterfall(curr,CLAY_COORDS, CLAY, settled_water)
#     if res:
#         w, s = res
#         settled_water.extend(w)
#         sources.append(s)
#         print(plot_clay(CLAY, settled_water))
#     else:
#         break




with open("day17_input.txt") as f:
    lines = [line.strip() for line in f]


clay = []

for line in lines:
    clay.extend(from_line(line))

print(plot_clay(clay, []))
settled_water = []
clay_coords: Set[Tuple[int, int]] =  {c.coords() for c in clay}

water, sources = waterfall((500,0), clay_coords, clay, [])
settled_water.extend(list(set(water)))

sources = deque(sources)

while True:
    curr = sources.popleft()
    res = waterfall(curr, clay_coords,  clay, settled_water)
    if res:
        w, s = res
        settled_water.extend(w)
        sources.extend(s)
      #  print(plot_clay(clay, settled_water))
    else:
        break


for _ in range(4):
    curr = sources.popleft()
    res = waterfall(curr, clay_coords,  clay, settled_water)
    if res:
        w, s = res
        settled_water.extend(w)
        sources.extend(s)
      #  print(plot_clay(clay, settled_water))
    else:
        break