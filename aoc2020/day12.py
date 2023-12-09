"""--- Day 12: Rain Risk ---
Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety, it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values. After staring at them for a few minutes, you work out what they probably mean:

Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.
The ship starts by facing east. Only the L and R actions change the direction the ship is facing. (That is, if the ship is facing east and the next instruction is N10, the ship would move north 10 units, but would still move east if the following action were F.)

For example:

F10
N3
F7
R90
F11
These instructions would be handled as follows:

F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
N3 would move the ship 3 units north to east 10, north 3.
F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
F11 would move the ship 11 units south to east 17, south 8.
At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?"""

RAW = """F10
N3
F7
R90
F11"""

from typing import NamedTuple, Tuple, List
from itertools import cycle

class Instruction(NamedTuple):
    name: str
    value: int


def make_instructions(raw: str) -> List[Instruction]:
    instr = [(line[0], int(line[1:])) for line in raw.split("\n")]

    return [Instruction(*i) for i in instr]


def navigate(instructions: List[Instruction]) -> Tuple[int, int]:
    location = [0, 0]
    directions = "ESWN"
    current_direction = 0

    def move(direction, value):
        if direction == "E":
            location[0] += value
        elif direction == "W":
            location[0] -= value
        elif direction == "N":
            location[1] += value
        elif direction == "S":
            location[1] -= value

    for ins in instructions:
        if ins.name in ("E", "W", "N", "S"):
            move(ins.name, ins.value)
        elif ins.name == "F":
            move(directions[current_direction], ins.value)
        elif ins.name == "R":
            # Right turn E -> S -> W -> N
            n_turns = ins.value // 90
            current_direction = (current_direction + n_turns) % 4
        elif ins.name == "L":
            # Right turn E -> S -> W -> N
            n_turns = ins.value // 90
            current_direction = (current_direction - n_turns) % 4

    return tuple(location)


INSTRUCTIONS = make_instructions(RAW)


assert navigate(INSTRUCTIONS) == (17, -8)


with open("data/12.txt") as f:
    raw = f.read().strip()

instructions = make_instructions(raw)

final_location = navigate(instructions)

print("Part1:", abs(final_location[0]) + abs(final_location[1]))



def navigate2(instructions: List[Instruction]) -> Tuple[int, int]:
    ship_location = [0, 0]
    waypoint_location = [10, 1]

    # directions = "ESWN"
    # current_direction = 0

    right_rot = [[0, 1], [-1, 0]]
    left_rot = [[0, -1], [1, 0]]


    def move(location, direction, value):
        if direction == "E":
            location[0] += value
        elif direction == "W":
            location[0] -= value
        elif direction == "N":
            location[1] += value
        elif direction == "S":
            location[1] -= value

    for ins in instructions:
        if ins.name in ("E", "W", "N", "S"):
            move(waypoint_location, ins.name, ins.value)
        elif ins.name == "F":

            ship_location[0] += waypoint_location[0] * ins.value
            ship_location[1] += waypoint_location[1] * ins.value


        elif ins.name == "R":
            n_turns = ins.value // 90
            for _ in range(n_turns):
                waypoint_location = [(x[0] * y[0] + x[1] * y[1]) for x, y in list(zip([waypoint_location] * 2, right_rot))]
        elif ins.name == "L":
            n_turns = ins.value // 90
            for _ in range(n_turns):
                waypoint_location = [(x[0] * y[0] + x[1] * y[1]) for x, y in list(zip([waypoint_location] * 2, left_rot))]

    return tuple(ship_location)


assert navigate2(INSTRUCTIONS) == (214, -72)


final_location2 = navigate2(instructions)

print("Part1:", abs(final_location2[0]) + abs(final_location2[1]))
