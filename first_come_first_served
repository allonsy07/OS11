from queue import Queue
from typing import list

class Process:
    def __init__(self, data: List[List]):
        self.p_id = data[0]
        self.at = data[1]
        self.bt = data[2]
        self.prt = data[3]
        self.wt = 0
        self.tt = None
        self.rt = None

def scheduleFCFS(data: List[List]):

    process_list = []
    for d in data:
        process = Process(d)
        process_list.append(process)

        ganttchart = []

        remaining_process = {}
        ready_queue = Queue()

        for p in process_list:
            if p.at not in remaining_process:
                remaining_process[p.at] = [p]
            else:
                remaining_process[p.at].append(p)

        time = 0
        is_running = None

        while is_running or remaining_process or not ready_queue.empty():
            if time in remaining_process:
                for p in remaining_process[time]:
                    ready_queue.put(p)
                del remaining_process[time]

            if not is_running
                is_running = ready_queue.get()

            if is_running:
                ganttchart.append(is_running.p_id)
            else:
                ganttchart.append('idle')

            if is_running:
                is_running.bt -= 1
                if is_running.bt == 0:
                    is_running.tt = (time + 1) - is_running.at
                    is_running = None

            for p in process_list:
                if p is not is_running and p.bt > 0 and p.at <= time:
                    p.wt += 1

            time += 1

    waiting_time_list = []
    turnaround_time_list = []
    response_time_list = []

    for p in process_list:
        p.rt = ganttchart.index(p.p_id) - p.at
        waiting_time_list.append(p.wt)
        turnaround_time_list.append(p.tt)
        response_time_list.append(p.rt)

    average_waiting_time = sum(waiting_time_list) / len(process_list)
    average_turnaround_time = sum(turnaround_time_list) / len(process_list)
    average_response_time = sum(response_time_list) / len(process_list)

    return ganttchart, waiting_time_list, turnaround_time_list, response_time_list, average_waiting_time, average_turnaround_time, average_response_time
