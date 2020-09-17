#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:23:08 2020

@author: pi
"""
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except: pass
from time import sleep



class FloatSwitch():
    """a class to handle the float switch
        pin, integer - the pin on the GPIO board that float switch is connected to
        switch, boolean - by default, a signal (true) from the float switch will turn the relays with the associated hardware off and vice versa
    """
    
    def __init__(self, pin, switch=False):
        self.pin = pin
        self.switch = switch
        self.lastState = switch
        self.thisState = switch
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def poll(self):
        input_state = GPIO.input(self.pin)
        self.lastState = self.thisState
        self.thisState = input_state

    def switchState(self):
        self.poll()
        if self.thisState != self.lastState:
            if self.thisState == self.switch:
                print('switch is false and relays connected to hw can be turned on')

            else:
                print('switch is true and relays connected to hw will be turned off')
            return True
        else:
            return False

if __name__ == "__main__":
    fs = FloatSwitch(24)
    while True:
        if fs.switchState():
            print(fs.thisState)
        sleep(1)