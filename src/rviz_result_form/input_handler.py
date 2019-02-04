import rospy
import json

from python_qt_binding.QtGui import QWidget, QLabel, QVBoxLayout
from .input_form_manager import InputFormManager

class InputHandler(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        while not rospy.has_param('bag_to_read'):
            pass

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        if len(rospy.get_name()) == 0:
            rospy.logerr("Error: the node has not been initialized!")
        else:
            rospy.loginfo("Received node name as %s", rospy.get_name)


        self.mgr_lst = {}
        self.curr_bag = None

    def input_update_callback(self, msg):
        bag_name = rospy.get_param('bag_to_read')
        if bag_name not in self.mgr_lst:
            json_dict = json.loads(msg.data)
            label_value_pr = []
            keys = sorted(json_dict.keys())
            for key in keys:
                label = str(key)
                value = str(json_dict[key])
                label_value_pr.append((label, value))

            mgr = InputFormManager(label_value_pr)
            self.mgr_lst[bag_name] = mgr
            self.layout.addWidget(mgr)

        if self.curr_bag is not None and self.curr_bag != bag_name:
            self.mgr_lst[self.curr_bag].hide()

        self.mgr_lst[bag_name].show()
        self.curr_bag = bag_name


    def write_to_file(self, location):
        pass
