import roslib
import rviz
import rospy
import sys

from python_qt_binding.QtGui import *
from python_qt_binding.QtCore import *

from input_handler import InputHandler

class InputFormFrame (QWidget):
    def __init__(self):
        QWidget.__init__(self)
        main_layout = QHBoxLayout()

        self.label_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()
        main_layout.addWidget(self.label_layout)
        main_layout.addWidget(self.content_layout)

        self.prs = {}

    def set_value(name, value):
        if name not in self.prs:
            self.prs[name] = QLineEdit()

class RvizFrame(QWidget):
    def __init__(self, bag_list=[]):
        QWidget.__init__(self)
        self.frame = rviz.VisualizationFrame()
        self.frame.setSplashPath('')
        self.frame.initialize()
        config_reader = rviz.YamlConfigReader()
        rviz_config = rviz.Config()
        config_reader.readFile(rviz_config, '../config.rviz')
        self.frame.load(rviz_config)

        self.frame.setMenuBar(None)
        self.frame.setStatusBar(None)
        self.frame.setHideButtonVisibility(False)

        self.nextButton = QPushButton('next')
        self.nextButton.clicked.connect(self.readNextBag)

        self.input_handler = InputHandler()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.frame)
        self.layout.addWidget(self.nextButton)
        self.layout.addWidget(self.input_handler)
        self.setLayout(self.layout)

        self.bag_lst = list(bag_list)
        self.bag_data = {file_name:{} for file_name in self.bag_lst}
        self.lst_idx = 0
        rospy.set_param('bag_to_read', self.bag_lst[self.lst_idx])

    def readNextBag(self):
        self.lst_idx += 1
        self.lst_idx %= len(self.bag_lst)
        rospy.set_param('bag_to_read', self.bag_lst[self.lst_idx])
