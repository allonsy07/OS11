from typing import List
from queue import PriorityQueue
from rr import round_robin

# 프로세스 행 클래스 정의
class Process:
    def __init__(self, data: List[List]):
        self.p_id = data[0]
        self.at = data[1]
        self.bt = data[2]
        self.prt = data[3]
        self.wt = 0
        self.tt = None
        self.rt = None

        
def process_input():
    # 일단 입력은 터미널로 받습니다.
    process_list = []

    print("프로세스 개수 입력")
    process_count = int(input())

    print("프로세스 개수만큼 Arrival time, Burst time 입력 (띄어쓰기로 구분)") # 순서대로 P1, P2, ...
    for pc in range(process_count):
        process = Process()
        process.p_id = "P" + str(pc + 1) # P1, P2, P3, ...
        process.at, process.bt = list(map(int, input().split()))
        process_list.append(process)
    return process_list

def get_time_quantum():
    # time quantum도 일단 터미널로 받습니다.
    print("Time quantum 입력 (정수)")
    return int(input())



# def arrived(priority_list: List, curr_time: float, idx: int):
#     for i in priority_list:
#         if i[-1] == idx:
#             if i[1] <= curr_time:
#                 return True
#     return False


# def nonpreemptive_priority_with_rr(data: List[List], time_quantum: float):

#     # priority = []
#     idx = 0
#     curr_time = 0
#     for i in data:
#         priority.append([i["priority"], i["arrival_time"], i["burst_time"], idx])
#         idx += 1
#     sorted_priority = sorted(priority, key = lambda x: x[0], reverse = True)

#     sorting_dict = {}
#     for i in sorted_priority:
#         if i[0] in sorting_dict.keys():
#             sorting_dict[i[0]].append(i)
#         else:
#             sorting_dict[i[0]] = [i] # 2d array

    
#     while sorting_dict:
#         for val in sorting_dict:
#             if len(sorting_dict[val]) >= 2:
#                 round_robin(sorting_dict[val], time_quantum= TIME_QUANTUM)
#             else: 
#                 if arrived(sorting_dict[val], curr_time, val[-1]):
#                     curr_time += val[2]
#                     data[val[-1]]["curr_time"] = curr_time
#                     sorting_dict[val].remove(val)
#     return "Done."



def nonpreemptive_priority_with_rr(data: List[Process]):
    ganttchart = []

    process_list = []
    arrival_time_list = []

    remaining_process = {}
    ready_queue = PriorityQueue()

    for d in data:
        process = Process(d)
        process_list.append(process)

    for p in process_list:
        if p.at not in remaining_process:
            remaining_process[p.at] = [p]
            arrival_time_list.append(p.at)
        else:
            remaining_process[p.at].append(p)
        
    for a in arrival_time_list:
        remaining_process[a] = sorted(remaining_process[a], key = lambda x: x.prt, reverse = True)
    

    # start this algorithm
    time = 0
    is_running = None 
    time_quantum = data[0][4]    

    while is_running or remaining_process or not ready_queue.empty():
        if time in remaining_process:
            for p in remaining_process[time]:
                ready_queue.put((p.bt, time, p))
            del remaining_process[time]
        
        if not ready_queue.empty():
            ready_process = ready_queue.get()
            if is_running: # 우선순위를 비교해보자!
                if ready_process[2].prt == is_running.prt: # 우선순위가 같다!
                    same_priority = [is_running, ready_process[2]]
                    round_robin(same_priority, time_quantum)
                else:
                    ready_queue.put(ready_process)
            else:
                is_running = ready_process[2]
        if is_running:
            print(time, is_running.p_id, is_running.bt)
            ganttchart.append(is_running.p_id)
        else:
            print(time, "Idle")
            ganttchart.append("idle")
        if is_running:
            is_running.bt -= 1
            if is_running.bt == 0:
                is_running.tt = (time + 1) - is_running.at
                is_running = None
        for p in process_list:
            if p is not is_running and p.bt > 0 and p.at <= time:
                p.wt += 1
        time += 1

        # response time 계산, 출력값 정리
        waiting_time_list = []
        turnaround_time_list = []
        response_time_list = []

        for p in process_list:
            p.rt = ganttchart.index(p.p_id) - p.at # response time 계산
            waiting_time_list.append(p.wt)
            turnaround_time_list.append(p.tt)
            response_time_list.append(p.rt)

        average_waiting_time = sum(waiting_time_list) / len(process_list)
        average_turnaround_time = sum(turnaround_time_list) / len(process_list)
        average_response_time = sum(response_time_list) / len(process_list)


        return ganttchart, waiting_time_list, turnaround_time_list, response_time_list, average_waiting_time, average_turnaround_time, average_response_time
