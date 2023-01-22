from djitellopy import Tello
import time
import sounddevice as sd
import numpy as np
from pynput import keyboard

tello = Tello()
stop = False

def detect_loud_noise():
    # Record audio for 1 second
    recording = sd.rec(8000, 
                      samplerate=sd.default.samplerate, 
                      channels=1)
    sd.wait()
    
    # Calculate the maximum amplitude of the recording
    max_amplitude = max(recording)
    
    # Convert amplitude to decibels
    max_decibels = 20 * (max_amplitude / 1)
    
    # Check if the maximum decibels is above 20
    if max_decibels > 20:
        return True
    else:
        return False

def on_press(key):
    #tello.land()
    print("stop")
    global stop
    stop = True

def on_release(key):
    return False


tello.connect(False)
tello.takeoff()

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while(not stop):
    if(detect_loud_noise()):
        print("understood")
        tello.flip_forward()  
        time.sleep(2)

tello.land()