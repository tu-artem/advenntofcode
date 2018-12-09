"""
https://adventofcode.com/2018/day/9
"""

from itertools import cycle
from collections import Counter, deque
from typing import Tuple

n_players = 9
n_marbles = 25

def play_marbles(n_players: int, n_marbles: int) -> int:
    marbles = deque([0])
    players = cycle(range(1, n_players+1))
    scores = Counter()
    for marble in range(1, n_marbles+1):
        curr_player = next(players)
        if marble % 23 == 0:
            scores[curr_player] += marble 

            marbles.rotate(7)
            scores[curr_player] += marbles.popleft()
           # marbles.remove(marbles[del_index])
        
        else:       
            marbles.rotate(-2)
            marbles.appendleft(marble)
    return scores.most_common(1)[0][1]


play_marbles(9,25)

"""
10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
"""

assert play_marbles(10, 1618) == 8317
assert play_marbles(13, 7999) == 146373
assert play_marbles(17, 1104) == 2764
assert play_marbles(21, 6111) == 54718
assert play_marbles(30, 5807) == 37305


"405 players; last marble is worth 70953 points"

print(play_marbles(405,70953))
print(play_marbles(405,70953*100))