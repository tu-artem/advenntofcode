"""
https://adventofcode.com/2018/day/12
"""

from typing import Dict, List,Set
from collections import defaultdict

TEST_INIT = """#..#.#..##......###...###"""
TEST_GENERATIONS =  """...## => #
                       ..#.. => #
                       .#... => #
                       .#.#. => #
                       .#.## => #
                       .##.. => #
                       .#### => #
                       #.#.# => #
                       #.### => #
                       ##.#. => #
                       ##.## => #
                       ###.. => #
                       ###.# => #
                       ####. => #"""



def parse_changes(changes: str):
    bool_changes = set()
    changes = [x.strip() for x in changes.split("\n")]
    for c in changes:
        change = c.strip()
        if change[-1] == "#":
            bool_changes.add(tuple([x=="#" for x in change[:5]]))
    return bool_changes

changes = parse_changes(TEST_GENERATIONS)


Plants = Dict[int, bool]

def populate_initial_state(state: str) -> Plants:
    plants = {}
    for pot, plant in enumerate(state):
        if plant == "#":
            plants[pot] = True
    
    return plants


plants = populate_initial_state(TEST_INIT)

def mutate(plants: Plants, changes) -> Plants:
    will_grow = []

    def get_neighbours(n: int):
        return (plants.get(n-2, False), 
                plants.get(n-1, False), 
                plants.get(n, False), 
                plants.get(n+1, False), 
                plants.get(n+2, False))
    
    min_ix = min(plants)
    max_ix = max(plants)

    for pot in range(min_ix, max_ix+1):
        neighbours = get_neighbours(pot)
        if neighbours in changes:
            will_grow.append(pot)


    for extra_pot in [min_ix-1, min_ix-2, max_ix+1, max_ix+2]:
        neighbours = get_neighbours(extra_pot)
        if neighbours in changes:
            will_grow.append(extra_pot)

    new_generation = dict.fromkeys(will_grow, True)

    return new_generation

print(mutate(plants, changes))


for _ in range(20):
    plants = mutate(plants, changes)



my_input = """
initial state: #.......##.###.#.#..##..##..#.#.###..###..##.#.#..##....#####..##.#.....########....#....##.#..##...

..... => .
#.... => .
..### => .
##..# => #
.###. => #
...## => .
#.#.. => .
..##. => .
##.#. => #
..#.. => .
.#... => #
##.## => .
....# => .
.#.#. => .
#..#. => #
#.### => .
.##.# => #
.#### => .
.#..# => .
####. => #
#...# => #
.#.## => #
#..## => .
..#.# => #
#.##. => .
###.. => .
##### => #
###.# => #
...#. => #
#.#.# => #
.##.. => .
##... => #"""

init_str = "#.......##.###.#.#..##..##..#.#.###..###..##.#.#..##....#####..##.#.....########....#....##.#..##..."

changes_str = """..... => .
#.... => .
..### => .
##..# => #
.###. => #
...## => .
#.#.. => .
..##. => .
##.#. => #
..#.. => .
.#... => #
##.## => .
....# => .
.#.#. => .
#..#. => #
#.### => .
.##.# => #
.#### => .
.#..# => .
####. => #
#...# => #
.#.## => #
#..## => .
..#.# => #
#.##. => .
###.. => .
##### => #
###.# => #
...#. => #
#.#.# => #
.##.. => .
##... => #"""


changes = parse_changes(changes_str)

plants = populate_initial_state(init_str)


for _ in range(500):
    plants = mutate(plants, changes)
    print(sum(plants.keys()), len(plants))