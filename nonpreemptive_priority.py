from typing import List

def arrived(priority_list: List, curr_time: float, idx: int):
    for i in priority_list:
        if i[-1] == idx:
            if i[1] <= curr_time:
                return True
    return False

def nonpreemtive_priority(data: List[dict]):
    priority = []
    idx = 0
    curr_time = 0
    for i in data:
        priority.append([i["priority"], i["arrival_time"], i["burst_time"], idx])
        idx += 1
    sorted_priority = sorted(priority, ascending = False)
    while priority:
        for val in priority:
            if arrived(sorted_priority, curr_time, val[-1]):
                curr_tiem += val[2]
                data[val[-1]]["curr_time"] = curr_time
                priority.remove(val)
    return data
