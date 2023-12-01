"""
https://adventofcode.com/2018/day/6
"""

from typing import List, Tuple, NamedTuple, Dict, Optional
from collections import Counter

TEST_CASE = """1, 1
               1, 6
               8, 3
               3, 4
               5, 5
               8, 9""".split("\n")


class Coord(NamedTuple):
    x: int
    y: int

def find_boundaries(coords: List[Coord]) -> Tuple[Coord, Coord]:
    """Scans all the input corrdinanes and returns Coord_hi and Coord_lo
    that defines the boundary around all the input coords
    """
    x_hi = min(coord.x for coord in coords)
    y_hi = min(coord.y for coord in coords)
    x_lo = max(coord.x for coord in coords)
    y_lo = max(coord.y for coord in coords)
   
    return Coord(x_hi, y_hi), Coord(x_lo, y_lo)

def distance(c1: Coord, c2: Coord) -> int:
    dist = abs(c1.x-c2.x) + abs(c1.y-c2.y)
    return dist

def find_closest(coord: Coord, coords: List[Coord]) -> Optional[Coord]:
    min_dist = distance(coord, coords[0])
    num_min = 1
    min_coord = coords[0]
    for ix in range(1, len(coords)):
        curr_dist = distance(coord, coords[ix])
        if curr_dist < min_dist:
            min_dist = curr_dist
            num_min = 1
            min_coord = coords[ix]
        elif curr_dist == min_dist:
            num_min += 1
    if num_min == 1:
        return min_coord
    return None
    

def parse_coords(raw: List[str]) -> List[Coord]:
    coords = [Coord(*tuple(map(int, coord.strip().split(", ")))) 
                        for coord in raw]
    return coords

coords = parse_coords(TEST_CASE)

def get_neighbours(coords: List[Coord]) -> Dict[Coord, int]:
    neighbours: Dict[Coord, int] = Counter()
    is_infinite = set()
    high, low = find_boundaries(coords)

    for x in range(high.x, low.x+1):
        for y in range(high.y, low.y+1):
            closest = find_closest(Coord(x,y), coords)
            if closest:
                neighbours[closest] += 1
                if x == high.x or x == low.x or y == high.y or y == low.y:
                    is_infinite.add(closest)
    return {n:neighbours[n] for n in neighbours if n not in is_infinite}


def total_distance(coord: Coord, coords: List[Coord]) ->int:
    total_distance = 0
    for c in coords:
        total_distance += distance(c, coord)
    return total_distance

def safe_distance(coords: List[Coord], threshold: int = 32) -> int:
    high, low = find_boundaries(coords)
    safe_areas = 0
    for x in range(high.x, low.x+1):
        for y in range(high.y, low.y+1):
            total_dist = total_distance(Coord(x,y), coords)
            # print(total_dist)
            if total_dist < threshold:
                safe_areas += 1
    return safe_areas

            

print(get_neighbours(coords))

with open("day6_input1.txt", "r") as f:
    coords_str = [line.strip() for line in f]


coords = parse_coords(coords_str)
neighbours = get_neighbours(coords)

print(max(neighbours.values()))

print(safe_distance(coords, threshold=10000))