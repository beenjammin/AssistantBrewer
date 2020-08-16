# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:34:55 2020

@author: BTHRO
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from pathlib import Path

from Actor_Classes import getActors

class Parameters():
    def __init__(self):
        self.colour = 'grey' #options are green, blue, orange, yellow, grey
        

    def initialise(self):
        #{pin:last state, Parent} The pin state is boolean and each pin can only have one parent which is the hardware
        self.activePins = {17:[False,None],22:[False,None],23:[False,None],27:[False,None]}
        #For relays, we have three types [heat,cool,binary]
        #Add hardware to dictionary to populate GUI {hardware:SimpleTemp,TempTgt,TempTimer,Relays}
        self.hardware = {   
                            'HLT':{'widgets':[False,True,False,True],'relayPins':[],'actors':[]},
                            'Mash':{'widgets':[False,False,True,True],'relayPins':[],'actors':[]},
                            'Boil':{'widgets':[True,False,False,False],'relayPins':[],'actors':[]},
                            'Pump 1':{'widgets':[False,False,False,True],'relayPins':[],'actors':[]},
                            'Pump 2':{'widgets':[False,False,False,True],'relayPins':[],'actors':[]},
                         }
        
        
        #go into test mode if we cannot find any actors
        try:
            if getActors():
#                print('found {} actors'.format(len(getActors())))
                self.test = False
            else:
                self.test = True
        except:
            self.test = True
        print('Assitant to the brewer is running in {} mode'.format(['live','test'][self.test]))
             
        #add path locations
        self.cwd = Path.cwd()
        self.imageFP = str(self.cwd/'Images')
        # self.database = str(self.cwd/'BrewDay')

        self.hwList = list(self.hardware)
        self.tempHardware = set()
        self.relayHardware = set()
        #store the databases as a dictionary here
        self.database = {}
        self.database['Type'] = {'fp':'filepath','data':'entire databse as pandas dataframe','lr':'last row of databse'}
        
        if self.test:
            self.actors = {'actors':['1','2','3'],'readings':[10,25,30]}
        else:
            self.actors = {'actors':getActors(),'readings':[]}
        self.actors['hw'] = [None]*len(self.actors['readings'])
        
        self.brewGUI = {}
        self.settingsGUI = {}
        self.plotGUI = {}

        # self._DOCK_OPTS = QMainWindow.AnimatedDocks
        # self._DOCK_OPTS |= QMainWindow.AllowNestedDocks
        # self._DOCK_OPTS |= QMainWindow.AllowTabbedDocks

        self.cwd = os.getcwd()
#        print(self.cwd)
        
        self.tempDatabaseFP = ''
        self.units('temperature')
        self.plotColours = ['blue','green','red','cyan','magenta','yellow','black']

    def units(self,variable):
        if variable == 'temperature':
            return 'C'


def colourPick(colour,shade):
    colourDict = {  'green':{'light':'#a9d08e','medium':'#548235','dark':'#375623'},
                    'blue':{'light':'#9bc2e6','medium':'#2f75b5','dark':'#203764'},
                    'orange':{'light':'#f4b084','medium':'#c65911','dark':'#833c0c'},
                    'yellow':{'light':'#ffd966','medium':'#bf8f00','dark':'#806000'},
                    'grey':{'light':'#999999','medium':'#616161','dark':'#383838'}
                    }

    return colourDict[colour][shade]
        



