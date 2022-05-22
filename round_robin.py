from typing import List

def round_robin(data: List[dict], time_quantum: float):
    rr_list = []
    idx = 0
    curr_time = 0
    flag = True

    for d in data:
        rr_list.append([d["arrival_time"], d["burst_time"], idx])
        idx+=1
    while flag:
        for i in range(len(rr_list)):
            burst_time = rr_list[i][1]
            arrival_time = rr_list[i][0]
            if burst_time != 0 and arrival_time < curr_time or curr_time == 0:
                if burst_time > time_quantum:
                    rr_list[i][1] -= time_quantum
                    curr_time += time_quantum
                else:
                    rr_list[i][1] = 0
                    curr_time += burst_time
                    data[rr_list[i][2]]['curr_time'] = curr_time
        flg = True
        for i in rr_list:
            if not i[1] == 0:
                flg = False
        if flg:
            flag = False
    return data
