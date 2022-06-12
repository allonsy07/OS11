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

> is_running : 프로세스 변수

None 으로 초기화하여 실행 중인 프로세스를 저장합니다. Idle 상태일 경우 None 값을 가집니다.

***
### Nonpreemptive Priority with Round Robin
> Ready Queue : Priority Queue(우선순위 큐)

PriorityQueue 라는 자료구조를 활용하여 각 프로세스 별 우선순위가 높은 순서대로 먼저 실행되도록 구현하였습니다.
우선순위에 따라 프로세스의 실행순서를 결정하고 우선순위가 같은 경우, 해당 프로세스들에 Round Robin 방식을 적용하여 time quantum에 따라 돌아가면서 실행되도록 구현하였습니다.
