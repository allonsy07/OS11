def schedulingNonpreemptivePriority(data):
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
    print(process_data)
    # sort the data according to arrival time
    process_data.sort(key=lambda x: x[1])
    ganttchart = []  # 프로세스 실행 sequence
    time_clock = 0 #진행시간
    ready_queue = [] #레디큐
    stage = 0
    meta_data = []
    print(process_data, len(process_data), process_data[0][1])
    while 1:
        #if stage>10: break
        stage += 1
        print("{}번째 단계".format(stage))
        #move into ready_queue
        for i in range(len(process_data)):
            #print("flag", i)
            if process_data[i][1] <= time_clock and process_data[i][5] != 1:
                process_data[i][5] = 1
                ready_queue.append(process_data[i])
        print("before sort ready_queue", ready_queue)

        #priority check and sort
        if len(ready_queue)!=0:
            if len(ganttchart) != 0 and ready_queue[0][0] == ganttchart[-1]: #간트차트 비어있지 않다 == 전에 실행된 것이 있음 + 아직 실행 중인 것이 끝나지 않음
                print("ganttchart[-1]", ganttchart[-1])
                temp = ready_queue[1:]
                print("temptemp", temp)
                temp.sort(key=lambda x: (x[4], x[1]), reverse=False) #뒤에 들어온 것이 있다면 뒤에 것들만 정렬
                for step in range(len(ready_queue) - 1):
                    ready_queue[step + 1] = temp[step]
            else: #그렇지 않다면 앗쎄이 정리
                ready_queue.sort(key=lambda x: (x[4], x[1]), reverse=False)
            # 실행 by 1 time clock
            print("after sort ready_queue", ready_queue)

            if ready_queue[0][2] == ready_queue[0][3]: # 처음 들어오는 것
                ready_queue[0][6] = time_clock
            ganttchart.append(ready_queue[0][0])
            print("ganttchart", ganttchart)
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



# 0: pid, 1: 도착시간, 2: burst_time, 3: 우선순위(낮은게 우선), 4: Time quantum
data = [['p1',0,10,3,5],['p2',1,28,2,4], ['p3',2,6,4,3], ['p4',3,4,1,2], ['p5',4,14,2,1]] #example input
ganttchart, waiting_time_list, turnaround_time_list, response_time_list, average_waiting_time, average_turnaround_time, average_response_time = schedulingNonpreemptivePriority(data)

print("show the result-------------")
print("pid\t\tAT\t\tBT\t\tPr\t\tTQ\t\tWT\t\tTT\t\tRT")
for i in range(len(data)):
    for j in range(len(data)):
        print(data[i][j], end="\t\t")
    print(waiting_time_list[i], end="\t\t")
    print(turnaround_time_list[i], end="\t\t")
    print(response_time_list[i], end="\t\t")
    print()
print("average_waiting_time:", average_waiting_time)
print("average_turnaround_time:",average_turnaround_time)
print("average_response_time:", average_response_time)




