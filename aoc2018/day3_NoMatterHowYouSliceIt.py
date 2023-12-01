"""
https://adventofcode.com/2018/day/3
"""
import re
import sys
from typing import List, NamedTuple, Tuple, Dict
from collections import Counter

class Claim(NamedTuple):
    id: int
    x_pos: int
    y_pos: int
    width: int
    height: int

def parse_claim(claim: str) -> Claim:
    _, id, pos, size = re.split("[#@:]", claim)
    x_pos, y_pos = pos.split(",")
    width, height = size.split("x")

    return Claim(int(id), 
                 int(x_pos),
                 int(y_pos),
                 int(width),
                 int(height))

def find_area(claim: Claim) -> List[Tuple[int, int]]:
    area: List[Tuple[int, int]] = []
    for i in range(claim.x_pos, claim.x_pos+claim.width):
        for j in range(claim.y_pos, claim.y_pos+claim.height):
            area.append((i,j))
    return area

def plot_area(area: List[Tuple[int, int]]) -> None:
    for y in range(14):
        for x in range(12):
            if (x, y) in area:
                sys.stdout.write("X")
            else:
                sys.stdout.write(".")
        sys.stdout.write("\n")

def count_overlaps(claims: List[str]) -> int:
    areas = Counter()
    overlapping = 0
    for claim in claims:
        cclaim = parse_claim(claim)
        area = find_area(cclaim)
        for ar in area:
            areas[ar] += 1
    for over in areas.values():
        if over > 1:
            overlapping += 1
    return overlapping

def get_areas_counts(claims: List[str]):
    areas: Counter = Counter()
    for claim in claims:
        cclaim = parse_claim(claim)
        area = find_area(cclaim)
        for ar in area:
            areas[ar] += 1
    return areas
    
def find_non_overlapping(claims: List[str]) -> int:
    areas = get_areas_counts(claims)
    for claim in claims:
        cclaim = parse_claim(claim)
        area = find_area(cclaim)
        overlaps = [areas.get(ar) for ar in area]
        if sum(overlaps) != len(overlaps):
            continue
        else:
            return cclaim.id
    


test = "#123 @ 3,2: 5x4"
test_area = find_area(parse_claim(test))

plot_area(test_area)


test1 = "#1 @ 1,3: 4x4"
test2 = "#2 @ 3,1: 4x4"
test3 = "#3 @ 5,5: 2x2"

assert count_overlaps([test1, test2, test3]) == 4
assert find_non_overlapping([test1, test2, test3]) == 3

with open("day3_input1.txt", "r") as f:
    lines = [line.strip() for line in f]

print(count_overlaps(lines))
print(find_non_overlapping(lines))