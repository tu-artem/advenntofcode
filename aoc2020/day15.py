"""--- Day 15: Rambunctious Recitation ---
You catch the airport shuttle and try to book a new flight to your vacation island. Due to the storm, all direct flights have been cancelled, but a route is available to get around the storm. You take it.

While you wait for your flight, you decide to check in with the Elves back at the North Pole. They're playing a memory game and are ever so excited to explain the rules!

In this game, the players take turns saying numbers. They begin by taking turns reading from a list of starting numbers (your puzzle input). Then, each turn consists of considering the most recently spoken number:

If that was the first time the number has been spoken, the current player says 0.
Otherwise, the number had been spoken before; the current player announces how many turns apart the number is from when it was previously spoken.
So, after the starting numbers, each turn results in that player speaking aloud either 0 (if the last number is new) or an age (if the last number is a repeat).

For example, suppose the starting numbers are 0,3,6:

Turn 1: The 1st number spoken is a starting number, 0.
Turn 2: The 2nd number spoken is a starting number, 3.
Turn 3: The 3rd number spoken is a starting number, 6.
Turn 4: Now, consider the last number spoken, 6. Since that was the first time the number had been spoken, the 4th number spoken is 0.
Turn 5: Next, again consider the last number spoken, 0. Since it had been spoken before, the next number to speak is the difference between the turn number when it was last spoken (the previous turn, 4) and the turn number of the time it was most recently spoken before then (turn 1). Thus, the 5th number spoken is 4 - 1, 3.
Turn 6: The last number spoken, 3 had also been spoken before, most recently on turns 5 and 2. So, the 6th number spoken is 5 - 2, 3.
Turn 7: Since 3 was just spoken twice in a row, and the last two turns are 1 turn apart, the 7th number spoken is 1.
Turn 8: Since 1 is new, the 8th number spoken is 0.
Turn 9: 0 was last spoken on turns 8 and 4, so the 9th number spoken is the difference between them, 4.
Turn 10: 4 is new, so the 10th number spoken is 0.
(The game ends when the Elves get sick of playing or dinner is ready, whichever comes first.)

Their question for you is: what will be the 2020th number spoken? In the example above, the 2020th number spoken will be 436.

Here are a few more examples:

Given the starting numbers 1,3,2, the 2020th number spoken is 1.
Given the starting numbers 2,1,3, the 2020th number spoken is 10.
Given the starting numbers 1,2,3, the 2020th number spoken is 27.
Given the starting numbers 2,3,1, the 2020th number spoken is 78.
Given the starting numbers 3,2,1, the 2020th number spoken is 438.
Given the starting numbers 3,1,2, the 2020th number spoken is 1836.
Given your starting numbers, what will be the 2020th number spoken?

Your puzzle input is 12,20,0,6,1,17,7."""

from typing import List
from collections import Counter, deque


def play_numbers(starting: List[int], end: int):
    last_time_spoken = {n: deque([t], 2) for t, n in enumerate(starting, 1)}

    turn = len(starting) + 1
    prev_spoken = starting[-1]
    while turn != (end + 1):
        if len(last_time_spoken[prev_spoken]) == 1:
            current = 0
        else:
            current = last_time_spoken[prev_spoken][-1] - last_time_spoken[prev_spoken][-2]

        if current in last_time_spoken:
            last_time_spoken[current].append(turn)
        else:
            last_time_spoken[current] = deque([turn])

        prev_spoken = current


        turn += 1
        # print(f"Turn {turn}/{end} [{turn/end:.2%}]", end="\r")
    return current


assert play_numbers([0,3,6], 2020) == 436
assert play_numbers([1,3,2], 2020) == 1
assert play_numbers([2,1,3], 2020) == 10
assert play_numbers([1,2,3], 2020) == 27
assert play_numbers([2,3,1], 2020) == 78


# print("Part1:", play_numbers([12,20,0,6,1,17,7], 2020))


print("Part2:", play_numbers([12,20,0,6,1,17,7], 30000000))
