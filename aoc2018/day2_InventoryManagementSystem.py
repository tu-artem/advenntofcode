"""
https://adventofcode.com/2018/day/2
"""

from collections import Counter
from typing import List, Tuple

def count_letters(id: str, appears: int = 2) -> bool:
    letters = Counter(id)

    for count in letters.values():
        if count == appears:
            return True
    return False

def get_checksum(input: List[str]) -> int:
    appears_two_times=0
    appears_three_times=0
    for id in input:
        appears_two_times += count_letters(id, appears=2)
        appears_three_times += count_letters(id, appears=3)

    return appears_three_times * appears_two_times


def get_distane(id1: str, id2: str) -> Tuple[int, str]:
    assert len(id1) == len(id2)
    distance: int = 0
    common: List[str] = []
    for letter1, letter2 in zip(id1, id2):
        if letter1 != letter2:
            distance += 1
        else:
            common.append(letter1)
    
    return distance, "".join(common)

def find_similar_boxes(ids: List[str]) -> str:
    for id1 in ids:
        for id2 in ids:
            distance, common = get_distane(id1, id2)
            if distance == 1:
                return common
    return ""


assert count_letters("abcdef", appears=2) == False
assert count_letters("bababc", appears=2) == True
assert count_letters("bababc", appears=3) == True


INPUT1 = [
    "abcdef",
    "bababc",
    "abbcde",
    "abcccd",
    "aabcdd",
    "abcdee",
    "ababab"
    ]

INPUT2 = [
    "abcde",
    "fghij",
    "klmno",
    "pqrst",
    "fguij",
    "axcye",
    "wvxyz"
    ]

assert get_checksum(INPUT1) == 12


assert get_distane("abcde", "axcye") == (2, "ace")
assert get_distane("fghij", "fguij") == (1, "fgij")

assert find_similar_boxes(INPUT2) == "fgij"

if __name__ == "__main__":


    with open("day2_input1.txt", "r") as inp:
        lines = [line.strip() for line in inp]

    print(get_checksum(lines))
    print(find_similar_boxes(lines))