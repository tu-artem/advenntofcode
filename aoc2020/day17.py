"""--- Day 17: Conway Cubes ---
As your flight slowly drifts through the sky, the Elves at the Mythical Information Bureau at the North Pole contact you. They'd like some help debugging a malfunctioning experimental energy source aboard one of their super-secret imaging satellites.

The experimental energy source is based on cutting-edge technology: a set of Conway Cubes contained in a pocket dimension! When you hear it's having problems, you can't help but agree to take a look.

The pocket dimension contains an infinite 3-dimensional grid. At every integer 3-dimensional coordinate (x,y,z), there exists a single cube which is either active or inactive.

In the initial state of the pocket dimension, almost all cubes start inactive. The only exception to this is a small flat region of cubes (your puzzle input); the cubes in this region start in the specified active (#) or inactive (.) state.

The energy source then proceeds to boot up by executing six cycles.

Each cube only ever considers its neighbors: any of the 26 other cubes where any of their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.

During a cycle, all cubes simultaneously change their state according to the following rules:

If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
The engineers responsible for this experimental energy source would like you to simulate the pocket dimension and determine what the configuration of cubes should be at the end of the six-cycle boot process.

For example, consider the following initial state:

.#.
..#
###
Even though the pocket dimension is 3-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1 region of the 3-dimensional space.)

Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is shown layer-by-layer at each given z coordinate (and the frame of view follows the active cells in each cycle):

Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......
After the full six-cycle boot process completes, 112 cubes are left in the active state.

Starting with your given initial configuration, simulate six cycles. How many cubes are left in the active state after the sixth cycle?"""


from typing import NamedTuple, Dict
from collections import defaultdict
from itertools import product

class Cube(NamedTuple):
    x: int
    y: int
    z: int


def make_cubes(raw: str) -> Dict[Cube, bool]:
    cubes = defaultdict(bool)
    for x, row in enumerate(raw.split("\n")):
        for y, val in enumerate(row):
            cube = Cube(x, y, 0)
            cubes[cube] = True if val == "#" else False

    return cubes


RAW = """.#.
..#
###"""

CUBES = make_cubes(RAW)


def evolution_step(cubes: Dict[Cube, bool]) -> Dict[Cube, bool]:
    max_x = max(cube.x for cube in cubes) + 1
    min_x = min(cube.x for cube in cubes) - 1
    max_y = max(cube.y for cube in cubes) + 1
    min_y = min(cube.y for cube in cubes) - 1
    max_z = max(cube.z for cube in cubes) + 1
    min_z = min(cube.z for cube in cubes) - 1

    new_cubes = defaultdict(bool)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                cube = Cube(x, y, z)
                active_neighbors = 0
                # check all 28 neighbours
                for dx, dy, dz in product((-1, 0, 1), repeat=3):
                    if dx == dy == dz == 0:
                        continue
                    neighbor_cube = Cube(x + dx, y + dy, z + dz)

                    if cubes[neighbor_cube]:
                        active_neighbors += 1

                # current active
                if cubes[cube]:
                    if active_neighbors == 2 or active_neighbors == 3:
                        new_cubes[cube] = True
                    else:
                        new_cubes[cube] = False

                # current inactive
                else:
                    if active_neighbors == 3:
                        new_cubes[cube] = True
                    else:
                        new_cubes[cube] = False

    return new_cubes


def count_active_cubes(cubes: Dict[Cube, bool], steps=6) -> int:
    for _ in range(steps):
        cubes = evolution_step(cubes)

    return sum(cubes.values())


assert count_active_cubes(CUBES, 6) == 112


with open("data/17.txt") as f:
    raw = f.read().strip()

cubes = make_cubes(raw)

print("Part1:", count_active_cubes(cubes, 6))



# PART 2


class Cube4d(NamedTuple):
    x: int
    y: int
    z: int
    w: int


def make_cubes_4d(raw: str) -> Dict[Cube4d, bool]:
    cubes = defaultdict(bool)
    for x, row in enumerate(raw.split("\n")):
        for y, val in enumerate(row):
            cube = Cube4d(x, y, 0, 0)
            cubes[cube] = True if val == "#" else False

    return cubes


RAW = """.#.
..#
###"""

CUBES4D = make_cubes_4d(RAW)


def evolution_step_4d(cubes: Dict[Cube4d, bool]) -> Dict[Cube4d, bool]:
    max_x = max(cube.x for cube in cubes) + 1
    min_x = min(cube.x for cube in cubes) - 1
    max_y = max(cube.y for cube in cubes) + 1
    min_y = min(cube.y for cube in cubes) - 1
    max_z = max(cube.z for cube in cubes) + 1
    min_z = min(cube.z for cube in cubes) - 1
    max_w = max(cube.w for cube in cubes) + 1
    min_w = min(cube.w for cube in cubes) - 1

    new_cubes = defaultdict(bool)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                for w in range(min_w, max_w + 1):
                    cube = Cube4d(x, y, z, w)
                    active_neighbors = 0
                    # check all 28 neighbours
                    for dx, dy, dz, dw in product((-1, 0, 1), repeat=4):
                        if dx == dy == dz == dw == 0:
                            continue
                        neighbor_cube = Cube4d(x + dx, y + dy, z + dz, w + dw)

                        if cubes[neighbor_cube]:
                            active_neighbors += 1

                    # current active
                    if cubes[cube]:
                        if active_neighbors == 2 or active_neighbors == 3:
                            new_cubes[cube] = True
                        else:
                            new_cubes[cube] = False

                    # current inactive
                    else:
                        if active_neighbors == 3:
                            new_cubes[cube] = True
                        else:
                            new_cubes[cube] = False

    return new_cubes


def count_active_cubes_4d(cubes: Dict[Cube4d, bool], steps=6) -> int:
    for i in range(steps):
        print(f"{i+1} iteration")
        cubes = evolution_step_4d(cubes)

    return sum(cubes.values())


assert count_active_cubes_4d(CUBES4D, 6) == 848



cubes4d = make_cubes_4d(raw)

print("Part2:", count_active_cubes_4d(cubes4d, 6))
