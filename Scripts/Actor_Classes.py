import os, csv
import glob
import time
from datetime import date
""" code modified from https://pimylifeup.com/raspberry-pi-temperature-sensor/"""

#function to return actors as a list
def getActors():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    home = '/home/pi/temperature_sensor'
    base_dir = '/sys/bus/w1/devices/'
    #Returns a list of all connected devices
    devices = [f.path for f in os.scandir(base_dir) if f.is_dir()]
    tempDevices = [x for x in devices if not 'master' in x]
    return tempDevices

#function to return the temperature of a given actor
def actor_read_raw(device_file):
    # we aer going to do something smart here to guess the device
    def read_raw(device_file):
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    lines = read_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

    
#takes a device as 
class ReadDevice():
    def __init__(self,device_file):
        self.device_file = device_file
    def read_raw(self):
        f = open(self.device_file, 'r')
        self.lines = f.readlines()
        f.close()
    def read_temp(self):
        self.read_raw()
        while self.lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            self.lines = read_raw()
        equals_pos = self.lines[1].find('t=')
        if equals_pos != -1:
            temp_string = self.lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c
