RAW = """#######  
#.G...#  
#...EG#  
#.#.#G#  
#..G#E#  
#.....#  
#######"""

grid = {}

for y, line in enumerate(RAW.split()):
    for x, s in enumerate(line):
        grid[x,y] = s


