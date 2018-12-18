from typing import Dict, Tuple, List

RAW = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

Acre = Tuple[int, int]
Area = Dict[Acre, str]

def from_raw(rows: List[str]) -> Area:
    area: Area = {}
    for y, row in enumerate(rows):
        for x, val in enumerate(row):
            area[(x, y)] = val
    return area


def plot_area(area: Area) -> str:
    x_min = min(val[0] for val in area)
    x_max = max(val[0] for val in area)
    y_min = min(val[1] for val in area)
    y_max = max(val[1] for val in area)

    p: List[str] = []

    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            p.append(area[(x, y)])
        p.append("\n")
    return "".join(p)


ROWS = RAW.split("\n")

AREA = from_raw(ROWS)

print(plot_area(AREA))


def get_neighbours(acre: Acre, area: Area) -> List[str]:
    nb: List[str] = []

    for x in range(acre[0]-1, acre[0]+2):
        for y in range(acre[1]-1, acre[1]+2):
            if (x, y) != acre and (x, y) in area:
                nb.append(area[(x,y)])
    
    

    assert len(nb) <= 8
    assert len(nb) >= 3

    return nb


def step(area: Area) -> Area:
    new_area: Area = {}

    for acre_pos, acre_val in area.items():
        nb = get_neighbours(acre_pos, area)
        if acre_val == ".":
            if nb.count("|") >= 3:
                new_area[acre_pos] = "|"
            else:
                new_area[acre_pos] = "."
        elif acre_val == "|":           
            if nb.count("#") >= 3:
                new_area[acre_pos] = "#"
            else:
                new_area[acre_pos] = "|"

        elif acre_val == "#":           
            if "#" in nb and "|" in nb:
                new_area[acre_pos] = "#"
            else:
                new_area[acre_pos] = "."
    
    return new_area
        


# for _ in range(10):
#     AREA = step(AREA)
#     print(plot_area(AREA))


# VALUES = list(AREA.values())

# assert VALUES.count("|") * VALUES.count("#") == 1147



with open("day18_input.txt") as f:
    lines = [line.strip() for line in f]

area = from_raw(lines)

print(plot_area(area))
values = list(area.values())


# when_seen = {plot_area(area):0}

# for i in range(1000):
#     area = step(area)
#     # print(plot_area(area))
#     values = list(area.values())
#     total = plot_area(area)
#     if total in when_seen:
#         break
#     else:
#         when_seen[total] = i

# values = list(area.values())

# print(values.count("|") * values.count("#"))


## Need to have 1_000_000_000 steps

# (1_000_000_000 - 455) // 28
# (1_000_000_000 - 455) // 28



for i in range(468):
    area = step(area)
    # print(plot_area(area))
 

print(plot_area(area))

values = list(area.values())


print(values.count("|") * values.count("#"))