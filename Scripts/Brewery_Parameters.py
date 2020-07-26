# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:34:55 2020

@author: BTHRO
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Parameters():
    def __init__(self):
        #{pin:last state} 
        self.activePins = {17:False,22:False,23:False,27:False}
        #For relays, we have three types [heat,cool,binary]
        #Add hardware to dictionary to populate GUI {hardware:SimpleTemp,TempTgt,TempTimer,Relays}
        self.hardware = {   
                            'HLT':{'widgets':[False,True,False,True],'relayPins':[],'actors':[]},
                            'Mash':{'widgets':[False,True,False,True],'relayPins':[],'actors':[]},
                            'Boil':{'widgets':[True,False,False,False],'relayPins':[],'actors':[]},
                            'Pump 1':{'widgets':[False,False,False,True],'relayPins':[],'actors':[]},
                            'Pump 2':{'widgets':[False,False,False,True],'relayPins':[],'actors':[]},
                         }
        self.colour = 'green' #options are green, blue, orange, yellow, grey
        #Dictionaries for GUI
        #user inputs as a dictionary{hardware: Status, Target tempature, Temperature tolerance, Actor}
        self.userInputs={}
        #Actor inputs as a dictionary{HLT: Status, Target tempature, Temperature tolerance, Actor}       
        self.actorTemps = {}
        #pins
        self.allHardware = {}
        
        for key in self.hardware:
            for hw in self.hardware[key]:
                 self.allHardware[hw] = []
        
        self.headerFont = QFont()
        self.headerFont.setPointSize(14)
        
        self.bodyFont = QFont()
        self.bodyFont.setPointSize(10)
        
        self.actors = {'actors':['1','2','3'],'readings':[]}#getActors()
        
        #Actor inputs as a dictionary{hardware: tgtTemp, tgtTolerance, tempReading, on/off switch,}
        self.brewGUI = {}
        self.settingsGUI = {}

        self._DOCK_OPTS = QMainWindow.AnimatedDocks
        self._DOCK_OPTS |= QMainWindow.AllowNestedDocks
        self._DOCK_OPTS |= QMainWindow.AllowTabbedDocks
        


