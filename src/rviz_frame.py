import roslib
import rviz
import rospy
import rosbag
import sys

from sensor_msgs.msg import PointCloud2
from visualization_msgs.msg import MarkerArray
from visualization_msgs.msg import Marker

from multiprocessing import Process

from python_qt_binding.QtGui import *
from python_qt_binding.QtCore import *

def readBag(file_path):
    bag = rosbag.Bag(file_path)
    cloud = None
    markers = None

    for topic, msg, t in bag.read_messages():
        if topic == 'cloud':
            cloud = msg
        elif topic == 'markers':
            markers = msg
        else:
            continue

    bag.close()

    return (cloud, markers)

def publisher_process():
    rospy.init_node('rviz_result_form')
    while rospy.Time().now().to_sec() == 0:
        pass

    cloud_pub = rospy.Publisher('cloud', PointCloud2, queue_size=200)
    marker_pub = rospy.Publisher('markers', MarkerArray, queue_size=200)

    current_bag = None
    cloud = None
    markers = MarkerArray()

    while not rospy.is_shutdown():
        if current_bag != rospy.get_param('bag_to_read'):
            marker_arr = MarkerArray()
            for marker in markers.markers:
                marker_to_delete = Marker()
                marker_to_delete.header = marker.header
                marker_to_delete.ns = marker.ns
                marker_to_delete.id = marker.id
                marker_to_delete.action = marker_to_delete.DELETE
                marker_arr.markers.append(marker_to_delete)
            marker_pub.publish(marker_arr)

            current_bag = rospy.get_param('bag_to_read')
            cloud, markers = readBag(current_bag)
        cloud_pub.publish(cloud)
        marker_pub.publish(markers)

    print "Process shutdown as rospy is shutdown"

class RvizFrame(QWidget):
    def __init__(self, bag_list=[]):
        QWidget.__init__(self)
        self.frame = rviz.VisualizationFrame()
        self.frame.setSplashPath('')
        self.frame.initialize()
        config_reader = rviz.YamlConfigReader()
        rviz_config = rviz.Config()
        config_reader.readFile(rviz_config, 'config.rviz')
        self.frame.load(rviz_config)

        self.frame.setMenuBar(None)
        self.frame.setStatusBar(None)
        self.frame.setHideButtonVisibility(False)

        self.nextButton = QPushButton('next')
        self.nextButton.clicked.connect(self.readNextBag)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.frame)
        self.layout.addWidget(self.nextButton)
        self.layout.addWidget(QLineEdit())
        self.layout.addWidget(QLineEdit())
        self.setLayout(self.layout)

        self.bag_lst = list(bag_list)
        self.lst_idx = 0
        rospy.set_param('bag_to_read', self.bag_lst[self.lst_idx])

    def readNextBag(self):
        self.lst_idx += 1
        self.lst_idx %= len(self.bag_lst)
        rospy.set_param('bag_to_read', self.bag_lst[self.lst_idx])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    lst = ['saved_exp_result1.bag', 'saved_exp_result2.bag']

    frame = RvizFrame(lst)
    frame.resize(500, 500)
    process = Process(target=publisher_process)
    process.start()
    frame.show()
    app.exec_()
    process.terminate()
