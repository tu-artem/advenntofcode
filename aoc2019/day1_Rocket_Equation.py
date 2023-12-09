"""https://adventofcode.com/2019/day/1"""
from typing import List

from utils import read_input

def calculate_required_fuel(mass: int) -> int:
    return mass // 3 - 2

assert calculate_required_fuel(12) == 2
assert calculate_required_fuel(14) == 2
assert calculate_required_fuel(1969) == 654
assert calculate_required_fuel(100756) == 33583


def part1(data: List[str]) -> int:
    reqs = [calculate_required_fuel(int(mass)) for mass in data]
    return sum(reqs)


def calculate_fuel_for_fuel(mass: int) -> int:
    total_fuel = 0
    while True:
        req = calculate_required_fuel(mass)
        if req < 0:
            break
        total_fuel += req
        mass = req
    return total_fuel


def part2(data: List[str]) -> int:
    reqs = [calculate_fuel_for_fuel(int(mass)) for mass in data]
    return sum(reqs)

assert calculate_fuel_for_fuel(14) == 2
assert calculate_fuel_for_fuel(1969) == 966
assert calculate_fuel_for_fuel(100756) == 50346


if __name__ == "__main__":
    raw_data_1 = read_input(day=1, part=1)
    print("Part 1")
    print(part1(raw_data_1))
    print("Part 2")
    print(part2(raw_data_1))
