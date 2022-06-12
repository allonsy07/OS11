from typing import List
from queue import Queue, PriorityQueue # 우선순위 큐
from rr import round_robin
import collections

# 프로세스 클래스 정의
class Process:
    def __init__(self, data: List[List]):
        self.p_id = data[0] # Process ID
        self.at = data[1] # Arrival Time
        self.bt = data[2] # Burst Time
        self.prt = data[3] # Priorty(Ascending)
        self.wt = 0 # Waiting time
        self.tt = None # Turnaround time
        self.rt = None # Response time

def schedulingPP(data):
    # data 는 리스트 형태로 각 항이 아래와 같음https://lavender-agenda-0e5.notion.site/Human-Object-Interaction-4e3f94908b744b828cd4fb68c67f0928
    # 0: pid, 1: 도착시간, 2: burst_time, 3: 우선순위(낮은게 우선), 4: Time quantum
    # 데이터변환
    process_data = []

    for i in range(len(data)):
        temporary = []
        process_id = data[i][0]
        arrival_time = data[i][1]
        burst_time = data[i][2]
        priority = data[i][3]
        temporary.extend([process_id, arrival_time, burst_time, burst_time,
                          priority, 0, 0, 0])  # 0: pid, 1: 도착시간, 2: burst_time, 3: 남은 burst_time, 4: 우선순위(낮은게 우선), 5:레디큐로 감, 6:start, 7:end
        process_data.append(temporary)
    # sort the data according to arrival time
    process_data.sort(key=lambda x: x[1])
    ganttchart = []  # 프로세스 실행 sequence
    time_clock = 0 #진행시간
    ready_queue = [] #레디큐
    stage = 0
    meta_data = []
    while 1:
        #if stage>10: break
        stage += 1
        #move into ready_queue
        for i in range(len(process_data)):
            if process_data[i][1] <= time_clock and process_data[i][5] != 1:
                process_data[i][5] = 1
                ready_queue.append(process_data[i])

        #priority check and sort
        if len(ready_queue)!=0:
            ready_queue.sort(key=lambda x: (x[4], x[1]), reverse=False)
            # 실행 by 1 time clock
            if ready_queue[0][2] == ready_queue[0][3]:
                ready_queue[0][6] = time_clock
            ganttchart.append(ready_queue[0][0])

            time_clock += 1
            ready_queue[0][3] -= 1
            if ready_queue[0][3] <= 0: #실행 다한 프로세스는 ready_queue에서 삭제
                ready_queue[0][7] = time_clock
                meta_data.append(ready_queue[0])
                del ready_queue[0]
        else:
            terminator = 0
            for j in range(len(process_data)):
                if process_data[j][5]!=0:
                    terminator += 1
            if terminator != len(process_data):
                ganttchart.append("idle")
                time_clock += 1
            else:
                # process 입력 순서대로
                response_time_list = []
                waiting_time_list = []
                turnaround_time_list = []
                total_turnaround_time = 0
                total_waiting_time = 0
                total_response_time= 0
                for j in range(len(data)):
                    for k in range(len(process_data)):
                        if data[j][0] == process_data[k][0]:
                            # process_data ->  0: pid, 1: 도착시간, 2: burst_time, 3: 남은 burst_time, 4: 우선순위(낮은게 우선), 5:레디큐로 감, 6:start, 7:end
                            response_time = process_data[k][6] - process_data[k][1]
                            turnaround_time = process_data[k][7] - process_data[k][1]
                            waiting_time = turnaround_time - process_data[k][2]

                            response_time_list.append(response_time)
                            waiting_time_list.append(waiting_time)
                            turnaround_time_list.append(turnaround_time)

                            total_waiting_time += waiting_time
                            total_turnaround_time += turnaround_time
                            total_response_time += response_time

                average_waiting_time = total_waiting_time / len(process_data)
                average_turnaround_time = total_turnaround_time / len(process_data)
                average_response_time = total_response_time / len(process_data)

                return ganttchart, waiting_time_list, turnaround_time_list, response_time_list, average_waiting_time, average_turnaround_time, average_response_time

