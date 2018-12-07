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



def find_path(graph, rev_graph, start, end):
    candidates = list(start)
    
    def check_all(l1, l2):
        if not l1: return True
        return all([(x in l2) for x in l1])
    executed = []
    

    while True:
        candidates = [candidate for candidate in candidates if check_all(rev_graph.get(candidate), executed)]
        # for candidate in candidates:    
        #     parents = rev_graph.get(candidate)
        #     if parents:
        #         all_parents = check_all(parents, executed)  
        #         if not all_parents:
        #             candidates.remove(candidate)


        to_execute = min(candidates)
        
        executed.append(to_execute)
        
        children = graph.get(to_execute)
        if children:
            new_candidates = [x for x in children if x not in executed]
           
            candidates.extend(new_candidates)
            candidates = [candidate for candidate in candidates if candidate != to_execute]
          
        reach_end = check_all(end, executed)
        if reach_end:
            return "".join(executed)



edges = [Edge.from_str(x.strip()) for x in TEST_CASE.split("\n") if x]
graph = build_graph(edges)
rev_graph =build_graph(edges, True)
start, end = find_start_end(edges)
find_path(graph,rev_graph, start, end)


# with open("day7_input.txt") as f:
#     lines = [line.strip() for line in f]

# edges = [Edge.from_str(x.strip()) for x in lines]

# graph = build_graph(edges)

# rev_graph =build_graph(edges, True)
# start, end = find_start_end(edges)

# print(find_path(graph,rev_graph, start, end))


class Worker:
    def __init__(self, id):
        self.id = id
        self.job = None
        self.elapsed_time = -2
        self.weight = 0
        self.busy = False

    def take_job(self, job):
        self.job = job
        self.elapsed_time = 0
        self.weight = weights[job]
        self.busy = True

    def finish_job(self):
        self.busy = False
        self.elapsed_time = -2
        job = self.job
        self.job = None
        return job
    
    def finished(self):
        return self.elapsed_time >= self.weight




class Factory:
    def __init__(self, graph, rev_graph, start, end):
        self.graph = graph
        self.rev_graph = rev_graph
        # self.start = start
        self.end = end
        self.executed = []
        self.candidates = list(start)
        self.locked_jobs = []
    
    def finish_job(self, job: str):
        self.executed.append(job)

        children = graph.get(job)
        if children:
            new_candidates = [x for x in children if x not in self.executed]
            
            self.candidates.extend(new_candidates)
        self.candidates = [candidate for candidate in self.candidates 
                                     if candidate != job and 
                                     self.check_all(rev_graph.get(candidate), self.executed)]

    def check_all(self, l1, l2):
        if not l1: return True
        return all([(x in l2) for x in l1])

    def lock_job(self, job):
        self.locked_jobs.append(job)

    def avaliable_jobs(self):
        return [candidate for candidate in self.candidates if candidate not in self.locked_jobs]


# with open("day7_input.txt") as f:
#     lines = [line.strip() for line in f]

# edges = [Edge.from_str(x.strip()) for x in lines]

# graph = build_graph(edges)

# rev_graph =build_graph(edges, True)
# start, end = find_start_end(edges)


factory = Factory(graph,rev_graph, start, end)

workers = [Worker(x) for x in range(2)]
weights = {l:(ix+1) for ix, l in enumerate(ascii_uppercase)}
curr_time = 0 
while factory.candidates:
    print(factory.candidates)
    #print(factory.candidates)
    for worker in workers:

        av_job = factory.avaliable_jobs()
        if worker.busy:
            worker.elapsed_time += 1
        if worker.finished():
            finished = worker.finish_job()
            factory.finish_job(finished)
            av_job = factory.avaliable_jobs()
        if not av_job:
            continue
        
        if not worker.busy:
            worker.take_job(min(av_job))
            factory.lock_job(min(av_job))
        
        
    print(curr_time, [(worker.id, worker.job) for worker in workers])
        #print(worker.id, worker.job)
    
    curr_time += 1
    #if curr_time > 20:
    #    break
print(curr_time)
# while curr_time < 10:
#     can_execute = start

