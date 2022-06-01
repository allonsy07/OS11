from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QDesktopWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize

class First(QMainWindow):
  def __init__(self):
    super().__init__()

    self.initUI()
  
  def initUI(self):
    self.setWindowTitle('Login Page')
    self.resize(800, 800)
    self.center()   

    title = QLabel('OS TermProject', self)
    title.move(225,-150)
    title.resize(450,450)
    title_font = title.font()
    title_font.setPointSize(50)
    title.setFont(title_font)          

    info = QLabel('Team 11', self)
    info.move(350, 550)
    info.resize(200,200)
    info_font = info.font()
    info_font.setPointSize(30)
    info.setFont(info_font)      

    info2 = QLabel('주재원, 김재훈, 김한주, 안수진, 이진호', self)
    info2.move(260, 600)
    info2.resize(600,200)
    info2_font = info2.font()
    info2_font.setPointSize(20)
    info2.setFont(info2_font)          

    self.btn = QPushButton("User_1", self)
    self.btn.resize(500,100)
    self.btn.move(150, 160)           

    self.btn2 = QPushButton("User_2", self)
    self.btn2.resize(500,100)
    self.btn2.move(150, 320) 

    self.btn3 = QPushButton("User_3", self)
    self.btn3.resize(500,100)
    self.btn3.move(150, 480)     

  def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft()) 