def schedulingSRTF(data: List[List]):
    # 입력을 프로세스 클래스로 바꾸어서 리스트에 정리
    process_list = []
    for d in data:
        process = Process(d)
        process_list.append(process)

    # 출력값 정의
    ganttchart = []

    # 필요한 자료구조 정의
    remaining_process = {} # 아직 큐에 들어가지 않은 프로세스를 저장하는 딕셔너리, arrive time : [프로세스, 프로세스, ...] 형태로 대응
    ready_queue = PriorityQueue() # SRTF 준비 큐: 우선순위 큐, (remaining burst time, enqueued time, 프로세스 클래스) 형태로 enqueue

    for p in process_list: # remaining process에 입력된 모든 프로세스 삽입
        if p.at not in remaining_process: # 해당 arrive time에 처음 있는 프로세스일 시
            remaining_process[p.at] = [p]
        else: # 해당 arrive time을 갖는 프로세스가 이미 들어가 있을 때
            remaining_process[p.at].append(p) # pid가 빠른 프로세스가 먼저 들어갑니다.

    # 알고리즘 시작
    time = 0 # 타이머
    is_running = None # Idle일 경우 None, 프로세스 실행 중일 경우 실행 중인 프로세스

    while is_running or remaining_process or not ready_queue.empty(): # ready queue가 비어있고, 남은 프로세스가 없고, 실행 상태가 Idle이면 종료
        # ready queue에 arrived process를 enqueue
        if time in remaining_process:
            for p in remaining_process[time]:
                ready_queue.put((p.bt, time, p))
            del remaining_process[time] # enqueue된 프로세스들은 remaining process에서 제거

        # ready queue와 실행중인 프로세스의 우선순위 비교
        if not ready_queue.empty(): # ready queue가 비어있지 않으면
            ready_process = ready_queue.get() # ready queue의 가장 앞에 있는 원소를 받아옵니다. [2]번이 프로세스 클래스
            if is_running: # 프로세스가 실행중이면 우선순위를 비교 (남은 시간)
                if ready_process[2].bt < is_running.bt: # ready process의 남은 시간이 더 작을 경우 interrupt
                    ready_queue.put((is_running.bt, time, is_running))
                    is_running = ready_process[2]
                else: # 아닐 경우 다시 ready queue에 돌려놓습니다.
                    ready_queue.put(ready_process)
            else: # idle일 경우 ready process를 바로 실행
                is_running = ready_process[2]

        ## 실행 결과 print
        if is_running:
            ganttchart.append(is_running.p_id)
            # print(time, is_running.p_id, is_running.bt) # 시간, PID, 남은 Burst time
        else:
            ganttchart.append('idle')
            # print(time, 'Idle')

        # 프로세스 실행 상태 확인
        if is_running:
            is_running.bt -= 1
            if is_running.bt == 0: # burst time이 0이 되면 실행 종료
                is_running.tt = (time + 1) - is_running.at # turnaround time 기록
                is_running = None

        # waiting time 갱신
        for p in process_list:
            if p is not is_running and p.bt > 0 and p.at <= time:
                p.wt += 1

        # 타이머 실행
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

