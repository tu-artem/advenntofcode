"""--- Day 14: Docking Data ---
As your ferry approaches the sea port, the captain asks for your help again. The computer system that runs this port isn't compatible with the docking program on the ferry, so the docking parameters aren't being correctly initialized in the docking program's memory.

After a brief inspection, you discover that the sea port's computer system uses a strange bitmask system in its initialization program. Although you don't have the correct decoder chip handy, you can emulate it in software!

The initialization program (your puzzle input) can either update the bitmask or write a value to memory. Values and memory addresses are both 36-bit unsigned integers. For example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the value 11 to memory address 8.

The bitmask is always given as a string of 36 bits, written with the most significant bit (representing 2^35) on the left and the least significant bit (2^0, that is, the 1s bit) on the right. The current bitmask is applied to values immediately before they are written to memory: a 0 or 1 overwrites the corresponding bit in the value, while an X leaves the bit in the value unchanged.

For example, consider the following program:

mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
This program starts by specifying a bitmask (mask = ....). The mask it specifies will overwrite two bits in every written value: the 2s bit is overwritten with 0, and the 64s bit is overwritten with 1.

The program then attempts to write the value 11 to memory address 8. By expanding everything out to individual bits, the mask is applied as follows:

value:  000000000000000000000000000000001011  (decimal 11)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001001001  (decimal 73)
So, because of the mask, the value 73 is written to memory address 8 instead. Then, the program tries to write 101 to address 7:

value:  000000000000000000000000000001100101  (decimal 101)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001100101  (decimal 101)
This time, the mask has no effect, as the bits it overwrote were already the values the mask tried to set. Finally, the program tries to write 0 to address 8:

value:  000000000000000000000000000000000000  (decimal 0)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001000000  (decimal 64)
64 is written to address 8 instead, overwriting the value that was there previously.

To initialize your ferry's docking program, you need the sum of all values left in memory after the initialization program completes. (The entire 36-bit address space begins initialized to the value 0 at every address.) In the above example, only two values in memory are not zero - 101 (at address 7) and 64 (at address 8) - producing a sum of 165.

Execute the initialization program. What is the sum of all values left in memory after it completes?"""

from typing import Dict, NamedTuple, List
from itertools import zip_longest, product

class Command(NamedTuple):
    address: int
    value: int
    mask: str



def apply_mask1(mask: str, value: int) -> int:
    bin_value = bin(value)
    new_value = "".join( m if m != "X" else v for v, m in zip_longest(bin_value[:1:-1], mask[::-1], fillvalue="0"))

    return int(new_value[::-1], 2)


mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
# mem[8] = 11
# mem[7] = 101
# mem[8] = 0

assert apply_mask1(mask, 11) == 73
assert apply_mask1(mask, 101) == 101
assert apply_mask1(mask, 0) == 64


def make_commands(raw: str) -> List[Command]:
    commands = []
    for line in raw.split("\n"):
        if line.strip().startswith("mask = "):
            current_mask = line[len("mask = "):]
        else:
            address, value = line.split(" = ")
            value = int(value)
            address = int(address[len("mem["):-1])
            command = Command(address, value, current_mask)
            commands.append(command)

    return commands


def run_program1(commands: List[Command]):
    mem = {}
    for command in commands:
        value = apply_mask1(command.mask, command.value)
        mem[command.address] = value

    return sum(mem.values())

RAW = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

COMMANDS = make_commands(RAW)


assert run_program1(COMMANDS) == 165


with open("data/14.txt") as f:
    raw = f.read().strip()


commands = make_commands(raw)

print("Part1:", run_program1(commands))


# PART 2

"""--- Part Two ---
For some reason, the sea port's computer system still can't communicate with your ferry's docking program. It must be using version 2 of the decoder chip!

A version 2 decoder chip doesn't modify the values being written at all. Instead, it acts as a memory address decoder. Immediately before a value is written to memory, each bit in the bitmask modifies the corresponding bit of the destination memory address in the following way:

If the bitmask bit is 0, the corresponding memory address bit is unchanged.
If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
If the bitmask bit is X, the corresponding memory address bit is floating.
A floating bit is not connected to anything and instead fluctuates unpredictably. In practice, this means the floating bits will take on all possible values, potentially causing many memory addresses to be written all at once!

For example, consider the following program:

mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
When this program goes to write to memory address 42, it first applies the bitmask:

address: 000000000000000000000000000000101010  (decimal 42)
mask:    000000000000000000000000000000X1001X
result:  000000000000000000000000000000X1101X"""


def apply_mask2(mask: str, value: int) -> List[int]:
    addresses = []

    bin_value = bin(value)
    masked = [v if m == "0" else m for v, m in zip_longest(bin_value[:1:-1], mask[::-1], fillvalue="0")]

    num_floating = sum(m == "X" for m in masked)

    substitutions = product(("0", "1"), repeat=num_floating)

    for sub in substitutions:
        result = masked[::-1].copy()
        for s in sub:
            result[result.index("X")] = s
        result = "".join(result)
        addresses.append(int(result, 2))

    return addresses



def run_program2(commands: List[Command]):
    mem = {}
    for command in commands:
        addresses = apply_mask2(command.mask, command.address)
        for address in addresses:
            mem[address] = command.value

    return sum(mem.values())


print("Part2:", run_program2(commands))
