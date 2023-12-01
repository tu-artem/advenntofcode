

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
x=502, y=11
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

CLAYS = []

for line in LINES:
    CLAYS.extend(from_line(line))


SPGING = (500, 0)

def plot_clay(clays: List[Clay], water: List[Water], pouring_water: List[Water]) -> str:
    x_min = min([clay[0] for clay in clays])
    x_max = max([clay[0] for clay in clays])
    y_min = min([clay[1] for clay in clays])
    y_max = max([clay[1] for clay in clays])

    water = set(water)
    clays = set(clays)
    pouring_water = set(pouring_water)
    grid = []

    for y in range(y_min - 1, y_max+1):
        for x in range(x_min - 1, x_max+1):
            if (x, y) == SPGING:
                grid.append("+")
            elif (x, y) in water:
                grid.append("~")
            elif (x, y) in pouring_water:
                grid.append("|")
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
    pouring_water = []
    try:
        hit = hit_ground(current, clays, water)
     #   print("hit: ", hit)
    except ValueError:
        return water, [], [(current[0], y) for y in range(current[1] + 1, 1 + max([clay[1] for clay in clays]))]

    ## Count pouring water
    pouring_water.extend([(current[0], y) for y in range(current[1] + 1, hit[1])])

    new_sources = []

    def find_right(position):
        to_the_right = settle_right(position)
        ## Moving right from hit
        while True:
            if not clay_below(to_the_right, clays, water):
                # print(f"ready to move down from right {to_the_right}")
                # print([Clay(x,y) for (x,y) in clays.union(all_water)],  clays.union(all_water))
                new_sources.append(to_the_right)
                pouring_water.extend([(x, to_the_right[1]) for x in range(position[0], to_the_right[0]+1)])
                return False
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
                pouring_water.extend([(x, to_the_left[1]) for x in range(position[0], to_the_left[0]-1, -1)])
             
                return False
            elif to_the_left in clays:
                return to_the_left
            to_the_left = settle_left(to_the_left)

    
    
    right = find_right(hit)
    left = find_left(hit)

    if left and not right:
        pouring_water.extend([(x, left[1]) for x in range(left[0]+1, hit[0])])
    
    if right and not left:
        pouring_water.extend([(x, right[1]) for x in range(hit[0]+1, right[0])])

    while right and left:
        water.extend(fill_up(left, right))
        hit = hit[0], hit[1] - 1
        right = find_right(hit)
        left = find_left(hit)  
    if left and not right:
        pouring_water.extend([(x, left[1]) for x in range(left[0]+1, hit[0])])
    if right and not left:
        pouring_water.extend([(x, right[1]) for x in range(hit[0]+1, right[0])])
    return water, new_sources, pouring_water




def flow(clays: List[Clay], show=False):

    water, sources, pouring_water = waterfall((500, 0), clays, [])
    sources = deque(sources)
    passed_sources = set()
    
    while len(sources) > 0:
    #     print("Settled:", len(water), len(set(water)))
    #     print("Pouring:", len(pouring_water), len(set(pouring_water)))
        curr = sources.pop()
        passed_sources.add(curr)
        water, s, pw = waterfall(curr, clays, water)
        pouring_water.extend(pw)
        sources.extend([sor for sor in s if sor not in passed_sources])
        if show:
            print(plot_clay(clays, water, pouring_water))

    return water,pouring_water,  sources, passed_sources


# w, s = waterfall((500, 0), CLAY, [])
# w, s = waterfall((500, 0), CLAY, w)

with open("day17_input.txt") as f:
    lines = [line.strip() for line in f]


clays = []

for line in lines:
    clays.extend(from_line(line))

# print(plot_clay(clays, []))


# water,pouring_water, sources, passed = flow(CLAYS)
# print(plot_clay(CLAYS, water, pouring_water))



# assert len(set(chain(water, pouring_water))) == 57


water,pouring_water, sources, passed = flow(clays)
print(plot_clay(clays, water, pouring_water))

ans = set(chain(water, pouring_water))


y_min = min([clay[1] for clay in clays])
y_max = max([clay[1] for clay in clays])


aaa = {a for a in ans if a[1] >= y_min and a[1]<=y_max}
len(aaa)



### Part 2
print(len(set(water)))