def schedulingRR(data: List[List]):
    # 입력을 프로세스 클래스로 바꾸어서 리스트에 정리
    process_list = []
    for d in data:
        process = Process(d)
        process_list.append(process)

    # 출력값 정의
    ganttchart = []

    # 필요한 자료구조 정의
    remaining_process = {} # 아직 큐에 들어가지 않은 프로세스를 저장하는 딕셔너리, arrive time : [프로세스, 프로세스, ...] 형태로 대응
    ready_queue = Queue() # SRTF 준비 큐: 우선순위 큐, (remaining burst time, enqueued time, 프로세스 클래스) 형태로 enqueue

    for p in process_list: # remaining process에 입력된 모든 프로세스 삽입
        if p.at not in remaining_process: # 해당 arrive time에 처음 있는 프로세스일 시
            remaining_process[p.at] = [p]
        else: # 해당 arrive time을 갖는 프로세스가 이미 들어가 있을 때
            remaining_process[p.at].append(p) # pid가 빠른 프로세스가 먼저 들어갑니다.

    # 알고리즘 시작
    time = 0 # 타이머
    time_tq = 0 # Time Quantum 지났는지 확인용 타이머
    is_running = None # Idle일 경우 None, 프로세스 실행 중일 경우 실행 중인 프로세스
    tq = data[0][4] # Time Quantum

    while is_running or remaining_process or not ready_queue.empty(): # ready queue가 비어있고, 남은 프로세스가 없고, 실행 상태가 Idle이면 종료
        # ready queue에 arrived process를 enqueue
        if time in remaining_process:
            for p in remaining_process[time]:
                ready_queue.put(p)
            del remaining_process[time] # enqueue된 프로세스들은 remaining process에서 제거

        if time_tq % tq == 0 or not is_running: # time quantum이 지났거나 idle이면 inturrupt
            if not ready_queue.empty(): # ready queue가 비어있지 않으면
                if is_running:
                    ready_queue.put(is_running) # 실행 중인 프로세스를 inturrupt하고 준비 큐에 삽입
                is_running = ready_queue.get() # 준비 큐 가장 앞의 프로세스를 받아옵니다.

        ## 실행 결과 print
        if is_running:
            ganttchart.append(is_running.p_id)
            # print(time, is_running.p_id, is_running.bt) # 시간, PID, 남은 Burst time
        else:
            ganttchart.append('idle')
            # print(time, 'Idle')

        # 프로세스 실행 상태 확인
        if is_running:
            is_running.bt -= 1
            if is_running.bt == 0: # burst time이 0이 되면 실행 종료
                is_running.tt = (time + 1) - is_running.at # turnaround time 기록
                is_running = None
                time_tq = 0

        # waiting time 갱신
        for p in process_list:
            if p is not is_running and p.bt > 0 and p.at <= time:
                p.wt += 1

        # 타이머 실행
        time += 1
        if is_running:
            time_tq += 1

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

def schedulingNPPwRR(data: List[Process]):

    ganttchart = []
    remaining_process = {}

    for d in data: 
        if d[1] in remaining_process.keys():
            remaining_process[d[1]].append([d[0], d[2], d[3], Process(d)])
        else:
            remaining_process[d[1]] = [[d[0], d[2], d[3], Process(d)]]
    
    for at in remaining_process.keys():
        remaining_process[at] = sorted(remaining_process[at], key= lambda x: x[2])

    time = 0
    running_process = None 
    time_quantum = data[0][4]   
    available_process = {} 

    pp_process_list = []
    while running_process or remaining_process or available_process:
        rm_list = []
        for at in remaining_process.keys():
            if time >= at:
                prc = remaining_process[at][0]
                if prc[2] in available_process.keys():
                    available_process[prc[2]].append([prc[0], prc[1], prc[3]])
                else:
                    available_process[prc[2]] = [[prc[0], prc[1], prc[3]]]
                rm_list.append(at)
            else:
                continue
        for rm_at in rm_list:
            remaining_process.pop(rm_at)

        available_process = collections.OrderedDict(sorted(available_process.items()))
        highest_priority = list(available_process.keys())[0]

        if len(available_process[highest_priority]) == 1:
            for pl in available_process[highest_priority]:
                pp_process_list.append(pl[2])
            running_process = available_process[highest_priority][0]

            burst_time = running_process[1]

            if available_process:
                for p1 in available_process:
                    for p2 in available_process[p1]:
                        p2[2].wt += time
                
            time += burst_time
            running_process[2].tt = (time + 1) - running_process[2].at

            if(running_process): 
                for _ in range(burst_time):
                    ganttchart.append(running_process[2].p_id)
            else: ganttchart.append("idle")

            running_process = None
            del available_process[highest_priority]


        elif len(available_process[highest_priority]) >= 2:
            rr_process_list = []
            for pl in available_process[highest_priority]:
                rr_process_list.append(pl[2])
        
            rr_remaining_process = {}
            rr_ready_queue = Queue()

            for p in rr_process_list:
                if p.at not in rr_remaining_process:
                    rr_remaining_process[p.at] = [p]
                else:
                    rr_remaining_process[p.at].append(p)
    
            time_tq = 0
            is_running = None
            tq = time_quantum


            while is_running or rr_remaining_process or not rr_ready_queue.empty():
                rr_remove_list = []
                for i in rr_remaining_process.keys():
                    rr_ready_queue.put(rr_remaining_process[i][0])
                    rr_remove_list.append(i)
                for r in rr_remove_list:
                    del rr_remaining_process[r]

                if time_tq % tq == 0 or not is_running:
                    if not rr_ready_queue.empty():
                        if is_running:
                            rr_ready_queue.put(is_running)
                        is_running = rr_ready_queue.get()
                
                if is_running:
                    ganttchart.append(is_running.p_id)
                else:
                    ganttchart.append('idle')
                
                if is_running:
                    is_running.bt -= 1
                    if is_running.bt == 0:
                        for idx, pl in enumerate(available_process[highest_priority]):
                            if pl[0] == is_running.p_id:
                                del available_process[highest_priority][idx]
                        is_running.tt = (time + 1) - is_running.at
                        is_running = None
                        time_tq = 0
                
                for p in rr_process_list:
                    if p is not is_running and p.bt > 0 and p.at <= time:
                        p.wt += 1
                time += 1
                if is_running:
                    time_tq += 1
            del available_process[highest_priority]

        else:
            continue

