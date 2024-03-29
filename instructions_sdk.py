from djitellopy import Tello
import time
import sounddevice as sd
import numpy as np
from pynput import keyboard
import threading

# tello = Tello()
# stop = False


class Drone:
    def __init__(self):
        # Initialize the Tello object
        self.tello = Tello()
        # Create an empty list to keep track of commands executed
        self.reverse = []
        # Create a boolean flag to determine if the drone should accept more commands
        self.acceptCommands = True
        # Create an Event object to signal clapping detection
        self.clapping = threading.Event()
        #when esc is pressed this will be true
        self.halt = False
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
       # Start a separate thread to detect clapping sounds
        #monitor_thread = threading.Thread(target=self.detect_loud_noise, args=self)
        #monitor_thread.start()
    def on_press(self,key):
        if key == keyboard.Key.esc:
            self.halt = True

    def forward(self, forwardAmount):
        # Check if the drone should accept more commands
        if not self.acceptCommands:
            return
        # Move the drone forward by the specified amount
        value = self.tello.move_forward(forwardAmount)
        # Append the reverse command to the reverse list
        self.reverse.append((self.tello.move_forward, forwardAmount))
        # Wait for the clapping event to be set
        # self.clapping.wait()
        # Clear the event
        #self.clapping.clear()
        # Check if the clapping event is set
        if self.halt:
            # Set the acceptCommands flag to false
            self.acceptCommands = False
            # Execute the reverse path
            self.DoReversePath()

    def takeoff(self):
        # Take off the drone
        self.tello.takeoff()

    def land(self):
        # Land the drone
        self.tello.land()

    def connect(self):
        self.tello.connect(False)

    def rotateCW(self, angle):
        # Check if the drone should accept more commands
        if not self.acceptCommands:
            return
        # Rotate the drone clockwise by the specified angle
        self.tello.rotate_clockwise(angle)
        # Append the reverse command to the reverse list
        self.reverse.append((self.tello.rotate_counter_clockwise, angle))
        # Wait for the clapping event to be set
        # self.clapping.wait()
        # Clear the event
        #self.clapping.clear()
        # Check if the clapping event is set
        if self.halt:
            # Set the acceptCommands flag to false
            self.acceptCommands = False
            # Execute the reverse path
            self.DoReversePath()

    def rotateCCW(self, angle):
        # Check if the drone should accept more commands
        if not self.acceptCommands:
            return
        # Rotate the drone clockwise by the specified angle
        self.tello.rotate_counter_clockwise(angle)
        # Append the reverse command to the reverse list
        self.reverse.append((self.tello.rotate_clockwise, angle))
        # Wait for the clapping event to be set
        # self.clapping.wait()
        # Clear the event
        #self.clapping.clear()
        # Check if the clapping event is set
        if self.halt:
            # Set the acceptCommands flag to false
            self.acceptCommands = False
            # Execute the reverse path
            self.DoReversePath()

    def DoReversePath(self):
        # Rotate the drone clockwise by 180 degrees
        self.tello.rotate_clockwise(180)
        # Execute the reverse commands
        while self.reverse.__len__() > 0:
            func = self.reverse.pop()
            func[0](*func[1:])
        # Land the drone
        self.tello.land()

    def detect_loud_noise(self):
        while True:
            # Record audio for 1 second
            recording = sd.rec(8000, samplerate=sd.default.samplerate, channels=1)
            sd.wait()

            # Calculate the maximum amplitude of the recording
            max_amplitude = max(recording)

            # Convert amplitude to decibels
            max_decibels = 20 * (max_amplitude / 1)

            # Check if the maximum decibels is above 20
            if max_decibels > 20:
                # Set the clapping event
                print("clap set")
                self.clapping.set()







# def on_release(key):
#     return False


# tello.connect(False)
# tello.takeoff()




# while not stop:
#     if detect_loud_noise():
#         print("understood")
#         tello.flip_forward()
#         break


# tello.land()
