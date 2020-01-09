import serial
import syslog
import time
import json
import rospy
from sensor_msgs.msg import NavSatFix

gps_port = '/dev/ttyUSB0'
ard = serial.Serial(gps_port,9600,timeout=5)

# while True:



def talker():
    pub = rospy.Publisher('gps', NavSatFix, queue_size=10)
    rospy.init_node('ros_GPS', anonymous=True)
    rate = rospy.Rate(10)

    gpsmsg = NavSatFix()



    flag = True
    while not rospy.is_shutdown():
        try:
            gpsmsg.header.stamp = rospy.Time.now()
            gpsmsg.header.frame_id = "gps"
            if flag:
                flag = False
                b = ard.readline()
                # time.sleep(3)
            b = ard.readline()  # read a byte string

            string_n = b.decode()  # decode byte string into Unicode
            string = string_n.rstrip()  # remove \n and \r
            lat = string.split(" ")[0]
            lng = string.split(" ")[1]
            gpsmsg.latitude = float(lat)
            gpsmsg.longitude = float(lng)



            pub.publish(gpsmsg)

            rate.sleep()
        except (json.decoder.JSONDecodeError, UnicodeDecodeError):
            continue

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass