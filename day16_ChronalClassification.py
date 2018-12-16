from typing import List
import re
from collections import Counter

def addr(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] + before[B]
    return after

def addi(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] + B
    return after

def mulr(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] * before[B]
    return after

def muli(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] * B
    return after

def banr(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] & before[B]
    return after

def bani(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] & B
    return after

def borr(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] | before[B]
    return after

def bori(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] | B
    return after

def setr(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] 
    return after

def seti(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = A
    return after

def gtir(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = A > before[B]
    return after

def gtri(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] > B
    return after

def gtrr(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] > before[B]
    return after

def eqir(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = A == before[B]
    return after

def eqri(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] == B
    return after

def eqrr(before:List[int], command: List[int]) -> List[int]:
    after = before[:]
    A, B, C = command[1:]
    after[C] = before[A] == before[B]
    return after

functions = {
    "addr":addr,
    "addi":addi,
    "mulr":mulr,
    "muli":muli,
    "banr":banr,
    "bani":bani,
    "borr":borr,
    "bori":bori,
    "gtri":gtri,
    "gtir":gtir,
    "gtrr":gtrr,
    "eqir":eqir,
    "eqri":eqri,
    "eqrr":eqrr,
    "setr":setr,
    "seti":seti
}


functions_match = {
    "addr":Counter(),
    "addi":Counter(),
    "mulr":Counter(),
    "muli":Counter(),
    "banr":Counter(),
    "bani":Counter(),
    "borr":Counter(),
    "bori":Counter(),
    "gtri":Counter(),
    "gtir":Counter(),
    "gtrr":Counter(),
    "eqir":Counter(),
    "eqri":Counter(),
    "eqrr":Counter(),
    "setr":Counter(),
    "seti":Counter()
}

rgx = r"Before: \[(.*)\]\n(.*)\nAfter:  \[(.*)\]"

with open("day16_input1.txt") as f:
    RAW = f.read()

raw_samples = re.findall(rgx, RAW)

samples = []

for sample in raw_samples:
    before = [int(x) for x in sample[0].split(",")]
    command = [int(x) for x in sample[1].split(" ")]
    after = [int(x) for x in sample[2].split(",")]

    samples.append([before, command, after])

three_or_more = 0
for sample in samples:
    matches = 0
    for name, f in functions.items():
        res = f(sample[0], sample[1])
        if res == sample[2]:
            matches += 1
            functions_match[name][sample[1][0]] += 1
    if matches >= 3:
        three_or_more += 1



code_functions = {
    0:addr,
    5:addi,
    14:mulr,
    9:muli,
    6:banr,
    15:bani,
    13:borr,
    8:bori,
    7:gtri,
    4:gtir,
    11:gtrr,
    2:eqir,
    1:eqri,
    3:eqrr,
    12:setr,
    10:seti
}

with open("day16_input2.txt") as f:
    lines = [line.strip() for line in f]


commands = [[int(x) for x in line.split(" ")] for line in lines]


registers = [0,0,0,0]

for command in commands:
    f = code_functions[command[0]]
    registers = f(registers, command)