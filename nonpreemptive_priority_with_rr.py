from typing import List

from .round_robin import round_robin
from nonpreemptive_priority import nonpreemtive_priority

TIME_QUANTUM = 2

def arrived(priority_list: List, curr_time: float, idx: int):
    for i in priority_list:
        if i[-1] == idx:
            if i[1] <= curr_time:
                return True
    return False

def nonpreemptive_priority_with_rr(data: List[dict], time_quantum: float):
    priority = []
    idx = 0
    curr_time = 0
    for i in data:
        priority.append([i["priority"], i["arrival_time"], i["burst_time"], idx])
        idx += 1
    sorted_priority = sorted(priority, key = lambda x: x[0], reverse = True)

    sorting_dict = {}
    for i in sorted_priority:
        if i[0] in sorting_dict.keys():
            sorting_dict[i[0]].append(i)
        else:
            sorting_dict[i[0]] = [i] # 2d array

    
    while sorting_dict:
        for val in sorting_dict:
            if len(sorting_dict[val]) >= 2:
                round_robin(sorting_dict[val], time_quantum= TIME_QUANTUM)
            else: 
                if arrived(sorting_dict[val], curr_time, val[-1]):
                    curr_time += val[2]
                    data[val[-1]]["curr_time"] = curr_time
                    sorting_dict[val].remove(val)
    return "Done."