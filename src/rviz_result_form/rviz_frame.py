import roslib
import rviz
import rospy
import sys

from python_qt_binding.QtGui import *
from python_qt_binding.QtCore import *

from std_msgs.msg import String

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

        self.input_handler = InputHandler()

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.frame)
        vLayout.addWidget(self.nextButton)
        hLayout = QHBoxLayout()
        hLayout.addLayout(vLayout)
        hLayout.addWidget(self.input_handler)
        self.setLayout(hLayout)

        # pyqt event is not supported in multithreading...
        #self.json_str_sub = rospy.Subscriber('json_str_pub', String, self.input_handler.input_update_callback)
        self.input_handler.input_update_callback()

    def readNextBag(self):
        self.lst_idx += 1
        self.lst_idx %= len(self.bag_lst)
        rospy.set_param('bag_to_read', self.bag_lst[self.lst_idx])
        self.input_handler.input_update_callback()
