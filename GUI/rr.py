from typing import List
from queue import Queue

# 프로세스 행 클래스 정의
class Process:
    def __init__(self):
        self.p_id = None
        self.at = None # Arrival Time
        self.bt = None # Burst Time

def round_robin(process_list: List[Process], time_quantum: int):
    # 필요한 자료구조 정의
    remaining_process = {} # 아직 큐에 들어가지 않은 프로세스를 저장하는 딕셔너리, arrive time : [프로세스, 프로세스, ...] 형태로 대응
    ready_queue = Queue() # RR 준비 큐: 큐, 프로세스 클래스가 그대로 enqueue

    for p in process_list: # remaining process에 입력된 모든 프로세스 삽입
        if p.at not in remaining_process: # 해당 arrive time에 처음 있는 프로세스일 시
            remaining_process[p.at] = [p]
        else: # 해당 arrive time을 갖는 프로세스가 이미 들어가 있을 때
            remaining_process[p.at].append(p) # pid가 빠른 프로세스가 먼저 들어갑니다.

    # 알고리즘 시작
    time = 0 # 타이머
    time_tq = 0 # Time Quantum 지났는지 확인용 타이머
    is_running = None # Idle일 경우 None, 프로세스 실행 중일 경우 실행 중인 프로세스
    tq = time_quantum # Time Quantum

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
            print(time, is_running.p_id, is_running.bt) # 시간, PID, 남은 Burst time
        else:
            print(time, 'Idle')

        # 프로세스 실행 상태 확인
        if is_running:
            is_running.bt -= 1
            if is_running.bt == 0: # burst time이 0이 되면 실행 종료
                is_running = None
                time_tq = 0
    
        # 타이머 실행
        time += 1
        if is_running:
            time_tq += 1