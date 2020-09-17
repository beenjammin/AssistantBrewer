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

    #get the latest probe readings that from the probe dictionary and then assign these as necessary
    def assignProbeReadings(self):
        #prob
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
            #for each probe with a hardware assigned, update the temp label of the hardware and check the pin status
            for hw in self.parameters.probes['temperature']['hw']:
                if hw and hw != 'None': 
                    self.parameters.brewGUI[hw]['object'].updateTempLabel()
                    self.parameters.brewGUI[hw]['object'].checkRelayPinStatus()





