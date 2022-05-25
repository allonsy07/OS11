def processData(no_of_processes):  # data 입력받기
    process_data = []
    for i in range(no_of_processes):
        temporary = []
        process_id = int(input("Enter Process ID: "))
        arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
        burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
        priority = int(input(f"Enter Priority for Process {process_id}: "))
        temporary.extend([process_id, arrival_time, burst_time, burst_time,
                          priority, 0, 0, 0])  # 0: pid, 1: 도착시간, 2: burst_time, 3: 남은 burst_time, 4: 우선순위(낮은게 우선), 5:레디큐로 감, 6:start, 7:end
        process_data.append(temporary)
    return process_data

def schedulingPreemptivePriority(process_data):
    # sort the data according to arrival time
    process_data.sort(key=lambda x: x[1])
    ganttchart = []  # 프로세스 실행 sequence
    start_time = [] # 시작한 시간
    complete_time = [] # 끝난 시간
    time_clock = 0 #진행시간
    ready_queue = [] #레디큐
    stage = 0
    meta_data = []
    print(process_data, len(process_data), process_data[0][1])
    while 1:
        stage += 1
        print("{}번째 단계".format(stage))
        #move into ready_queue
        for i in range(len(process_data)):
            #print("flag", i)
            if process_data[i][1] == time_clock:
                process_data[i][5] = 1
                ready_queue.append(process_data[i])
        print("ready_queue", ready_queue)

        #priority check and sort
        if len(ready_queue)!=0:
            ready_queue.sort(key=lambda x: (x[4], x[1]), reverse=False)
            # 실행 by 1 time clock
            if ready_queue[0][2] == ready_queue[0][3]:
                ready_queue[0][6] = time_clock
            ganttchart.append(ready_queue[0][0])

            time_clock += 1
            ready_queue[0][3] -= 1
            if ready_queue[0][3] == 0: #실행 다한 프로세스는 ready_queue에서 삭제
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
                return ganttchart, meta_data


# 0: pid, 1: 도착시간, 2: burst_time, 3: 남은 burst_time, 4: 우선순위(낮은게 우선), 5:age
process_data = [['p1',0,3,3,1,0,0,0],['p2',5,3,3,0,0,0,0]]
gantt_chart, meta_data = schedulingPreemptivePriority(process_data)
print(gantt_chart)
print(meta_data)




