# Nonpreemptive Priority with Round Robin

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

> is_running : Round Robin에 들어가는 프로세스 변수
> running_process: 우선순위 로직에 사용되는 프로세스 변수

None 으로 초기화하여 실행 중인 프로세스를 저장합니다. Idle 상태일 경우 None 값을 가집니다.

***
### Nonpreemptive Priority with Round Robin
> available_process : dictionary 자료형을 사용하였으며, arrival time이 되어 실행할 준비가 된 프로세스를 넣어줍니다. 우선순위에 따라 프로세스를 실행하므로, {우선순위: [프로세스, 프로세스, ...]} 의 형태로 저장하도록 하였습니다.

각 프로세스 별 우선순위가 높은 순서대로 먼저 실행되도록 구현하였습니다.
우선순위에 따라 프로세스의 실행순서를 결정하고 우선순위가 같은 경우, 해당 프로세스들에 Round Robin 방식을 적용하여 time quantum에 따라 돌아가면서 실행되도록 구현하였습니다.

> 알고리즘 핵심 코드

1. 전체적인 알고리즘 구조 설명

`available_process`에 dictionary 형태로 우선순위에 따라 프로세스를 정렬시킵니다.
우선순위를 바탕으로 while 문 안에서 진행을 하게 되는데, 우선순위가 같은게 하나인 경우(프로세스 본인 말고 동일한 우선순위가 없을 경우)에는 Nonpreemptive priority algorithm을 바탕으로 프로세스를 처리합니다. 이 경우에 첫번째 `if` 내부에서 동작하게 됩니다. 만약 arrival time이 지나고 동일한 우선순위를 가진 프로세스가 2개 이상인 경우 `elif` 문으로 들어가 Round Robin 알고리즘을 바탕으로 프로세스를 처리합니다. 

```python
    if len(available_process[highest_priority]) == 1:
        # apply non preemptive priority algorithm
    elif len(available_process[highest_priority]) >= 2:
        # apply round robin algorithm
    else:
        # Do nothing
```

2. NonPreemptive Priority 부분 설명(if)

우선순위가 가장 높은 프로세스를 가져와 프로세스의 burst time 만큼 실행시킵니다.

```python
for pl in available_process[highest_priority]:
    pp_process_list.append(pl[2])
running_process = available_process[highest_priority][0]
burst_time = running_process[1]
time += burst_time
```

3. Round Robin 부분 설명 (elif)

time quantum을 바탕으로 같은 우선순위에 있는 프로세스들을 번갈아가며 수행합니다.

```python
if time_tq % tq == 0 or not is_running:
    if not rr_ready_queue.empty():
        if is_running:
            rr_ready_queue.put(is_running)
        is_running = rr_ready_queue.get()
```

