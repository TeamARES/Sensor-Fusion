import serial
import syslog
import time
import json
import rospy
from sensor_msgs.msg import Imu

imu_port = '/dev/ttyACM0'
ard = serial.Serial(imu_port,57600,timeout=5)

# while True:



def talker():
    pub = rospy.Publisher('imu', Imu, queue_size=10)
    rospy.init_node('ros_erle_imu', anonymous=True)
    rate = rospy.Rate(10)



    flag = True
    while not rospy.is_shutdown():
        msg = Imu()
        try:
            if flag:
                flag = False
                b = ard.readline()
                # time.sleep(3)
            b = ard.readline()  # read a byte string

            string_n = b.decode()  # decode byte string into Unicode
            string = string_n.rstrip()  # remove \n and \r
            imu_obj = json.loads(string)
            msg.header.stamp = rospy.Time.now()
            msg.header.frame_id = "odom"


        # Fill message
            msg.orientation.x = imu_obj["orientationx"]
            msg.orientation.y = imu_obj["orientationy"]
            msg.orientation.z = imu_obj["orientationz"]
            msg.orientation.w = imu_obj["orientationw"]
            msg.orientation_covariance[0] = imu_obj["orientationx"] * imu_obj["orientationx"]
            msg.orientation_covariance[0] = imu_obj["orientationy"] * imu_obj["orientationy"]
            msg.orientation_covariance[0] = imu_obj["orientationz"] * imu_obj["orientationz"]
            msg.angular_velocity.x = imu_obj["angular_velocityx"]
            msg.angular_velocity.y = imu_obj["angular_velocityy"]
            msg.angular_velocity.z = imu_obj["angular_velocityz"]
            msg.angular_velocity_covariance[0] = imu_obj["angular_velocityx"] * imu_obj["angular_velocityx"]
            msg.angular_velocity_covariance[4] = imu_obj["angular_velocityy"] * imu_obj["angular_velocityy"]
            msg.angular_velocity_covariance[8] = imu_obj["angular_velocityz"] * imu_obj["angular_velocityz"]

            msg.linear_acceleration.x = imu_obj["linear_accelerationx"]
            msg.linear_acceleration.y = imu_obj["linear_accelerationy"]
            msg.linear_acceleration.z = imu_obj["linear_accelerationz"]
            msg.linear_acceleration_covariance[0] = imu_obj["linear_accelerationx"] * imu_obj["linear_accelerationx"]
            msg.linear_acceleration_covariance[4] = imu_obj["linear_accelerationy"] * imu_obj["linear_accelerationy"]
            msg.linear_acceleration_covariance[8] = imu_obj["linear_accelerationz"] * imu_obj["linear_accelerationz"]

            pub.publish(msg)

            rate.sleep()
        except (json.decoder.JSONDecodeError, UnicodeDecodeError):
            continue

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass