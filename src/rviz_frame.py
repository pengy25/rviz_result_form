import roslib
import rviz
import rospy
import rosbag
import rosnode
import sys

from sensor_msgs.msg import PointCloud2
from visualization_msgs.msg import MarkerArray

from multiprocessing import Process

from python_qt_binding.QtGui import *
from python_qt_binding.QtCore import *

def publisher_process(cloud_pub, cloud, marker_pub, markers):
    rospy.init_node('rviz_result_form')
    while rospy.Time().now().to_sec() == 0:
        pass
    while not rospy.is_shutdown():
        cloud_pub.publish(cloud)
        marker_pub.publish(markers)

    print "Process shutdown as rospy is shutdown"

class RvizFrame(QWidget):
    def __init__(self):
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

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.frame)
        self.setLayout(self.layout)

        self.cloud_pub = rospy.Publisher('cloud', PointCloud2, queue_size=1)
        self.marker_pub = rospy.Publisher('markers', MarkerArray, queue_size=1)

        self.cloud = None
        self.markers = None

    def readBag(self, file_path):
        bag = rosbag.Bag(file_path)

        for topic, msg, t in bag.read_messages():
            if topic == 'cloud':
                self.cloud = msg
            elif topic == 'markers':
                self.markers = msg
            else:
                continue

        bag.close()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    frame = RvizFrame()
    frame.resize(500, 500)
    frame.readBag('saved_exp_result.bag')
    process = Process(target=publisher_process, args=[frame.cloud_pub, frame.cloud, frame.marker_pub, frame.markers])
    process.start()
    frame.show()
    app.exec_()
    #sys.exit()
    #rosnode.kill_node(["rviz_result_form"])
    #rospy.signal_shutdown("Shutting down rospy as the main process is about to terminate")
    process.terminate()
