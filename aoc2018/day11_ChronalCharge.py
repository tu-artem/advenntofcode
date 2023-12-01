"""
https://adventofcode.com/2018/day/11
"""

from typing import Dict, Tuple

def find_cell_power_level(x: int, y: int, grid_sn: int) -> int:
    rack_id = x + 10
    begin = rack_id * y
    increase = begin + grid_sn
    power_level = increase * rack_id
    hundreds = power_level % 1000 // 100
    substract = hundreds - 5
    return substract


assert find_cell_power_level(122, 79, 57) == -5
assert find_cell_power_level(217, 196, 39) == 0
assert find_cell_power_level(101, 153, 71) == 4


def create_grid(sn: int):
    grid: Dict[Tuple[int,int], int] = {}

    for y in range(1, 301):
        for x in range(1, 301):
            grid[(x, y)] = find_cell_power_level(x, y, sn)

    return grid

def where_max_power(grid, window_size=3):
    max_power = float("-Inf")
    cell = ()
    for y in range(1, 301-window_size+1):
        for x in range(1, 301-window_size+1):
            power = sum([grid[(n,m)] for n in range(x, x+window_size) 
                                     for m in range (y, y+window_size)])
            
            if power > max_power:
                max_power = power
                cell = (x,y)
    
    return max_power, cell



def where_max_power_full_scan(grid, start: Tuple[int,int]):
    x, y = start
    prev_sum = grid[start]
    max_power = prev_sum
    size = 1
    max_steps_avaliable = min(300-x, 300-y)
    #max_steps_avaliable = 16
   # print(max_steps_avaliable)
    for step in range(1, max_steps_avaliable):
            
            power = sum([grid[(n, y+step)] 
                         for n in range(x, x+step)]) + \
                    sum([grid[(x+step, m)] 
                         for m in range(y, y+step)]) + \
                         grid[x+step, y+step]
            
            prev_sum += power
          #   print(step, (x+step, y+step))
          #   print(prev_sum)
            if prev_sum > max_power:
                max_power = prev_sum
                size = step + 1
    return max_power, size


grid = create_grid(18)

assert where_max_power_full_scan(grid, (90,269)) == (113, 16)



grid = create_grid(42)

assert where_max_power_full_scan(grid, (232,251)) == (119, 12)


grid = create_grid(7857)
max_pows = {}

size = 0
for x in range(1, 301):
    for y in range(1, 301):
        curr_pow, curr_size = where_max_power_full_scan(grid, (x,y))
        max_pows[(x, y)] = (curr_pow, curr_size)
    print(f"x is:{x}")