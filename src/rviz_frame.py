import roslib
import rviz

import sys

from python_qt_binding.QtGui import *
from python_qt_binding.QtCore import *

class RvizFrame(QWidget):
    def __init__(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    b = QLabel(w)

    b.setText("Hello!")
    w.setGeometry(100, 100, 200, 50)

    b.move(50, 20)
    w.setWindowTitle("PYQT")

    w.show()
    app.exec_()
    #sys.exit()
