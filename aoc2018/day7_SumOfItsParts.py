"""
https://adventofcode.com/2018/day/7
"""


import re
from typing import NamedTuple, List, Tuple, Dict

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
    
    @staticmethod
    def from_str(raw: str) -> 'Edge':
        rgx_found = re.match(rgx, raw).groups()
        return Edge(*rgx_found)



def dependencies(edges: List[Edge]) -> Dict[str, List[str]]:
    
    graph: Dict[str, List[str]] = {node:[] for nodes in edges for node in nodes}
    
    for edge in edges:
       graph[edge.to].append(edge.fr)
    return graph



def find_start_end(edges: List[Edge]) -> Tuple[List[str], List[str]]:
    fr, to = zip(*[(edge.fr, edge.to) for edge in edges])
    start = [x for x in fr if x not in to]
    end = [x for x in to if x not in fr]

    return set(start), set(end)


edges = [Edge.from_str(x.strip()) for x in TEST_CASE.split("\n") if x]

class Factory:
    def __init__(self, edges):
        self.dependencies = dependencies(edges)
        
        self.executed = []
        self.locked_jobs = []
    
    def finish_job(self, job: str):
        self.executed.append(job)

        for dependency in self.dependencies.values():
            if job in dependency:
                dependency.remove(job)
            

    def lock_job(self, job):
        self.locked_jobs.append(job)

    def avaliable_jobs(self):
        return [k for k,v in self.dependencies.items() 
                if not v and 
                 k not in self.locked_jobs and
                 k not in self.executed]


def get_job_duration(job, base=60):
    return ord(job) - ord("A") + 1 + base


class Worker:
    def __init__(self, id):
        self.id = id
        self.job = None
        self.elapsed_time = 0
        self.weight = 0
        self.busy = False

    def take_job(self, job, start):
        self.job = job
        self.weight = get_job_duration(job, base=60)
        self.elapsed_time = start + self.weight
        self.busy = True

    def finish_job(self):
        self.busy = False
        job = self.job
        self.job = None
        return job
    
    def finished(self):
        return self.elapsed_time >= self.weight







with open("day7_input.txt") as f:
    lines = [line.strip() for line in f]

edges = [Edge.from_str(x.strip()) for x in lines]



factory = Factory(edges)

workers = [Worker(x) for x in range(5)]

curr_time = 0
while factory.avaliable_jobs() or any([worker.busy for worker in workers]):

    #print(factory.candidates)

    for worker in workers:
        
        if worker.busy and worker.elapsed_time <= curr_time:
            finished = worker.finish_job()
            factory.finish_job(finished)

    for worker in workers:    
        av_job = factory.avaliable_jobs()
        if not worker.busy:
            if av_job:
                worker.take_job(min(av_job), curr_time)
             #   worker.elapsed_time = curr_time + worker.weight 
                factory.lock_job(min(av_job))
        
    if any(worker.busy for worker in workers):
        curr_time = min([worker.elapsed_time for worker in workers if worker.busy])
    
    #if curr_time > 20:
    print(curr_time, [(worker.id, worker.job) for worker in workers])
    #    break
print(curr_time)

