from instructions_sdk import Drone
import time

tello = Drone()
tello.connect()
tello.takeoff()
time.sleep(4)
tello.forward(250)
tello.rotateCW(90)
tello.forward(400)
tello.rotateCW(90)
tello.forward(100)
tello.land()