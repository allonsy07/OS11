# SRTF + RR Code Description

### 공통 클래스 : Process 클래스
> #### 클래스 변수
p_id : Process ID   
at : Arrival time  
bt : Burst time  
prt : Priority (작을수록 높음)  
wt : Waiting time  
tt : Turnaround time  
rt : Response time  

***
### 공통 자료구조

> remaining_process : dictionary (딕셔너리)  

arrival time이 되면 ready queue 에 들어갈 수 있도록 {arrive_time: [프로세스, 프로세스, ...]} 의 형태로 저장합니다.

***
### 공통 변수

> time : int 

타이머 변수로 0에서 시작해 알고리즘 반복문이 실행될 때마다 1씩 증가합니다.

> is_running : 프로세스 변수

None 으로 초기화하여 실행 중인 프로세스를 저장합니다. Idle 상태일 경우 None 값을 가집니다.
***
### SRTF
> Ready Queue : Priority Queue (우선순위 큐)

Queue 모듈의 PriorityQueue 자료구조를 사용해서 SRTF의 남은 burst time이 가장 짧은 프로세스가 제일 우선순위가 높은 특성을 구현했습니다.
Priority Queue에 (remaining burst time, enqueued time, 프로세스 클래스)의 튜플 형태로 삽입하여 남은 burst time이 같은 경우 enqueued time이 빠른 프로세스가 먼저 나오도록 구현했습니다.

> 알고리즘 핵심 코드
```python
        # ready queue와 실행중인 프로세스의 우선순위 비교
        if not ready_queue.empty(): # ready queue가 비어있지 않으면
            ready_process = ready_queue.get() # ready queue의 가장 앞에 있는 원소를 받아옵니다. [2]번이 프로세스 클래스
            if is_running: # 프로세스가 실행중이면 우선순위를 비교 (남은 시간)
                if ready_process[2].bt < is_running.bt: # ready process의 남은 시간이 더 작을 경우 interrupt
                    ready_queue.put((is_running.bt, time, is_running))
                    is_running = ready_process[2] # 프로세스 클래스
                else: # 아닐 경우 다시 ready queue에 돌려놓습니다.
                    ready_queue.put(ready_process)
            else: # idle일 경우 ready process를 바로 실행
                is_running = ready_process[2]
```
***
```python
        if not ready_queue.empty(): # ready queue가 비어있지 않으면
            ready_process = ready_queue.get() # ready queue의 가장 앞에 있는 원소를 받아옵니다. [2]번이 프로세스 클래스
```
ready queue가 비어있으면 우선순위를 비교할 수 없으므로 ready queue가 비어있는 경우에 알고리즘을 실행합니다.  
실행 중인 프로세스와 우선순위를 비교할 ready queue 맨 앞의 프로세스를 ready_process 변수에 저장합니다.  

```python
            if is_running: # 프로세스가 실행중이면 우선순위를 비교 (남은 시간)
                (중략)
            else: # idle일 경우 ready process를 바로 실행
                is_running = ready_process[2]
```
실행 중인 프로세스가 없을 경우 바로 ready_process를 실행합니다.  

```python
                if ready_process[2].bt < is_running.bt: # ready process의 남은 시간이 더 작을 경우 interrupt
                    ready_queue.put((is_running.bt, time, is_running))
                    is_running = ready_process[2] # 프로세스 클래스
                else: # 아닐 경우 다시 ready queue에 돌려놓습니다.
                    ready_queue.put(ready_process)
```
ready_process와 실행 중인 프로세스의 남은 burst time 을 비교해서 ready_process가 더 적게 남았을 경우 interrupt 하고 ready_process를 실행합니다. 
실행 중이던 프로세스는 준비 큐에 enqueue 합니다.  
실행 중인 프로세스가 더 적게 남았을 경우 ready_process를 다시 준비 큐에 돌려놓습니다. enqueued time은 현재 시간이 아닌 원래 시간으로 넣습니다.  

***
### RR
> Ready Queue : Queue (큐)

Queue 모듈의 Queue 자료구조를 그대로 사용해서 준비 큐의 FIFO 특성을 구현했습니다.  

> 주요 변수  

##### time_tq  
time quantum이 지났는 지 확인하는 타이머  
time quantum이 지났을 경우 0으로 초기화됩니다. 프로세스 실행이 끝나서 idle 상태가 될 경우 0으로 초기화되고 시간에 따라 증가하지 않습니다.  

> 알고리즘 핵심 코드

```python
        if time_tq % tq == 0 or not is_running: # time quantum이 지났거나 idle이면 inturrupt
            if not ready_queue.empty(): # ready queue가 비어있지 않으면
                if is_running:
                    ready_queue.put(is_running) # 실행 중인 프로세스를 inturrupt하고 준비 큐에 삽입
                is_running = ready_queue.get() # 준비 큐 가장 앞의 프로세스를 받아옵니다.
```
프로세스 실행이 끝나서 idle 상태이거나, Time quantum이 지난 경우에만 interrupt가 발생합니다.  
Time quantum이 지난 경우 실행 중인 프로세스를 준비 큐에 삽입합니다. 그리고 준비 큐에서 dequeue한 프로세스를 실행시킵니다.
Idle 상태였을 경우 바로 준비 큐에서 프로세스를 dequeue해 실행시킵니다.

***

FCFS랑 SJF 알고리즘도 이 코드를 기반으로 하고 있어서 해당 내용 참고하셔도 좋을 것 같습니다!
