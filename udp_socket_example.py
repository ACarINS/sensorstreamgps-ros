import socket
import time
UDP_IP = "0.0.0.0"
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

def start_element(name, attrs):
	# tags[name] = tags[name] + 1 if name in tags else 1
   print("Element",name)


import re


pattern = r'<NodeId>(.*?)</NodeId>'


while True:
   data, addr = sock.recvfrom(4096) # buffer size is 1024 bytes
   print(data)
   nodeid = re.findall(r'<NodeId>(.*?)</NodeId>', str(data), re.DOTALL)
   if(len(nodeid)>0) :
      nodeid=nodeid[0]
   print(nodeid)
   timestamp = re.findall(r'<TimeStamp>(.*?)</TimeStamp>', str(data), re.DOTALL)
   if(len(nodeid)>0) :
      timestamp=timestamp[0]
   print(timestamp)
   Accelerometer = re.findall(r'<Accelerometer[1-3]>(.*?)</Accelerometer[1-3]>', str(data), re.DOTALL)
   if (Accelerometer) :
      print("Accelerometer:",Accelerometer)
   Gyroscope = re.findall(r'<Gyroscope[1-3]>(.*?)</Gyroscope[1-3]>', str(data), re.DOTALL)
   if (Gyroscope):
      print("Gyroscope:", Gyroscope)


         # //print(etree.fromstring(data))
