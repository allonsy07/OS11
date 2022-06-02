from typing import List
from queue import Queue, PriorityQueue # 우선순위 큐

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