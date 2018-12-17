"""
https://adventofcode.com/2018/day/14
"""
from collections import deque

elves = [0,1]
recipes = [3, 7]


def create_recipes(elves, init_recipes, epochs=9):
    elves = elves[:]
    recipes = init_recipes[:]
    while len(recipes) < (epochs+10):
        new_recipe = sum(recipes[elf] for elf in elves)
        for ch in str(new_recipe):
            recipes.append(int(ch))

        elves = [(elf + recipes[elf] + 1) % len(recipes) for elf in elves]
    return "".join(str(x) for x in recipes[epochs:epochs+10])


assert create_recipes(elves, recipes, 9) == "5158916779"
assert create_recipes(elves, recipes, 5) == "0124515891"
assert create_recipes(elves, recipes, 18) == "9251071085"
assert create_recipes(elves, recipes, 2018) == "5941429882"


#print(create_recipes(elves, recipes, 681901))


def find_how_many(elves, recipes, score="51589"):
    elves = elves[:]
    recipes = recipes[:]
    score = deque([int(x) for x in score], maxlen=len(score))
    running_scores = deque(recipes, maxlen=len(score))
    while True:
        new_recipe = sum(recipes[elf] for elf in elves)
        
        # for ch in str(new_recipe):
        #     recipes.append(int(ch))
        #     running_scores.append(int(ch))
        a, b = divmod(new_recipe, 10)
        if a != 0:
            recipes.append(a)
            running_scores.append(a)
            if running_scores == score:
                return len(recipes) - len(score)
        recipes.append(b)
        running_scores.append(b)
        
        elves = [(elf + recipes[elf] + 1) % len(recipes) for elf in elves]
        #print(running_scores)
        if running_scores == score:
            return len(recipes) - len(score)

    
assert find_how_many(elves, recipes, score="51589") == 9
assert find_how_many(elves, recipes, score="01245") == 5
assert find_how_many(elves, recipes, score="92510") == 18
assert find_how_many(elves, recipes, score="59414") == 2018


print(find_how_many(elves, recipes, "681901"))

