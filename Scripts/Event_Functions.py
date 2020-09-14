from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
try:
    import RPi.GPIO as GPIO #incase we are in test mode
except: 
    print('could not import RPi.GPIO')

#to do, add the option for an always on relay

class EventFunctions():
    """A class which contains the function handling for the GUI EventFunctions"""
    def __init__(self):pass

    #update raw temp readings on the connections tab
    def updateReadings(self):
        for probe in self.parameters.probes.keys():
            for count, actor in enumerate(self.parameters.probes[probe]['actors']):
                if not self.parameters.probes[probe]['readings']:
                    text = 'none'
                else:
                    text = str(self.parameters.probes[probe]['readings'][count])
                try:
                    self.parameters.connectionsGUI['actorDict'][actor]['QLabelReading']['widget'].setText(text)
                except KeyError:pass
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise
            for hw in self.parameters.tempHardware:
                self.parameters.brewGUI[hw]['object'].updateTempLabel()





