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



