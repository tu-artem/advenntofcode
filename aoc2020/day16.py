"""--- Day 16: Ticket Translation ---
As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed trip coming up is on a high-speed train. However, the train ticket you were given is in a language you don't understand. You should probably figure out what it says before you get to the train station after the next flight.

Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and so you figure out the fields these tickets must have and the valid ranges for values in those fields.

You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby tickets for the same train service (via the airport security cameras) together into a single document you can reference (your puzzle input).

The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields in every ticket is named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is not).

Each ticket is represented by a single line of comma-separated values. The values are the numbers on the ticket in the order they appear; every ticket has the same format. For example, consider this ticket:

.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'
Here, ? represents text in a language you don't understand. This ticket might be represented as 101,102,103,104,301,302,303,401,402,403; of course, the actual train tickets you're looking at are much more complicated. In any case, you've extracted just the numbers in such a way that the first number is always the same specific field, the second number is always a different specific field, and so on - you just don't know what each position actually means!

Start by determining which tickets are completely invalid; these are tickets that contain values which aren't valid for any field. Ignore your ticket for now.

For example, suppose you have the following notes:

class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only whether tickets contain values that are not valid for any field. In this example, the values on the first nearby ticket are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.

Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?"""


from typing import List, Tuple, Dict
from itertools import chain
from collections import defaultdict

Ticket = List[int]
Rule = Tuple[int, int]

def make_rule(line: str) -> Tuple[str, List[Rule]]:
    name, bounds = line.split(": ")

    bounds = [tuple(map(int, b.split("-"))) for b in bounds.split(" or ")]

    return name, bounds


def parse_raw(raw: str) -> Tuple[Ticket, List[Ticket], Dict[str, List[Rule]]]:
    raw_rules, raw_my_ticket, raw_tickets = raw.strip().split("\n\n")

    my_ticket = [int(value) for value in raw_my_ticket.split("\n")[1].split(",")]

    tickets = [[int(value) for value in row.split(",")] for row in raw_tickets.split("\n")[1:]]

    rules = dict(make_rule(line) for line in raw_rules.split("\n"))

    return my_ticket, tickets, rules


RAW = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""


MY_TICKET, TICKETS, RULES = parse_raw(RAW)


def validate(rules: Dict[str, List[Rule]], ticket: Ticket) -> int:
    # Returns number of not valid values opn ticket
    valid = {}

    for value in ticket:
        valid[value] = False
        for lo, hi in chain.from_iterable(rules.values()):
            if lo <= value <= hi:
                valid[value] = True

    return sum(value for value, is_valid in valid.items() if not is_valid)


assert sum(validate(RULES, T) for T in TICKETS) == 71


with open("data/16.txt") as f:
    raw = f.read().strip()



my_ticket, tickets, rules = parse_raw(raw)

print("Part1: ", sum(validate(rules, t) for t in tickets))


valid_tickets = [t for t in tickets if validate(rules, t) == 0]


def validate2(rule: List[Rule], tickets: List[Ticket], position: int) -> bool:
    values = [t[position] for t in tickets]


    def is_valid(rule: List[Rule], val):
        return any(lo <= val <= hi for lo, hi in rule)

    return all(is_valid(rule, val) for val in values)


VALID_TICKETS = [t for t in TICKETS if validate(RULES, t) == 0]


def find_fields_positions(rules, valid_tickets) -> Dict[str, int]:
    candidate_positions = {}
    actual_positions = {}

    for rule_name, rule in rules.items():
        valid_position = []
        for pos in range(len(valid_tickets[0])):
            is_valid = validate2(rule, valid_tickets, pos)
            if is_valid:
                valid_position.append(pos)
        candidate_positions[rule_name] = valid_position



    for key in sorted(candidate_positions, key=lambda x: len(candidate_positions[x])):
        if len(candidate_positions[key]) == 1:
            current = candidate_positions[key][0]
            actual_positions[key] = current
            for positions in candidate_positions.values():
                if current in positions:
                    positions.remove(current)

    return actual_positions


valid_tickets = [t for t in tickets if validate(rules, t) == 0]

positions = find_fields_positions(rules, valid_tickets)


def solve2(ticket, positions) -> int:
    start = 1
    for name, p in positions.items():
        if name.startswith("departure"):
            start *= ticket[p]
    return start



print("Part2:", solve2(my_ticket, positions))
