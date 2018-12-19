from typing import List, Tuple

REGISTERS = [0, 0, 0, 0, 0, 0]


RAW = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""


def parse(raw: str) -> List[List[str]]:
    instr = [[x  for x in line.split()] for line in raw.split("\n")[1:]]
    return instr


INSTRUCTIONS = parse(RAW)

POINTER = 0
POINTER_VAL = 0


def operate(registers: List[int], instr: List[str]) -> List[int]:
    
    after = registers[:]
    opcode = instr[0]
    A, B, C = [int(x) for x in instr[1:]] 
    if opcode == "addr":
        after[C] = registers[A] + registers[B]
        return after
    elif opcode == "addi":
        after[C] = registers[A] + B
        return after

    elif opcode == "mulr":
        after[C] = registers[A] * registers[B]
        return after
    elif opcode == "muli":
        after[C] = registers[A] * B
        return after

    elif opcode == "banr":
        after[C] = registers[A] & registers[B]
        return after
    elif opcode == "bani":
        after[C] = registers[A] & B
        return after

    elif opcode == "borr":
        after[C] = registers[A] | registers[B]
        return after
    elif opcode == "bori":
        after[C] = registers[A] | B
        return after

    elif opcode == "setr":
        after[C] = registers[A] 
        return after
    elif opcode == "seti":
        after[C] = A
        return after

    elif opcode == "gtir":
        after[C] = int(A > registers[B])
        return after

    elif opcode == "gtri":
        after[C] = int(registers[A] > B)
        return after
    elif opcode == "gtrr":
        after[C] = int(registers[A] > registers[B])
        return after

    elif opcode == "eqir":
        after[C] = int(A == registers[B])
        return after

    elif opcode == "eqri":
        after[C] = int(registers[A] == B)
        return after
    elif opcode == "eqrr":
        after[C] = int(registers[A] == registers[B])
        return after
    
    else:
        raise ValueError("Unknown opcode!")



def flow(pointer: int, pointer_contains:int, registers: List[int], instrs: List[List[str]]):
    registers = registers[:]
    
    instr = instrs[pointer_contains]
    
    registers[pointer] = pointer_contains
    old_reg = registers
    registers = operate(registers, instr)
    # print(pointer_contains, registers)
    registers[pointer] = registers[pointer] + 1
    pointer_contains = registers[pointer]

    return pointer_contains, registers


# while POINTER_VAL < len(INSTRUCTIONS):
#     POINTER_VAL, REGISTERS = flow(POINTER, POINTER_VAL, REGISTERS, INSTRUCTIONS)

# print(POINTER_VAL, REGISTERS)

registers = [1, 0, 0, 0, 0, 0] ## For part 1 register 0 started with 0, for part 2 with 1

with open("day19_input.txt") as f:
    raw = f.read()

instructions = parse(raw)

pointer = 2
pointer_val = 0

all_Zero_registers = set()

i = 0
while pointer_val < len(instructions):
    pointer_val, registers = flow(pointer,pointer_val, registers, instructions)
    i += 1
    # if registers[0] == 1482:
    #     break
    all_Zero_registers.add(registers[0])


print(pointer_val, registers)


import math

def all_factors(n: int):
    factors = [n]
    for i in range(1, n // 2):
        if n % i == 0:
            factors.append(i)
    return factors