"""--- Day 13: Shuttle Search ---
Your ferry can make it safely to a nearby port, but it won't get much further. When you call to book another ship, you discover that no ships embark from that port to your vacation island. You'll need to get from the port to the nearest airport.

Fortunately, a shuttle bus service is available to bring you from the sea port to the airport! Each bus has an ID number that also indicates how often the bus leaves for the airport.

Bus schedules are defined based on a timestamp that measures the number of minutes since some fixed reference point in the past. At timestamp 0, every bus simultaneously departed from the sea port. After that, each bus travels to the airport, then various other locations, and finally returns to the sea port to repeat its journey forever.

The time this loop takes a particular bus is also its ID number: the bus with ID 5 departs from the sea port at timestamps 0, 5, 10, 15, and so on. The bus with ID 11 departs at 0, 11, 22, 33, and so on. If you are there when the bus departs, you can ride that bus to the airport!

Your notes (your puzzle input) consist of two lines. The first line is your estimate of the earliest timestamp you could depart on a bus. The second line lists the bus IDs that are in service according to the shuttle company; entries that show x must be out of service, so you decide to ignore them.

To save time once you arrive, your goal is to figure out the earliest bus you can take to the airport. (There will be exactly one such bus.)

For example, suppose you have the following notes:

939
7,13,x,x,59,x,31,19
Here, the earliest timestamp you could depart is 939, and the bus IDs in service are 7, 13, 59, 31, and 19. Near timestamp 939, these bus IDs depart at the times marked D:

time   bus 7   bus 13  bus 59  bus 31  bus 19
929      .       .       .       .       .
930      .       .       .       D       .
931      D       .       .       .       D
932      .       .       .       .       .
933      .       .       .       .       .
934      .       .       .       .       .
935      .       .       .       .       .
936      .       D       .       .       .
937      .       .       .       .       .
938      D       .       .       .       .
939      .       .       .       .       .
940      .       .       .       .       .
941      .       .       .       .       .
942      .       .       .       .       .
943      .       .       .       .       .
944      .       .       D       .       .
945      D       .       .       .       .
946      .       .       .       .       .
947      .       .       .       .       .
948      .       .       .       .       .
949      .       D       .       .       .
The earliest bus you could take is bus ID 59. It doesn't depart until timestamp 944, so you would need to wait 944 - 939 = 5 minutes before it departs. Multiplying the bus ID by the number of minutes you'd need to wait gives 295.

What is the ID of the earliest bus you can take to the airport multiplied by the number of minutes you'll need to wait for that bus?"""

from typing import List, Tuple
from operator import itemgetter
from functools import reduce
from operator import mul

EARLIEST = 939
RAW = "7,13,x,x,59,x,31,19"

def make_shuttles(raw: str) -> List[int]:
    return [int(x) for x in raw.split(",") if x != 'x']


def find_shuttle(earliest: int, shuttles: List[int]) -> Tuple[int, int]:
    prev_departure = [earliest // s * s for s in shuttles]
    time_till_next = [(s, p + s - earliest) for p, s in zip(prev_departure, shuttles)]

    return sorted(time_till_next, key=itemgetter(1))[0]



SHULLTES = make_shuttles(RAW)


SHUTTLE = find_shuttle(EARLIEST, SHULLTES)

assert SHUTTLE[0] * SHUTTLE[1] == 59 * 5


earliest = 1009310
raw = "19,x,x,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,599,x,29,x,x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,x,x,x,x,23,x,x,x,x,x,x,x,761,x,x,x,x,x,x,x,x,x,41,x,x,13"

shuttles = make_shuttles(raw)

shuttle = find_shuttle(earliest, shuttles)

print("Part1:", shuttle[0] * shuttle[1])


# PART 2

def make_shuttles2(raw: str) -> List[Tuple[int, int]]:
    return [(int(x), i) for i, x in enumerate(raw.split(",")) if x != 'x']


def check_timestamp(ts, shuttles):
    return [(ts + a) % d == 0 for d, a in shuttles]



def find_departure_time(shuttles: List[Tuple[int, int]]) -> int:
    delta = shuttles[0][0]
    ts = 0
    n = 0
    while True:
        n+= 1
        res = check_timestamp(ts, shuttles)
        if all(res):
            return ts
        else:
            matched = [s[0] for s, r in zip(shuttles, res) if r]
            delta = reduce(mul, matched, 1)

        ts += delta


assert find_departure_time(make_shuttles2("7,13,x,x,59,x,31,19")) == 1068781
assert find_departure_time(make_shuttles2("17,x,13,19")) == 3417
assert find_departure_time(make_shuttles2("67,7,59,61")) == 754018
assert find_departure_time(make_shuttles2("67,x,7,59,61")) == 779210
assert find_departure_time(make_shuttles2("67,7,x,59,61")) == 1261476
assert find_departure_time(make_shuttles2("1789,37,47,1889")) == 1202161486


shuttles2 = make_shuttles2(raw)
print("Part2:", find_departure_time(shuttles2))
