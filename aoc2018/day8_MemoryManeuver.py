"""
https://adventofcode.com/2018/day/8

https://www.reddit.com/r/adventofcode/comments/a47ubw/2018_day_8_solutions/
"""


from typing import List

TEST_STR = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

"""
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A----------------------------------
    B----------- C-----------
                     D-----
"""

TEST_CASE = [int(x) for x in TEST_STR.split()]


def find_leaves(tree: List[int]) -> List[int]:
    """Leave node is a node with no children
    Returns indices of all leaves
    """
    leaves =  [ix for ix, x in enumerate(tree) if x == 0]
    return leaves


def parse(data):
    children, metas = data[:2]
    data = data[2:]
    total_sum = 0
    total_value = []

    for _ in range(children):
        sum_child, data, value = parse(data)
        total_sum += sum_child
        total_value.append(value)
       

    total_sum += sum(data[:metas])

    if children == 0:
        return sum(data[:metas]), data[metas:], sum(data[:metas])
    else: 
        return total_sum, data[metas:], sum([total_value[x-1] for x in data[:metas] if x<=len(total_value)])
parse(TEST_CASE)

# while TEST_CASE:
#     to_remove = []

#     leaves = find_leaves(TEST_CASE)[0:1]

#     for leave in leaves:
#         n_meta = TEST_CASE[leave+1]
#         start_meta = leave + 2
#         if leave != 0:
#             TEST_CASE[leave-2] -= 1
#         end_meta = start_meta + n_meta
#         sum_metadata += sum(TEST_CASE[start_meta:end_meta])
#         to_remove.extend(range(leave, end_meta))
#     TEST_CASE = [x for ix,x in enumerate(TEST_CASE) if ix not in to_remove]



"""
2 3 1 1 0 1 99 2 0 3 10 11 12 1 1 2
A----------------------------------
    C----------- B-----------
        D-----             
"""

with open("day8_input.txt", "r") as f:
    inp = f.read()

data = [int(x) for x in inp.split()]

# print(len(TEST_CASE))
# sum_metadata = 0

print(parse(data))
