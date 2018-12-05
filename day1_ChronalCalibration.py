"""
https://adventofcode.com/2018/day/1
"""

from typing import List, Set
from itertools import cycle

def calibration(changes: List[int]) -> int:
    return sum(changes)

def clean_input(inp: str) -> List[int]:
    return [int(x) for x in inp.split(",")]

def reach_twice(changes: List[int]) -> int:
    freqs = set([0])
    current = 0
    for change in cycle(changes):
        current += change
        if current not in freqs:
            freqs.add(current)
        else:
            break
    return current

if __name__ == "__main__":
    
    
    input1 = clean_input("+1, -2, +3, +1")

    assert calibration(input1) == 3 
    assert reach_twice(input1) == 2   

    assert calibration(clean_input("+1, +1, +1")) ==  3
    assert calibration(clean_input("+1, +1, -2")) ==  0
    assert calibration(clean_input("-1, -2, -3")) == -6

    assert reach_twice(clean_input("+1, -1")) == 0
    assert reach_twice(clean_input("+3, +3, +4, -2, -4")) == 10 
    assert reach_twice(clean_input("-6, +3, +8, +5, -6")) == 5 
    assert reach_twice(clean_input("+7, +7, -2, -7, -4")) == 14 

    with open("day1_input1.txt", "r") as inp:
        INPUT = inp.readlines()

    print(calibration([int(x) for x in INPUT]))
    print(reach_twice([int(x) for x in INPUT]))