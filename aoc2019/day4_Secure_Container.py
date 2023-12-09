"""
However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 264360-746325
"""
from itertools import groupby


def validate_password(pwd: str) -> bool:

    # check inscreases
    is_sorted = sorted(pwd) == list(pwd)

    # check adjacent
    pairs = zip(pwd[:-1], pwd[1:])
    has_same = any([pair[0] == pair[1] for pair in pairs])

    return is_sorted and has_same


assert validate_password("111111")
assert validate_password("122345")
assert validate_password("111123")

assert not validate_password("223450")
assert not validate_password("123789")

def validate_part_two(pwd: str) -> bool:
    # check inscreases
    is_sorted = sorted(pwd) == list(pwd)

    # check adjacent
    has_same = False
    groups = groupby(pwd)
    for _, g in groups:
        n_elem = len(list(g))
        if n_elem == 2:
            has_same = True
            break

    return is_sorted and has_same

assert validate_part_two("112233")
assert not validate_part_two("123444")
assert validate_part_two("111122")

total = 0
for pwd in range(264360, 746325 + 1):
    total += validate_password(str(pwd))

print(f"Part 1: {total}")

total2 = 0
for pwd in range(264360, 746325 + 1):
    total2 += validate_part_two(str(pwd))

print(f"Part 2: {total2}")
