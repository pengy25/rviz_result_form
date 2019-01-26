import rospy

from python_qt_binding.QtGui import QWidget, QLabel, QVBoxLayout

class InputHandler(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("IOU"))
        self.setLayout(layout)

        if len(rospy.get_name()) == 0:
            print("Error: the node has not been initialized!")
        else:
            print("Received node name as %s" % (rospy.get_name(),))

    def input_update_callback(self):
        pass

    def write_to_file(self, location):
        pass
