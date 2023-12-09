"""--- Day 11: Seating System ---
Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?"""

from typing import NamedTuple, Set, Dict, List
from itertools import product

class Seat(NamedTuple):
    x: int
    y: int


def make_seats(raw: str) -> Dict[Seat, bool]:
    seats = {}
    for x, row in enumerate(raw.split("\n")):
        for y, s in enumerate(row):
            if s == "L":
                seat = Seat(x, y)
                seats[seat] = False
            if s == "#":
                seat = Seat(x, y)
                seats[seat] = True

    return seats


def get_adjusent(seat: Seat):
    for dx, dy in product((-1, 0, 1), (-1, 0, 1)):
        if not(dx == dy == 0):
            yield Seat(seat.x + dx, seat.y + dy)


def get_occupation(seats: Dict[Seat, bool]) -> Dict[Seat, bool]:
    new_seats = {}

    for seat, occupied in seats.items():
            n_occupied = 0
            # calculate all adjusent and see if they are occupid
            for adj_seat in get_adjusent(seat):
                    if seats.get(adj_seat, False):
                        n_occupied += 1
            if not occupied and not n_occupied:
                new_seats[seat] = True
            elif occupied and n_occupied >= 4:
                new_seats[seat] = False
            else:
                new_seats[seat] = occupied

    return new_seats


def count_final_occupation(seats: Dict[Seat, bool]) -> int:
    new_seats = get_occupation(seats)

    while new_seats != seats:
        seats, new_seats = new_seats, get_occupation(new_seats)

    return sum(new_seats.values())


RAW = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


SEATS = make_seats(RAW)
assert count_final_occupation(SEATS) == 37


with open("data/11.txt") as f:
    raw = f.read()


seats = make_seats(raw)

# print("Part1:", count_final_occupation(seats))


def get_adjusent2(seat: Seat, seats: Dict[Seat, bool]):
    max_x = max(s.x for s in seats)
    max_y = max(s.y for s in seats)
    for dx, dy in product((-1, 0, 1), (-1, 0, 1)):
        if not(dx == dy == 0):
            adj_seat = Seat(seat.x + dx, seat.y + dy)
            while True:
                if adj_seat.x < 0 or adj_seat.y < 0:
                    break
                if adj_seat.x > max_x or adj_seat.y > max_y:
                    break
                if adj_seat in seats:
                    yield adj_seat
                    break
                adj_seat = Seat(adj_seat.x + dx, adj_seat.y + dy)



def get_occupation2(seats: Dict[Seat, bool]) -> Dict[Seat, bool]:
    new_seats = {}

    for seat, occupied in seats.items():
            n_occupied = 0
            # calculate all adjusent and see if they are occupid
            for adj_seat in get_adjusent2(seat, seats):
                    if seats.get(adj_seat, False):
                        n_occupied += 1
            if not occupied and not n_occupied:
                new_seats[seat] = True
            elif occupied and n_occupied >= 5:
                new_seats[seat] = False
            else:
                new_seats[seat] = occupied

    return new_seats


def count_final_occupation2(seats: Dict[Seat, bool]) -> int:
    new_seats = get_occupation2(seats)
    it = 0
    while new_seats != seats:
        it += 1
        seats, new_seats = new_seats, get_occupation2(new_seats)

    return sum(new_seats.values())


assert count_final_occupation2(SEATS) == 26


print("Part2:", count_final_occupation2(seats))
