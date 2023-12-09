"""https://adventofcode.com/2019/day/2"""

from typing import List
from copy import copy
from utils import read_input

test_input1 = [int(x) for x in "1,9,10,3,2,3,11,0,99,30,40,50".split(",")]


def execute_program(program: List[int]) -> List[int]:
    program = copy(program)
    for i in range(0, len(program), 4):
        op = program[i]

        if op == 99:
            break
        if op == 1:
            x1 = program[i+1]
            x2 = program[i+2]
            program[program[i+3]] = program[x1] + program[x2]
        if op == 2:
            x1 = program[i+1]
            x2 = program[i+2]
            program[program[i+3]] = program[x1] * program[x2]

    return program


def assert_program(inp: str, expected_output: str) -> None:
    inp = [int(x) for x in inp.split(",")]
    expected_output = [int(x) for x in expected_output.split(",")]

    executed = execute_program(inp)
    assert executed == expected_output


assert_program("1,0,0,0,99"           ,"2,0,0,0,99")
assert_program("2,3,0,3,99"           ,"2,3,0,6,99")
assert_program("2,4,4,5,99,0"         ,"2,4,4,5,99,9801")
assert_program("1,1,1,4,99,5,6,0,99"  ,"30,1,1,4,2,5,6,0,99")


if __name__ == "__main__":
    raw_input = read_input(day=2, part=1)

    program = [int(x) for x in raw_input[0].split(",")]
    program[1] = 12
    program[2] = 2
    executed = execute_program(program)
    print(executed[0])

    for noun in range(99):
        for verb in range(99):
            program_inp = copy(program)
            program[1] = noun
            program[2] = verb

            executed = execute_program(program)
            if executed[0] == 19690720:
                print(f"Found!, Noun is {noun}, verb is {verb}")
                break
