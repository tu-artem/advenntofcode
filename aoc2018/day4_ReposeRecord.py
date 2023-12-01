TEST_INPUT_SORTED = """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
"""

TEST_INPUT_UNSORTED = """
[1518-11-01 00:05] falls asleep
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-02 00:50] wakes up
[1518-11-03 00:29] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-04 00:36] falls asleep
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-05 00:55] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-04 00:46] wakes up
"""

from typing import List, Tuple, Dict
import re
from datetime import datetime
from collections import Counter


rgx = "[[(0-9- :)]+]"
get_date = lambda x: datetime.strptime(re.match(rgx, x).group(), "[%Y-%m-%d %H:%M]")

def sort_rows(records: List[str]) -> List[str]:
    return sorted(records, key=get_date)


Timing = List[Tuple[int, int, int]]

def split_records(records: List[str]) -> Timing: 
    """
    Returns list of guard_id, start_sleep, end_sleep
    """
    timings = []
    rgx_id = "#([0-9]+) "
    start_rgx = ":([0-9]{2})] falls asleep"
    end_rgx = ":([0-9]{2})] wakes up"
    curr_id = 0
    curr_start = 0
    curr_end = 0
    for record in records:
        guard = re.search(rgx_id, record)
        start = re.search(start_rgx, record)
        end = re.search(end_rgx, record)
        if guard:
            curr_id = int(guard.groups()[0])
        if start:
            curr_start = int(start.groups()[0])
        if end:    
            curr_end = int(end.groups()[0])
        #if curr_start and curr_end:
            timings.append([curr_id, curr_start, curr_end])
            curr_start = 0
            curr_end = 0
    return timings


def get_durations(timings: Timing) -> Dict[int, int]: # id, duration
    durations = Counter()
    durations_by_minutes = Counter()
    for [guard_id, start, end] in timings:
        duration = end - start
        for minute in range(start, end):
            durations_by_minutes[(guard_id, minute)] += 1
        durations[guard_id] += duration
    return durations_by_minutes, durations

def find_max_sleep(durations_by_minutes, durations) -> int:
    inverse = [(value, key) for key, value in durations.items()]
    max_sleeper = max(inverse)[1]
    
    max_sleeper_minutes = [(x[0][1], x[1])  for x in durations_by_minutes.items()
                                if x[0][0] == max_sleeper]
    max_minute = max( [(value, key) for key, value in max_sleeper_minutes])[1]
    return max_minute * max_sleeper

def find_max_sleep2(durations_by_minutes, durations) -> int:
   #  inverse = [(value, key) for key, value in durations.items()]
   #  max_sleeper = max(inverse)[1]
   # print([(value, key) for key, value in durations_by_minutes.items()])
    max_minute = max([(value, key) for key, value in durations_by_minutes.items()])
   # print(max_minute)
    return max_minute[1][1] * max_minute[1][0]


assert sort_rows(TEST_INPUT_UNSORTED.strip().split("\n")) == TEST_INPUT_SORTED.strip().split("\n")

timings = split_records(sort_rows(TEST_INPUT_UNSORTED.strip().split("\n")))
assert find_max_sleep(*get_durations(timings)) == 240
assert find_max_sleep2(*get_durations(timings)) == 99 * 45

with open("day4_input1.txt", "r") as f:
    records = [line.strip() for line in f]



timings = split_records(sort_rows(records))
print(find_max_sleep(*get_durations(timings)))

print(find_max_sleep2(*get_durations(timings)) )