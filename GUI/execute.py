from distutils.command.build_scripts import first_line_re
import sys
from PyQt5.QtWidgets import QApplication
from first_page import First
from second_page import Second
from second_page2 import Second2
from second_page3 import Second3

if __name__ == '__main__':
  app = QApplication(sys.argv)
  first = First()
  second1 = Second()
  second2 = Second2()
  second3 = Second3()

  first.show()
  first.btn.clicked.connect(second1.show)
  first.btn.clicked.connect(first.close)
  first.btn2.clicked.connect(second2.show)
  first.btn2.clicked.connect(first.close)
  first.btn3.clicked.connect(second3.show)
  first.btn3.clicked.connect(first.close)

  second1.btn.clicked.connect(first.show)
  second1.btn.clicked.connect(second1.close)
  second2.btn.clicked.connect(first.show)
  second2.btn.clicked.connect(second2.close)
  second3.btn.clicked.connect(first.show)
  second3.btn.clicked.connect(second2.close)  

  sys.exit(app.exec_())
      