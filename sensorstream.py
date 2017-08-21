#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import std_msgs
import socket
import re
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 5555

publishers = {}
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))



def parse_data(data):
    res = {}

    nodeid = re.findall(r'<NodeId>(.*?)</NodeId>', str(data), re.DOTALL)
    if (len(nodeid) > 0):
        res["nodeid"] = nodeid[0]

    timestamp = re.findall(r'<TimeStamp>(.*?)</TimeStamp>', str(data), re.DOTALL)
    if (len(timestamp) > 0):
        res["timestamp"] = timestamp[0]

    Accelerometer = re.findall(r'<Accelerometer[1-3]>(.*?)</Accelerometer[1-3]>', str(data), re.DOTALL)
    if (Accelerometer):
        res["Accelerometer"]=Accelerometer

    Gyroscope = re.findall(r'<Gyroscope[1-3]>(.*?)</Gyroscope[1-3]>', str(data), re.DOTALL)
    if (Gyroscope):
        res["Gyroscope"] = Gyroscope

    LightIntensity = re.findall(r'<LightIntensity>(.*?)</LightIntensity>', str(data), re.DOTALL)
    if (len(LightIntensity) > 0):
        LightIntensity = LightIntensity[0]
        res["LightIntensity"] = LightIntensity

    return(res)

def add_publisher(id,sensor):
   publishers[id] = {}
   publishers[id][sensor]= rospy.Publisher('airacar/'+str(id)+"/"+sensor, String, queue_size=10)


def talker():
    rospy.init_node('sensorstream', anonymous=True)
    # rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_theader.stampime()
        # rospy.loginfo(hello_str)

        data, addr = sock.recvfrom(4096)  # buffer size is 1024 bytes
        r= parse_data(data)
        # print(r)
        # print(data)
        if not (r['nodeid'] in publishers.keys()):
            add_publisher(r['nodeid'],"LightIntensity")

        msg = std_msgs.msg.String()
        msg.data = r["LightIntensity"]

        # msg.header.stamp = r["timestamp"]*1000000

        publishers[r['nodeid']]["LightIntensity"].publish(msg)
        # print(rospy.Time.now())
        # print(r["timestamp"])





        # rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass