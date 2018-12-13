
from typing import Tuple, List, Dict
from itertools import cycle
from collections import Counter

RAW= r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """

RAW2 = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
"""

lines = [line for line in RAW2.split("\n") if line]


paths = {
    "/":"/",
    "\\":"\\",
    "|":"|",
    "-":"-",
    "^":"|",
    "v":"|",
    ">":"-",
    "<":"-",
    "+":"+"
}


class Cart:
    def __init__(self,
                cart_id: int, 
                position: Tuple[int, int],
                direction: str):
        
        self.cart_id = cart_id
        self.x, self.y = position
        self.direction = direction
        self.cross = cycle(["left", "straingh", "right"])

    def __repr__(self):
        return f"(Cart) {self.cart_id} at {self.x, self.y} moving {self.direction}"

    def on_cross(self):
        return next(self.cross)

    def position(self):
        return self.x, self.y


def create_grid_and_carts(lines: List[str]):
    grid = {}
    init_id = 0
    carts = []
    for y, line in enumerate(lines):
        for x, row in enumerate(line):
            if row == ">":
                carts.append(Cart(init_id, (x,y), "right"))
                init_id += 1
            elif row == "<":
                carts.append(Cart(init_id, (x,y), "left"))
                init_id += 1
            elif row == "^":
                carts.append(Cart(init_id, (x,y), "up"))
                init_id += 1
            elif row == "v":
                carts.append(Cart(init_id, (x,y), "down")) 
                init_id += 1
            grid[x, y] = paths.get(row)
    
    return grid, carts

grid, carts = create_grid_and_carts(lines)

def tick(carts: List[Cart], grid: Dict[Tuple[int, int], str]) -> List[Cart]:
    for cart in carts:
        
        if cart.direction == "right":
            cart.x += 1
        elif cart.direction == "left":
            cart.x += -1
        elif cart.direction == "up":
            cart.y += -1
        elif cart.direction == "down":
            cart.y += 1

        current_position = (cart.x, cart.y)
        track = grid.get(current_position)
        if track == "+":
            turn = cart.on_cross()
            if cart.direction == "right":
                if turn == "left":
                    cart.direction = "up"
                elif turn == "right":
                    cart.direction = "down"
            elif cart.direction == "left":
                if turn == "left":
                    cart.direction = "down"
                elif turn == "right":
                    cart.direction = "up"
            elif cart.direction == "up":
                if turn == "left":
                    cart.direction = "left"
                elif turn == "right":
                    cart.direction = "right"
            elif cart.direction == "down":
                if turn == "left":
                    cart.direction = "right"
                elif turn == "right":
                    cart.direction = "left"
        else:
            if cart.direction == "right":
                if track == "\\":
                    cart.direction = "down"
                elif track == "/":
                    cart.direction = "up"
            elif cart.direction == "left":
                if track == "\\":
                    cart.direction = "up"
                elif track == "/":
                    cart.direction = "down"
            elif cart.direction == "up":
                if track == "\\":
                    cart.direction = "left"
                elif track == "/":
                    cart.direction = "right"
            elif cart.direction == "down":
                if track == "\\":
                    cart.direction = "right"
                elif track == "/":
                    cart.direction = "left"

    return carts

def move(carts, grid):
            
    carts = tick(carts, grid)
    tick(carts, grid)

    while True:
        carts = tick(carts, grid)
        positions = Counter((cart.x, cart.y) for cart in carts)
        if positions.most_common(1)[0][1] > 1:
            break

    return positions

# move(carts, grid)

with open("day13_input.txt") as f:
    LINES = f.readlines()



def find_last(carts, grid):
    ticks = 0
    
    while len(carts) > 1:
        carts = tick(carts, grid)
        ticks += 1
        positions = Counter((cart.x, cart.y) for cart in carts)
        #if positions.most_common(1)[0][1] > 1:
        accidents = set([pos for (pos, count) in positions.most_common() if count > 1])
        if accidents:
            print(accidents)
        carts = [cart for cart in carts if cart.position() not in accidents]
      #  print(len(carts))
   
    return carts


# print(find_last(carts, grid))


GRID, CARTS = create_grid_and_carts(LINES)


# find_last(CARTS, GRID)