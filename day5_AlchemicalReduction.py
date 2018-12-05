"""
https://adventofcode.com/2018/day/5
"""

from typing import List, Dict
from string import ascii_lowercase

def react(unit1: str, unit2: str) -> bool:
    same_type = unit1.lower() == unit2.lower()
    opposite_polarity = unit1.isupper() ^ unit2.isupper()

    return same_type & opposite_polarity

assert react("a", "A") == True
assert react("A", "A") == False
assert react("A", "a") == True
assert react("A", "B") == False
assert react("b", "b") == False

TEST_INPUT = list("dabAcCaCBAcCcaDA")

def reduction(polymer: List[str]) -> int:
    # print(len(polymer))
    while True:
        polymer = polymer.copy()
        to_remove = []
        ix = 0
        # for ix in range(len(polymer)-1):
        while ix < (len(polymer) - 1):
            nix = ix + 1
            unit1 = polymer[ix]
            unit2 = polymer[nix]
            remove = react(unit1, unit2)
            if remove:
                to_remove.append(ix)
                to_remove.append(nix)
                ix+=2   
            else:
                ix +=1
        for rem in reversed(to_remove):
            del polymer[rem]
        #print(to_remove)
        if not to_remove:
            return len(polymer)


def remove_units(polymer: List[str], to_remove: str) -> List[str]:
    new_polymer = [unit for unit in polymer
                        if unit.lower() != to_remove]

    return new_polymer


def find_length_of_good(polymer: List[str]) -> int:
    after_remove: Dict[str, int] = {}
    for letter in ascii_lowercase:
        print(f"Checking {letter}")
        new_polymer = remove_units(polymer, letter)
        length = reduction(new_polymer)
        after_remove[letter] = length
    return min(after_remove.values())

assert reduction(TEST_INPUT) == 10
assert find_length_of_good(TEST_INPUT) == 4

with open("day5_input1.txt", "r") as f:
    polymer = f.read()

#print(len(polymer))

#print(reduction(list(polymer)))

print(find_length_of_good(list(polymer)))