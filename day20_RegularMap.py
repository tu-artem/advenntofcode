import re
from collections import defaultdict

# TEST_STR = "WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))"
TEST_STR = "N(E|W)N"



def find_max_path(input: str) -> int:
    d = {
        "N": (0, 1),
        "S": (0, -1),
        "W": (-1, 0),
        "E": (1, 0)
    }

    distances = defaultdict(int)

    to_check = []

    px, py = x, y = 0, 0

    for current in input:
        
        if current == "(":
            to_check.append((x,y))
        elif current == "|":
            x, y = to_check[-1]
        elif current == ")":
            x, y = to_check.pop()
        else:
            dx, dy = d.get(current)
            x += dx
            y += dy
            distances[(x,y)] = min(distances[(x, y)], distances[(px, py)]) if distances[(x, y)] else distances[(px, py)] + 1
        px, py = x, y
    return max(distances.values())
    

assert find_max_path(TEST_STR) == 31
# assert find_max_path("WNE") == 3
# assert find_max_path("ENWWW(NEEE|SSE(EE|N))") == 10

# assert find_max_path("ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN") == 18



# def paths_with_n_doors(input: str, n_doors: int = 1000) -> int:
#     d = {
#         "N": (0, 1),
#         "S": (0, -1),
#         "W": (-1, 0),
#         "E": (1, 0)
#     }

#     distances = defaultdict(int)

#     to_check = []

#     px, py = x, y = 0, 0

#     for current in input:
        
#         if current == "(":
#             to_check.append((x,y))
#         elif current == "|":
#             x, y = to_check[-1]
#         elif current == ")":
#             x, y = to_check.pop()
#         else:
#             dx, dy = d.get(current)
#             x += dx
#             y += dy
#             distances[(x,y)] = min(distances[(x, y)], distances[(px, py)]) if distances[(x, y)] else distances[(px, py)] + 1
#         px, py = x, y
#     return len([x for x in distances.values() if x >=1000])
    



with open("day20_input.txt") as f:
    raw = f.read()



print(find_max_path(raw[1:-1]))

print(paths_with_n_doors(raw[1:-1], n_doors=1000))