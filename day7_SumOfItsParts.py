"""
https://adventofcode.com/2018/day/7
"""


import re
from typing import NamedTuple, List, Tuple

r"""
  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
"""

TEST_CASE = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""


rgx = "Step ([A-Z]) must be finished before step ([A-Z]) can begin."

class Edge(NamedTuple):
    fr: str = None
    to: str = None
    
    @classmethod
    def from_str(self, raw: str) -> 'Edge':
        rgx_found = re.match(rgx, raw).groups()
        return Edge(*rgx_found)


edges = [Edge.from_str(x.strip()) for x in TEST_CASE.split("\n") if x]





candidates = []
executed = {}


print(edges)

with open("day7_input.txt") as f:
    lines = [line.strip() for line in f]

edges = [Edge.from_str(x.strip()) for x in lines]

