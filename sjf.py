n = int(raw_input('Enter number of process : '))

processes=[]
for i in range(0,n):
 processes.insert(i,i+1)
bursttime = list()

print 'Enter burst time of the processes  '
for i in range(int(n)):
    p = raw_input("burst time :")
    bursttime.append(int(p))
print 'burst times are: ',bursttime

for i in range(0,len(bursttime)-1):
 for j in range(0,len(bursttime)-i-1):
  if(bursttime[j]>bursttime[j+1]):
   temp=bursttime[j]
   bursttime[j]=bursttime[j+1]
   bursttime[j+1]=temp
   temp=processes[j]
   processes[j]=processes[j+1]
   processes[j+1]=temp
waitingtime=[]
averagewaitingtime=0
turnaroundtime=[]
avgoftat=0
waitingtime.insert(0,0)
turnaroundtime.insert(0,bursttime[0])
for i in range(1,len(bursttime)):
 waitingtime.insert(i,waitingtime[i-1]+bursttime[i-1])
 turnaroundtime.insert(i,waitingtime[i]+bursttime[i])
 averagewaitingtime+=waitingtime[i]
 avgoftat+=turnaroundtime[i]
averagewaitingtime=float(averagewaitingtime)/n
avgoftat=float(avgoftat)/n'
