import roslib
import rviz
import rospy
import sys

from python_qt_binding.QtGui import *
from python_qt_binding.QtCore import *

from input_handler import InputHandler

class RvizFrame(QWidget):
    def __init__(self, bag_list=[]):
        QWidget.__init__(self)
        self.bag_lst = list(bag_list)
        self.bag_data = {file_name:{} for file_name in self.bag_lst}
        self.lst_idx = 0
        rospy.set_param('bag_to_read', self.bag_lst[self.lst_idx])

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

        self.input_handler = InputHandler(self.bag_lst)

        layout = QVBoxLayout()
        layout.addWidget(self.frame)
        layout.addWidget(self.nextButton)
        layout.addWidget(self.input_handler)
        self.setLayout(layout)

    def readNextBag(self):
        self.lst_idx += 1
        self.lst_idx %= len(self.bag_lst)
        rospy.set_param('bag_to_read', self.bag_lst[self.lst_idx])
