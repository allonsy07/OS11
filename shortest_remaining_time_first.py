from typing import List
from queue import PriorityQueue # 우선순위 큐

# 프로세스 행 클래스 정의
class Process:
    def __init__(self):
        self.p_id = None
        self.at = None # Arrival Time
        self.bt = None # Burst Time


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


def shortest_remainig_time_first(process_list: List[Process]):
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
            print(time, is_running.p_id, is_running.bt) # 시간, PID, 남은 Burst time
        else:
            print(time, 'Idle')

        # 프로세스 실행 상태 확인
        if is_running:
            is_running.bt -= 1
            if is_running.bt == 0: # burst time이 0이 되면 실행 종료
                is_running = None
        # 타이머 실행
        time += 1

shortest_remainig_time_first(process_input())