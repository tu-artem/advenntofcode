from typing import NamedTuple, Dict, Tuple

START = (0, 0)
TARGET = (10, 10)
DEPTH = 510


class Region(NamedTuple):
    geo_index: int
    erosion: int
    r_type: int 

Position = Tuple[int, int]

Cave = Dict[Position, Region]

def create_cave(target: Position, depth: int) -> Cave:
    """The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    The region at the coordinates of the target has a geologic index of 0.
    If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
    If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
    Otherwise, the region's geologic index is the result of multiplying the erosion levels 
    of the regions at X-1,Y and X,Y-1.
    A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183. Then:

    If the erosion level modulo 3 is 0, the region's type is rocky.
    If the erosion level modulo 3 is 1, the region's type is wet.
    If the erosion level modulo 3 is 2, the region's type is narrow."""

    cave = {}
    
    # Mouth
    gi = 0
    el = (gi + depth) % 20183
    rt = el % 3
    cave[(0, 0)] = Region(gi, el, rt)

    # Target
    cave[target] = Region(gi, el, rt)

    # Fill edges
    for x in range(1, target[0] + 1):
        gi = x * 16807
        el = (gi + depth) % 20183
        rt = el % 3
        cave[(x, 0)] = Region(gi, el, rt)
    
    for y in range(1, target[1] + 1):
        gi = y * 48271
        el = (gi + depth) % 20183
        rt = el % 3
        cave[(0, y)] = Region(gi, el, rt)

    ## Fill rest
    for x in range(1, target[0] + 1):
        for y in range(1, target[1] + 1):
            if (x, y) == target:
                continue
            gi = cave[(x-1, y)].erosion * cave[(x, y-1)].erosion
            el = (gi + depth) % 20183
            rt = el % 3
            cave[(x, y)] = Region(gi, el, rt)
    
    return cave


CAVE = create_cave(TARGET, DEPTH)

assert sum([reg.r_type for reg in CAVE.values()]) == 114


# depth: 3879
# target: 8,713

cave = create_cave((8, 713), 3879)
print(sum([reg.r_type for reg in cave.values()]))

def plot_cave(cave: Cave, target: Position) -> str:
    
    signature = []
    
    types = {
        0: ".",
        1: "=",
        2: "|"
    }
    
    for y in range(target[1]):
        for x in range(target[0]):
            t = cave[(x,y)].r_type
            signature.append(types[t])
        signature.append("\n")
    return "".join(signature)
    