from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QDesktopWidget, QLabel, QTableWidget, QAbstractItemView, QTableWidgetItem
from algorithm import schedulingPP, schedulingSRTF, schedulingRR

class Second2(QWidget):
  def __init__(self):
    super().__init__() 
    self.current = [-1]      
    self.initUI()  
  
  def initUI(self):
    self.setWindowTitle('Ready Page') 
    self.resize(1200, 800)
    self.center()      

    title = QLabel('Welcome {}'.format(str('User_2')), self)
    title.move(400,-200)
    title.resize(450,450)
    title_font = title.font()
    title_font.setPointSize(50)
    title.setFont(title_font)            

    self.btn = QPushButton("First Page", self)
    self.btn.move(10, 10)
    btn_font = self.btn.font()
    btn_font.setPointSize(10)
    self.btn.setFont(btn_font) 

    self.table = QTableWidget(self)
    self.table.setRowCount(10)
    self.table.setColumnCount(5)
    self.table.resize(550, 200)
    self.table.move(550, 100)
    self.table.setHorizontalHeaderLabels(['ID', 'Arrival Time', 'Burst Time', 'Priority', 'Time Quantum'])

    clear = QPushButton('Clear', self)
    clear.clicked.connect(self.table.clearContents)
    clear.move(1000, 300)   

    ready = QPushButton('Ready', self)
    ready.clicked.connect(self.save)
    ready.move(900, 300)  

    self.cb1 = QCheckBox('First Come First Served (FCFS)', self)
    self.cb1.move(100, 100)
    self.cb1.resize(300,30)
    self.cb2 = QCheckBox('Shortest Job First (SJF)', self)
    self.cb2.move(100, 130)
    self.cb2.resize(300,30)
    self.cb3 = QCheckBox('Shortest Remaining Time First (SRTF)', self)
    self.cb3.move(100, 160)
    self.cb3.resize(300,30)
    self.cb4 = QCheckBox('Round Robin (RR)', self)
    self.cb4.move(100, 190)
    self.cb4.resize(300,30)
    self.cb5 = QCheckBox('Non-Preemptive Priority (NPP)', self)
    self.cb5.move(100, 220)
    self.cb5.resize(300,30)
    self.cb6 = QCheckBox('Preemptive Priority (PP)', self)
    self.cb6.move(100, 250)
    self.cb6.resize(300,30)
    self.cb7 = QCheckBox('Non-Preemptive Priority with RR (NPPwRR)', self)
    self.cb7.move(100, 280)
    self.cb7.resize(300,30)

    GBox = QLabel(self)
    GBox.setStyleSheet("color: dark;"
                             "border-style: solid;"
                             "border-width: 3px;"
                             "border-color: #000000;"
                             "border-radius: 3px")
    GBox.move(100, 350)
    GBox.resize(1000, 200) 

    self.GB = QLabel(self)    
    self.times = []
    self.lines = []
    self.labels = []
    for i in range(50):
        time = QLabel(self)
        line = QLabel(self)
        label = QLabel(self)
        time.resize(30,30)
        line.resize(30,30)
        label.resize(30,30)

        self.times.append(time)
        self.lines.append(line)
        self.labels.append(label)

    
    gb = QLabel(self)
    gb.setStyleSheet("color: dark;"
                             "border-style: solid;"
                             "border-width: 3px;"
                             "border-color: #000000;"
                             "border-radius: 3px")
    gb.move(100, 313)
    gb.resize(130, 40)    

    Gant = QLabel('Gantt Chart', self)
    Gant.move(105, 320)
    gant_font = Gant.font()
    gant_font.setPointSize(20)
    Gant.setFont(gant_font)    

    self.name = QLabel('                    ', self)
    self.name.move(115, 360)
    self.name_font = self.name.font()
    self.name_font.setPointSize(18)
    self.name.setFont(self.name_font)      

    prev = QPushButton('<', self)
    prev.clicked.connect(self.prev)
    prev.move(980, 500)

    next = QPushButton('>', self)
    next.clicked.connect(self.next)
    next.move(1030, 500)        

    output = QLabel(self)
    output.setStyleSheet("color: blue;"
                       "background-color: #87CEFA;"
                       "border-style: solid;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")   
    output.move(100, 570)
    output.resize(425, 50)     

    output2 = QLabel(self)
    output2.setStyleSheet("color: blue;"
                       "background-color: #87CEFA;"
                       "border-style: solid;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")   
    output2.move(100, 620)
    output2.resize(425, 50) 

    output3 = QLabel(self)
    output3.setStyleSheet("color: blue;"
                       "background-color: #87CEFA;"
                       "border-style: solid;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")   
    output3.move(100, 670)
    output3.resize(425, 50)    

    output4 = QLabel(self)
    output4.setStyleSheet("color: blue;"
                       "background-color: #87CEFA;"
                       "border-style: solid;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")   
    output4.move(100, 720)
    output4.resize(425, 50) 

    self.text1 = QLabel('평균 대기시간:                ', self)
    self.text1.move(105, 575)
    self.text1_font = self.text1.font()
    self.text1_font.setPointSize(30)
    self.text1.setFont(self.text1_font) 

    self.text2 = QLabel('평균 반환시간:                ', self)
    self.text2.move(105, 625)
    self.text2_font = self.text2.font()
    self.text2_font.setPointSize(30)
    self.text2.setFont(self.text2_font) 

    self.text3 = QLabel('평균 응답시간:                ', self)
    self.text3.move(105, 675)
    self.text3_font = self.text3.font()
    self.text3_font.setPointSize(30)
    self.text3.setFont(self.text3_font) 

    self.text4 = QLabel('추천 알고리즘:', self)                             
    self.text4.move(105, 725)
    self.text4_font = self.text4.font()
    self.text4_font.setPointSize(30)
    self.text4.setFont(self.text4_font)

    self.text5 = QLabel('                                                                              ',self)                             
    self.text5.move(300, 730)
    self.text5_font = self.text5.font()
    self.text5_font.setPointSize(25)
    self.text5.setFont(self.text5_font)        

    self.table2 = QTableWidget(self)
    self.table2.setRowCount(3)
    self.table2.setColumnCount(10)
    self.table2.resize(550, 150)
    self.table2.move(550, 620)
    self.table2.setVerticalHeaderLabels(['대기시간', '반환시간', '응답시간'])
    self.table2.setEditTriggers(QAbstractItemView.NoEditTriggers)    

    text5 = QLabel('OUTPUT', self)
    text5.move(550, 570)
    text5_font = text5.font()
    text5_font.setPointSize(30)
    text5.setFont(text5_font) 

  def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())   

  def save(self):
      rowcount = self.table.rowCount()
      columncount = self.table.columnCount()
      self.data = []
      self.ID = []        

      for row in range(0, rowcount):
          if self.table.item(row,0) is None:
              break
          self.data.append([])
          id = self.table.item(row,0)
          self.ID.append(str(id.text()))
          for column in range(0, columncount):
              value = self.table.item(row, column)
              if value is not None:
                  if column != 0:
                    self.data[row].append(int(value.text())) # ['ID', 'Arrival Time', 'Burst Time', 'Priority', 'Time Quantum'] 순서로 value가 들어감
                  else:
                    self.data[row].append(str(value.text()))  
              else:
                self.data[row].append(0)

      self.table2.setHorizontalHeaderLabels(self.ID)           
      self.list = []

      for cb, name in [(self.cb1, 'FCFS'), (self.cb2, 'SJF'), (self.cb3, 'SRTF'), (self.cb4, 'RR'), (self.cb5, 'NPP'), (self.cb6, 'PP'), (self.cb7, 'NPPwRR')]:
          if cb.isChecked():
              self.list.append(name)

      self.scheduling()

  def scheduling(self):
      if self.list is None:
          return None

      else:   
          self.output = []
        #   GC, WT, TA, RT, AWT, ATT, ART = schedulingFSFC(self.data)
        #   self.output.append([GC, WT, TA, RT, AWT, ATT, ART, 'FCFS'])

        #   GC, WT, TA, RT, AWT, ATT, ART = schedulingSJF(self.data)
        #   self.output.append([GC, WT, TA, RT, AWT, ATT, ART, 'SJF'])

          GC, WT, TA, RT, AWT, ATT, ART = schedulingSRTF(self.data)
          self.output.append([GC, WT, TA, RT, AWT, ATT, ART, 'SRTF'])
          
          GC, WT, TA, RT, AWT, ATT, ART = schedulingRR(self.data)
          self.output.append([GC, WT, TA, RT, AWT, ATT, ART, 'RR'])

        #   GC, WT, TA, RT, AWT, ATT, ART = schedulingNPP(self.data)
        #   self.output.append([GC, WT, TA, RT, AWT, ATT, ART, 'NPP'])

          GC, WT, TA, RT, AWT, ATT, ART = schedulingPP(self.data)
          self.output.append([GC, WT, TA, RT, AWT, ATT, ART, 'PP'])                                                   

        #   GC, WT, TA, RT, AWT, ATT, ART = schedulingNPPwRR(self.data)
        #   self.output.append([GC, WT, TA, RT, AWT, ATT, ART, 'NPPwRR'])

          self.recommendation()
          self.draw_output()

  def recommendation(self):
      self.rec1 = sorted(self.output, key = lambda x : (x[-4], x[-3], x[-2]))
      self.rec2 = sorted(self.output, key = lambda x : (x[-3], x[-2], x[-4]))
      self.rec3 = sorted(self.output, key = lambda x : (x[-2], x[-3], x[-4]))
      self.top1 = self.rec1[0][-1]  
      self.top2 = self.rec2[0][-1]
      self.top3 = self.rec3[0][-1]

      self.text4.setText('추천 알고리즘:')
      self.text5.setText(' {}, {}, {}'.format(self.top1, self.top2, self.top3))

  def draw_output(self, alpha = 1):
      if alpha == 1:
        self.current = [self.list[0], 0]

      self.name.setText('{}'.format(self.current[0]))

      self.gantt_chart()
      self.draw_remain()

  def prev(self):
      if len(self.list) != 0:
        if self.current[-1] != 0:
            self.current = [self.list[self.current[-1] - 1], self.current[-1] - 1]
            self.draw_output(alpha = 0)
        else:
            pass
      else:
          pass

  def next(self):
      if len(self.list) != 0:      
        if self.current[-1] != len(self.list) - 1:
            self.current = [self.list[self.current[-1] + 1], self.current[-1] + 1]
            self.draw_output(alpha = 0)
        else:
            pass
      else:
          pass  

  def gantt_chart(self):       
      for i in range(len(self.output)):
          if self.current[0] in self.output[i]:
              index = i
              break     

      GT = self.output[index][0] 
      final_time = len(GT)    

      self.GB.setStyleSheet("color: dark;"
                             "border-style: solid;"
                             "border-width: 2px;"
                             "border-color: #000000;"
                             "border-radius: 3px")
      self.GB.move(130, 390)
      self.GB.resize(930, 80)

      box_size = 930

      st = self.times[0]  
      st.setText("0")    
      st.move(130, 475)
      st_font = st.font()
      st_font.setPointSize(18)
      st.setFont(st_font)    

      new_GT = []

      for i, alpha in enumerate(GT):
        if i == 0:
          cnt = 1
          prev = alpha
          new_GT.append((alpha, cnt))
          continue
    
        if alpha == prev:
          cnt += 1
          new_GT[-1] = (alpha, cnt)

        else:
          cnt = 1
          new_GT.append((alpha, cnt))
          prev = alpha


      start = 130
      accum_time = 0

      for i in range(50):
          p = self.labels[i]
          l = self.lines[i]
          p.setText('')
          l.resize(0,0)

          if i == 49:
            break
          t = self.times[i+1]
          t.setText('')


      for i, value in enumerate(new_GT):
          process, time = value
          accum_time += time
          p = self.labels[i]
          p.setText('{}'.format(process))
          end = start + int(((box_size  * time)/ final_time))
          if time == final_time:
            end = start + box_size          
          p.move(int((start + end) / 2) - 5, 416)
          p_font = p.font()
          p_font.setPointSize(18)
          p.setFont(p_font) 

          start = end

          if i != len(new_GT) - 1:
            l = self.lines[i]
            l.setStyleSheet("color: dark;"
                              "border-style: solid;"
                              "border-width: 2px;"
                              "border-color: #000000;"
                              "border-radius: 3px")          
            l.move(end, 390)
            l.resize(2, 80)     

          t = self.times[i+1]
          t.setText('{}'.format(accum_time))
          t.move(end-5, 475)
          t_font = t.font()
          t_font.setPointSize(18)
          t.setFont(t_font)           


  def draw_remain(self):
      for i in range(len(self.output)):
          if self.current[0] in self.output[i]:
              index = i
              break
      
      self.text1.setText('평균 대기시간: {}'.format(self.output[index][4]))
      self.text2.setText('평균 반환시간: {}'.format(self.output[index][5]))
      self.text3.setText('평균 응답시간: {}'.format(self.output[index][6]))

      WT = self.output[index][1]
      TA = self.output[index][2]
      RT = self.output[index][3]

      for i in range(len(WT)):
          val = QTableWidgetItem(str(WT[i]))
          self.table2.setItem(0, i, val)

      for i in range(len(TA)):
          val = QTableWidgetItem(str(TA[i]))
          self.table2.setItem(1, i, val)

      for i in range(len(RT)):
          val = QTableWidgetItem(str(RT[i]))
          self.table2.setItem(2, i, val)

     
