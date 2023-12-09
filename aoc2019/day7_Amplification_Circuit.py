from typing import List
from collections import deque
from itertools import permutations, cycle


class Amplifier:
    def __init__(self, program: List[int], phase_code: int):
        self.program = program[:]
        self.inputs = [phase_code]
        self.pos = 0
        self.halted = False

    def execute(self) -> int:
        current = self.program[self.pos]
        self.opcode = current % 100

        while self.opcode != 99:
            if self.opcode in (1, 2, 7, 8):
                n_params = 3
            elif self.opcode in (5, 6):
                n_params = 2
            elif self.opcode in (3, 4):
                n_params = 1
            elif self.opcode == 9:
                n_params = 0
            else:
                raise RuntimeError(f"Unknown self.opcode {self.opcode}")

            mode1 = (current // 100) % 10
            mode2 = (current // 1000) % 10
            modified_inside = False
            # print(f"self.opcode: {self.opcode}, mode1 {mode1}, mode2 {mode2}")
            if self.opcode in (1, 2, 7, 8):
                x1 = self.program[self.pos+1] if mode1 else self.program[self.program[self.pos+1]]
                x2 = self.program[self.pos+2] if mode2 else self.program[self.program[self.pos+2]]

                if self.opcode == 1:
                    self.program[self.program[self.pos+3]] = x1 + x2
                elif self.opcode == 2:
                    self.program[self.program[self.pos+3]] = x1 * x2
                elif self.opcode == 7:
                    self.program[self.program[self.pos+3]] = 1 if x1 < x2 else 0
                elif self.opcode == 8:
                    self.program[self.program[self.pos+3]] = 1 if x1 == x2 else 0
            elif self.opcode == 3:
                x1 = self.program[self.pos+1]# if mode1 else self.program[self.program[self.pos+1]]
                # print(f"mode1 {mode1}")
                # print(f"x1 {x1}")
                # print("Adding input")
                self.program[x1] = self.inputs[0]
                self.inputs = self.inputs[1:]
            elif self.opcode == 4:
                x1 = self.program[self.pos+1] if mode1 else self.program[self.program[self.pos+1]]
                self.pos = self.pos + n_params + 1
                return x1
            elif self.opcode in (5, 6):
                x1 = self.program[self.pos+1] if mode1 else self.program[self.program[self.pos+1]]
                x2 = self.program[self.pos+2] if mode2 else self.program[self.program[self.pos+2]]

                if self.opcode == 5:
                    if x1:
                        self.pos = x2
                        modified_inside = True
                elif self.opcode == 6:
                    if not x1:
                        self.pos = x2
                        modified_inside = True
            else:
                raise RuntimeError(f"Unknow self.opcode {self.opcode}")

            if not modified_inside:
                self.pos = self.pos + n_params + 1

            current = self.program[self.pos]
            self.opcode = current % 100

        raise StopIteration("Halted!")


def run_amplifiers(program: List[int], phase_codes: List[int], first_input: int) -> int:
    for pc in phase_codes:
        amp = Amplifier(program, pc)
        amp.inputs.append(first_input)
        outputs = amp.execute()
        # print(outputs)
        first_input = outputs

    return first_input


test_program1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
assert run_amplifiers(test_program1, [4,3,2,1,0], 0) == 43210

test_program2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
assert run_amplifiers(test_program2, [0,1,2,3,4], 0) == 54321

test_program3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
assert run_amplifiers(test_program3, [1,0,4,3,2], 0) == 65210


def find_max_signal(program: List[int], phase_codes = range(5)) -> int:
    return max(
        run_amplifiers(program, phase_codes, 0) for phase_codes in permutations(phase_codes)
    )

assert find_max_signal(test_program1) == 43210
assert find_max_signal(test_program2) == 54321
assert find_max_signal(test_program3) == 65210

PROGRAM = [3,8,1001,8,10,8,105,1,0,0,21,42,55,64,77,94,175,256,337,418,99999,3,9,102,4,9,9,1001,9,5,9,102,2,9,9,101,3,9,9,4,9,99,3,9,102,2,9,9,101,5,9,9,4,9,99,3,9,1002,9,4,9,4,9,99,3,9,102,4,9,9,101,5,9,9,4,9,99,3,9,102,5,9,9,1001,9,3,9,1002,9,5,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99]


# if __name__ == "__main__":
#     print(find_max_signal(PROGRAM))


def run_amplifiers2(program: List[int], phase_codes: List[int], first_input: int) -> int:
    amplifiers = []
    for pc in phase_codes:
        amp = Amplifier(program, pc)
        amplifiers.append(amp)

    amplifiers = cycle(amplifiers)

    while True:
        amp = next(amplifiers)
        amp.inputs.append(first_input)
        try:
            output = amp.execute()
            first_input = output
        except StopIteration:
            break

    return output


test_program4 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

assert run_amplifiers2(test_program4, [9,8,7,6,5], 0) == 139629729


def find_max_signal2(program: List[int], phase_codes = range(5)) -> int:
    return max(
        run_amplifiers2(program, phase_codes, 0) for phase_codes in permutations(phase_codes)
    )


assert find_max_signal2(test_program4, phase_codes = [5,6,7,8,9]) == 139629729


if __name__ == "__main__":
    print(find_max_signal2(PROGRAM, phase_codes=[9,8,7,6,5]))
