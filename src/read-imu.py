import serial
import syslog
import time
import json

imu_port = '/dev/ttyACM0'
ard = serial.Serial(imu_port,57600,timeout=5)
flag = True

while True:
    if flag:
        flag = False
        b = ard.readline()
        time.sleep(1)
    b = ard.readline()  # read a byte string

    string_n = b.decode()  # decode byte string into Unicode
    string = string_n.rstrip()  # remove \n and \r
    imu_obj = json.loads(string)
    print(imu_obj)
