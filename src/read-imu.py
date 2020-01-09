import asyncio
import websockets
import serial
import syslog
import time

imu_port = '/dev/ttyACM0'
ard = serial.Serial(port,57600,timeout=5)

import asyncio
import websockets

def echo(websocket, path):
    while True:
        # print("here")
        b = ard.readline()  # read a byte string
        string_n = b.decode()  # decode byte string into Unicode
        string = string_n.rstrip()  # remove \n and \r
        # readings = string.split(",")
        # if len(readings[0]) != 19:
        #     continue
        # print(readings)
        # await websocket.send(readings[0])

asyncio.get_event_loop().run_until_complete(
websockets.serve(echo, '0.0.0.0', 8765))
asyncio.get_event_loop().run_forever()