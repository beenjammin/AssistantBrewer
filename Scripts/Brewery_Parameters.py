# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:34:55 2020

@author: BTHRO
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os

from Actor_Classes import getActors

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
        
        #go into test mode if we cannot find any actors
        try:
            if getActors():
                print('found {} actors'.format(len(getActors())))
                self.test = True
            else:
                self.test = False
        except:
            self.test = False
        print('Assitant to the brewer is running in {} mode'.format(['test','live'][self.test]))
             
        #Dictionaries for GUI
        #user inputs as a dictionary{hardware: Status, Target tempature, Temperature tolerance, Actor}
        # self.userInputs={}
        #Actor inputs as a dictionary{HLT: Status, Target tempature, Temperature tolerance, Actor}       
        # self.actorTemps = {}
        #pins
        # self.allHardware = {}
        
        # for key in self.hardware:
        #     for hw in self.hardware[key]:
        #          self.allHardware[hw] = []
        
        self.headerFont = QFont()
        self.headerFont.setPointSize(14)     
        self.bodyFont = QFont()
        self.bodyFont.setPointSize(10)

        if self.test:
            self.actors = {'actors':['1','2','3'],'readings':[10,25,30]}
        else:
            self.actors = {'actors':getActors(),'readings':[]}
        
        self.brewGUI = {}
        self.settingsGUI = {}
        self.plotGUI = {}

        self._DOCK_OPTS = QMainWindow.AnimatedDocks
        self._DOCK_OPTS |= QMainWindow.AllowNestedDocks
        self._DOCK_OPTS |= QMainWindow.AllowTabbedDocks

        self.cwd = os.getcwd()
#        print(self.cwd)
        
        self.tempDatabaseFP = ''
        self.units()
        

    def units(self):
        self.tempUnit = 'C'


def colourPick(colour,shade):
    colourDict = {  'green':{'light':'#a9d08e','medium':'#548235','dark':'#375623'},
                    'blue':{'light':'#9bc2e6','medium':'#2f75b5','dark':'#203764'},
                    'orange':{'light':'#f4b084','medium':'#c65911','dark':'#833c0c'},
                    'yellow':{'light':'#ffd966','medium':'#bf8f00','dark':'#806000'},
                    'grey':{'light':'#999999','medium':'#616161','dark':'#383838'}
                    }

    return colourDict[colour][shade]
        