def schedulingSJF(data: List[List]):
    # 입력을 프로세스 클래스로 바꾸어서 리스트에 정리
    process_list = []
    for d in data:
        process = Process(d)
        process_list.append(process)

    # 출력값 정의
    ganttchart = []

    # 필요한 자료구조 정의
    remaining_process = {} # 아직 큐에 들어가지 않은 프로세스를 저장하는 딕셔너리, arrive time : [프로세스, 프로세스, ...] 형태로 대응
    ready_queue = PriorityQueue() # SJF 준비 큐: 우선순위 큐, (burst time, enqueued time, 프로세스 클래스) 형태로 enqueue

    for p in process_list: # remaining process에 입력된 모든 프로세스 삽입
        if p.at not in remaining_process: # 해당 arrive time에 처음 있는 프로세스일 시
            remaining_process[p.at] = [p]
        else: # 해당 arrive time을 갖는 프로세스가 이미 들어가 있을 때
            remaining_process[p.at].append(p) # pid가 빠른 프로세스가 먼저 들어갑니다.

    # 알고리즘 시작
    time = 0 # 타이머
    is_running = None # Idle일 경우 None, 프로세스 실행 중일 경우 실행 중인 프로세스

    while is_running or remaining_process or not ready_queue.empty(): # ready queue가 비어있고, 남은 프로세스가 없고, 실행 상태가 Idle이면 종료
        # ready queue에 arrived process를 enqueue
        if time in remaining_process:
            for p in remaining_process[time]:
                ready_queue.put((p.bt, time, p))
            del remaining_process[time] # enqueue된 프로세스들은 remaining process에서 제거

        # 실행 중인 프로세스가 끝나면 ready queue의 프로세스 중 가장 burst time이 짧은 프로세스를 불러옵니다.
        if not is_running:
            if not ready_queue.empty():
                is_running = ready_queue.get()[2]

        # 간트 차트 
        if is_running:
            ganttchart.append(is_running.p_id)
        else:
            ganttchart.append('idle')

        # 프로세스 실행 상태 확인
        if is_running:
            is_running.bt -= 1
            if is_running.bt == 0: # burst time이 0이 되면 실행 종료
                is_running.tt = (time + 1) - is_running.at # turnaround time 기록
                is_running = None

        # waiting time 갱신
        for p in process_list:
            if p is not is_running and p.bt > 0 and p.at <= time:
                p.wt += 1

        # 타이머 실행
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

