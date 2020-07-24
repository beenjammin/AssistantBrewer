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
        #Add hardware to dictionary to populate GUI     
        self.hardware = {'tempHardware':['HLT','Mash','Boil'],
                         'otherHardware':['Pump 1','Pump 2']}
        self.colour = 'grey'
        # self.colours = {'black':'#000000','grey1':'#383838','grey2':'#616161','grey3':'#999999','white':'#ffffff','darkGreen':'#33524c'}
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
        
        self.relayComboBoxes = []
        self.actorComboBoxes = []
        self.actors = ['1','2','3']#getActors()
        
        #Actor inputs as a dictionary{hardware: tgtTemp, tgtTolerance, tempReading, on/off switch,}
        self.hardwareDict={}

        self._DOCK_OPTS = QMainWindow.AnimatedDocks
        self._DOCK_OPTS |= QMainWindow.AllowNestedDocks
        self._DOCK_OPTS |= QMainWindow.AllowTabbedDocks
        



