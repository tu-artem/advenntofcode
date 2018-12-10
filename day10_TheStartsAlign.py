"""
https://adventofcode.com/2018/day/10
"""

from typing import NamedTuple, List, Tuple
import re
import sys

TEST_CASE = """
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
""".strip()

class Point(NamedTuple):
    x: int
    y: int
    right: int
    up: int

rgx = r"position=<([\s0-9-,]+)> velocity=<([\s0-9-,]+)>"

def parse_line(line: str) -> Point:
    position, velocity = re.match(rgx, line).groups()

    x, y = [int(n) for n in position.split(",")]
    right, up = [int(n) for n in velocity.split(",")]

    point = Point(x, y, right, up)

    return point


points = [parse_line(line) for line in TEST_CASE.split("\n")]


def find_boundaries(points: List[Point]) -> Tuple[int,int,int,int]:
    x_min = min([point.x for point in points])
    x_max = max([point.x for point in points])
    y_min = min([point.y for point in points])
    y_max =max([point.y for point in points])

    return x_min, y_min, x_max, y_max


x_min, y_min, x_max, y_max = find_boundaries(points)


def plot_starts(points: List[Point]) -> None:
    x_min,y_min, x_max, y_max, = find_boundaries(points)

    xy = set([(point.x, point.y) for point in points])

    for y in range(y_min,y_max+1):
        for x in range(x_min, x_max+1):
            ch = "#" if (x,y) in xy else "."
            sys.stdout.write(ch)
        sys.stdout.write("\n")


def move_points(points: List[Point], acceleration=1) -> List[Point]:
    new_points = [
        Point(p.x+p.right*acceleration, 
              p.y+p.up*acceleration, 
              p.right, p.up)
              for p in points
                ]
    return new_points


with open("day10_input.txt", "r") as f:
    lines = [line.strip() for line in f]


POINTS = [parse_line(line) for line in lines]


x_min, y_min, x_max, y_max = find_boundaries(POINTS)

x_distance = x_max - x_min
y_distance = y_max - y_min

sec = 0

while x_distance > 90:
    # print(x_distance)
    POINTS = move_points(POINTS, 10)
    sec += 1
    x_min, y_min, x_max, y_max = find_boundaries(POINTS)

    x_distance = x_max - x_min
    y_distance = y_max - y_min