def schedulingNPP(data):
    # data 는 리스트 형태로 각 항이 아래와 같음
    # 0: pid, 1: 도착시간, 2: burst_time, 3: 우선순위(낮은게 우선), 4: Time quantum
    # 데이터변환
    process_data = []

    for i in range(len(data)):
        temporary = []
        process_id = data[i][0]
        arrival_time = data[i][1]
        burst_time = data[i][2]
        priority = data[i][3]
        temporary.extend([process_id, arrival_time, burst_time, burst_time,
                          priority, 0, 0, 0])  # 0: pid, 1: 도착시간, 2: burst_time, 3: 남은 burst_time, 4: 우선순위(낮은게 우선), 5:레디큐로 감, 6:start, 7:end
        process_data.append(temporary)
    # sort the data according to arrival time
    process_data.sort(key=lambda x: x[1])
    ganttchart = []  # 프로세스 실행 sequence
    time_clock = 0 #진행시간
    ready_queue = [] #레디큐
    stage = 0
    meta_data = []
    while 1:
        #if stage>10: break
        stage += 1
        #move into ready_queue
        for i in range(len(process_data)):
            #print("flag", i)
            if process_data[i][1] <= time_clock and process_data[i][5] != 1:
                process_data[i][5] = 1
                ready_queue.append(process_data[i])

        #priority check and sort
        if len(ready_queue)!=0:
            if len(ganttchart) != 0 and ready_queue[0][0] == ganttchart[-1]: #간트차트 비어있지 않다 == 전에 실행된 것이 있음 + 아직 실행 중인 것이 끝나지 않음
                temp = ready_queue[1:]
                temp.sort(key=lambda x: (x[4], x[1]), reverse=False) #뒤에 들어온 것이 있다면 뒤에 것들만 정렬
                for step in range(len(ready_queue) - 1):
                    ready_queue[step + 1] = temp[step]
            else: #그렇지 않다면 앗쎄이 정리
                ready_queue.sort(key=lambda x: (x[4], x[1]), reverse=False)
            # 실행 by 1 time clock

            if ready_queue[0][2] == ready_queue[0][3]: # 처음 들어오는 것
                ready_queue[0][6] = time_clock
            ganttchart.append(ready_queue[0][0])
            time_clock += 1
            ready_queue[0][3] -= 1
            if ready_queue[0][3] <= 0: #실행 다한 프로세스는 ready_queue에서 삭제
                ready_queue[0][7] = time_clock
                meta_data.append(ready_queue[0])
                del ready_queue[0]
        else:
            terminator = 0
            for j in range(len(process_data)):
                if process_data[j][5]!=0:
                    terminator += 1
            if terminator != len(process_data):
                ganttchart.append("idle")
                time_clock += 1
            else:
                # process 입력 순서대로
                response_time_list = []
                waiting_time_list = []
                turnaround_time_list = []
                total_turnaround_time = 0
                total_waiting_time = 0
                total_response_time= 0
                for j in range(len(data)):
                    for k in range(len(process_data)):
                        if data[j][0] == process_data[k][0]:
                            # process_data ->  0: pid, 1: 도착시간, 2: burst_time, 3: 남은 burst_time, 4: 우선순위(낮은게 우선), 5:레디큐로 감, 6:start, 7:end
                            response_time = process_data[k][6] - process_data[k][1]
                            turnaround_time = process_data[k][7] - process_data[k][1]
                            waiting_time = turnaround_time - process_data[k][2]

                            response_time_list.append(response_time)
                            waiting_time_list.append(waiting_time)
                            turnaround_time_list.append(turnaround_time)

                            total_waiting_time += waiting_time
                            total_turnaround_time += turnaround_time
                            total_response_time += response_time

                average_waiting_time = total_waiting_time / len(process_data)
                average_turnaround_time = total_turnaround_time / len(process_data)
                average_response_time = total_response_time / len(process_data)

                return ganttchart, waiting_time_list, turnaround_time_list, response_time_list, average_waiting_time, average_turnaround_time, average_response_time

def schedulingFCFS(data: List[List]):

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

        if not is_running:
            if not ready_queue.empty():
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
