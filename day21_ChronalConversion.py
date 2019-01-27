from day19_GoWithTheFlow import parse,  operate
from typing import List



def flow(pointer: int, pointer_contains:int, registers: List[int], instrs: List[List[str]]):
    registers = registers[:]
    
    instr = instrs[pointer_contains]
    
    registers[pointer] = pointer_contains
    old_reg = registers
    # print(instr)
 #    if pointer_contains ==30:
 #        print(registers[3])
    # if pointer_contains == 28:
    #     print(registers[4])
    registers = operate(registers, instr)
    # if pointer_contains == 7:
    #     print(registers[4])
    # registers[pointer] = registers[pointer] + 1
    pointer_contains = registers[pointer] + 1

    return pointer_contains, registers

with open("day21_input.txt") as f:
    raw = f.read()

instructions = parse(raw)

pointer = 5
registers = [10593665, 0, 0, 0, 0, 0]
pointer_val = registers[pointer]



# for i in range(100000000000):
#    #  print(registers)
#     pointer_val, registers = flow(pointer,pointer_val, registers, instructions)

### PArt 2


prev_r4 = 0
seen_r4 = set()
all_r4 = []
r3 = 2**16
r4 = 4332021

while True:
   
    r2 = r3 & 255
    r4 = r4 + r2

    r4 = r4 & 16777215
    r4 = r4 * 65899
    r4 = r4 & 16777215


    if r3 < 256:

        r2 = 1
         # print(r4)
        if r4 in seen_r4:
            break
        else:
            seen_r4.add(r4)
            all_r4.append(r4)
        r3 = r4 | 65536
        r4 = 4332021
        continue
    else:
        r2 = 0

  
    while True:
        r1 = r2 + 1
        r1 *= 256
        if r1 > r3:
            r3 = r2
            break
        else:    
            r2 += 1

all_r4[-1]