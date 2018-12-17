

import re
from itertools import product
from typing import NamedTuple, List, Tuple, Set

from itertools import chain
from collections import deque


Clay = Tuple[int, int]
Water = Tuple[int, int] 


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

    return coords


LINES = RAW.split("\n")

CLAY = []

for line in LINES:
    CLAY.extend(from_line(line))


SPGING = (500, 0)

def plot_clay(clays: List[Clay], water: List[Water]) -> str:
    x_min = min([clay[0] for clay in clays])
    x_max = max([clay[0] for clay in clays])
    y_min = min([clay[1] for clay in clays])
    y_max = max([clay[1] for clay in clays])

    water = set(water)
    clays = set(clays)

    grid = []

    for y in range(y_min - 1, y_max+1):
        for x in range(x_min - 1, x_max+1):
            if (x, y) == SPGING:
                grid.append("+")
            elif (x, y) in water:
                grid.append("~")
            elif (x, y) in clays:
                grid.append("#")
            else:
                grid.append(".")
        grid.append("\n")
    return "".join(grid)


#print(plot_clay(CLAY))



def clay_below(current: Tuple[int, int], clays, water):
    in_clays =  (current[0], current[1] + 1) in clays
    in_water =  (current[0], current[1] + 1) in water
    return in_clays or in_water

def hit_ground(current: Tuple[int, int], clays: List[Clay], water) -> Tuple[int, int]:
    
    hit = min(chain(
        [clay[1] for clay in clays if clay[0] == current[0] and clay[1] >= current[1]],
        [w[1] for w in water if w[0] == current[0] and w[1] > current[1]])
        )
    return current[0], hit - 1

def settle_right(current: Tuple[int, int]) -> Tuple[int, int]:
    x, y = current
    return x + 1, y

def settle_left(current: Tuple[int, int]) -> Tuple[int, int]:
    x, y = current
    return x - 1, y

def fill_up(left, right):
    assert left[1] == right[1]
    water_cells = []
    y = left[1]

   
    for x in range(left[0]+1, right[0]):
        water_cells.append((x, y))
    
    return water_cells


def waterfall(current: Tuple[int, int], clays: List[Clay], water=[]):
    print(current)
    water = water[:]
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
            if not clay_below(to_the_right, clays, water):
                # print(f"ready to move down from right {to_the_right}")
                # print([Clay(x,y) for (x,y) in clays.union(all_water)],  clays.union(all_water))
                new_sources.append(to_the_right)
                return None
            elif to_the_right in clays:
                return to_the_right
            to_the_right = settle_right(to_the_right)

    def find_left(position):
        to_the_left = settle_left(position)
        ## Moving left from hit
        while True:
            if not clay_below(to_the_left, clays, water):
                # print("ready to move down from left")
                new_sources.append(to_the_left)
                return None
            elif to_the_left in clays:
                return to_the_left
            to_the_left = settle_left(to_the_left)

    
    
    right = find_right(hit)
    left = find_left(hit)
    
    while right and left:
        water.extend(fill_up(left, right))
        hit = hit[0], hit[1] - 1
        right = find_right(hit)
        left = find_left(hit)
    return water, new_sources




def flow(clays: List[Clay], show=False):

    water, sources = waterfall((500, 0), clays, [])

    sources = deque(sources)

    while True:
        print(len(water), len(set(water)))
        curr = sources.popleft()
        res = waterfall(curr, clays, water)
        if res:
            water, s = res
            sources.extend(s)
            if show:
                print(plot_clay(clays, water))
        else:
            break
    return water


# w, s = waterfall((500, 0), CLAY, [])
# w, s = waterfall((500, 0), CLAY, w)

with open("day17_input.txt") as f:
    lines = [line.strip() for line in f]


claysss = []

for line in lines:
    claysss.extend(from_line(line))

# print(plot_clay(clays, []))


water = flow(claysss)

# print(plot_clay(clays, water))