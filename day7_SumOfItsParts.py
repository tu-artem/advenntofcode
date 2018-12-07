"""
https://adventofcode.com/2018/day/7
"""


import re
from typing import NamedTuple, List, Tuple, Dict
from string import ascii_uppercase

r"""
  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
"""

TEST_CASE = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""


rgx = "Step ([A-Z]) must be finished before step ([A-Z]) can begin."

class Edge(NamedTuple):
    fr: str = None
    to: str = None
    
    @classmethod
    def from_str(self, raw: str) -> 'Edge':
        rgx_found = re.match(rgx, raw).groups()
        return Edge(*rgx_found)


edges = [Edge.from_str(x.strip()) for x in TEST_CASE.split("\n") if x]

def build_graph(edges: List[Edge], reverse=False) -> Dict[str, List[str]]:
    graph: Dict[str, List[str]] = {}
    for edge in edges:
        if not reverse:
            fr = edge.fr
            to = edge.to
        else:
            fr = edge.to
            to = edge.fr
        if fr in graph:
            graph[fr].append(to)
        else:
            graph[fr] = [to]
    return graph



def find_start_end(edges: List[Edge]) -> Tuple[List[str], List[str]]:
    fr, to = zip(*[(edge.fr, edge.to) for edge in edges])
    start = [x for x in fr if x not in to]
    end = [x for x in to if x not in fr]

    return set(start), set(end)

graph = build_graph(edges)

rev_graph =build_graph(edges, True)
start, end = find_start_end(edges)


def find_path(graph, rev_graph, start, end):
    candidates = list(start)
    
    def check_all(l1, l2):
        return all([(x in l2) for x in l1])
    
    executed = []
    while True:
        
        to_execute = min(candidates)
        
        parents = rev_graph.get(to_execute)
        executed.append(to_execute)
        if parents:
            all_parents = check_all(parents, executed)  
            if not all_parents:
                candidates.remove(to_execute)
                executed.remove(to_execute)
                continue
        
        children = graph.get(to_execute)
        if children:
            new_candidates = [x for x in children if x not in executed]
           
            candidates.extend(new_candidates)
            candidates = [x for x in candidates if x not in executed]
          
        reach_end = check_all(end, executed)
        if reach_end:
            return "".join(executed)
        


def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths


weights = {l:(ix+1) for ix, l in enumerate(ascii_uppercase)}

def weight_path(path, weights=weights):
    total_weight = sum([weights.get(vertex) for vertex in path])
    return total_weight

find_path(graph,rev_graph, start, end)

paths = find_all_paths(graph, list(start)[0], list(end)[0])

w = [weight_path(path) for path in paths]


with open("day7_input.txt") as f:
    lines = [line.strip() for line in f]

edges = [Edge.from_str(x.strip()) for x in lines]

graph = build_graph(edges)

rev_graph =build_graph(edges, True)
start, end = find_start_end(edges)

print(find_path(graph,rev_graph, start, end))


paths = []
for s in list(start):
    for e in list(end):
        p = find_all_paths(graph, s, e)
        paths.extend(p)

w = [weight_path(path) for path in paths]