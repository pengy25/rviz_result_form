import rospy

from python_qt_binding.QtGui import QWidget, QLabel, QVBoxLayout

class InputHandler(QWidget):
    def __init__(self, file_lst):
        QWidget.__init__(self)
        self.file_lst = list(file_lst)
        for file_name in self.file_lst:
            pass
        layout = QVBoxLayout()
        self.setLayout(layout)

        if len(rospy.get_name()) == 0:
            rospy.logerr("Error: the node has not been initialized!")
        else:
            rospy.loginfo("Received node name as %s", rospy.get_name())

        self.json_str = ""



    def input_update_callback(self, msg):
        if self.json_str == msg.data:
            return

        self.json_str = ""

    def write_to_file(self, location):
        pass
