print("FCFS SCHEDULLING")
n = int(input("Enter number of processes : "))
d = dict()

for i in range(n):
    key = "P" + str(i + 1)
    a = int(input("Enter arrival time of process" + str(i + 1) + ": "))
    b = int(input("Enter burst time of process" + str(i + 1) + ": "))
    l = []
    l.append(a)
    l.append(b)
    d[key] = l

d = sorted(d.items(), key=lambda item: item[1][0])

ET = []
for i in range(len(d)):
    if (i == 0):
        ET.append(d[i][1][1])

    # get prevET + newBT
    else:
        ET.append(ET[i - 1] + d[i][1][1])

TAT = []
for i in range(len(d)):
    TAT.append(ET[i] - d[i][1][0])

WT = []
for i in range(len(d)):
    WT.append(TAT[i] - d[i][1][1])

avg_WT = 0
for i in WT:
    avg_WT += i
avg_WT = (avg_WT / n)


print("Process\t  Burst Time\t  Waiting Time\t  TurnAround Time")
for i in range(0,n):
 print(str(processes[i])+"\t\t"+str(bursttime[i])+"\t\t"+str(waitingtime[i])+"\t\t"+str(turnaroundtime[i]))
 print("\n")
print("Average Waitingtime is: "+str(averagewaitingtime))
print("Average TurnAround Time is: "+str(avgoftat)
