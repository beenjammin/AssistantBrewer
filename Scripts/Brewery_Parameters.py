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
from datetime import date



class Parameters():
    def __init__(self):
        self.colour = 'grey' #options are green, blue, orange, yellow, grey
        

    def initialise(self):
        #{pin:last state, Parent} The pin state is boolean and each pin can only have one parent which is the hardware
        # Each pin should have its own class
        self.relayPins = {'17':[False,None],'18':[False,None],'23':[False,None],'22':[False,None]}
        self.floatPins = {'24':[False,None]}
        self.pins = {   'relay':list(self.relayPins.keys()),
                        'floatSwitch':list(self.floatPins.keys())
                    }

        #For relays, we have three types [heat,cool,binary]
        #Add hardware to dictionary to populate GUI {hardware:SimpleTemp,TempTgt,TempTimer,Relays}
        #not sure if I use the relayPins or actors, think it is covered by the class
        self.hardware = {   
                            'HLT':{'widgets':[False,True,False,True],'relayPins':[],'actors':[]},
                            'Mash':{'widgets':[False,False,True,True],'relayPins':[],'actors':[]},
                            'Boil':{'widgets':[True,False,False,False],'relayPins':[],'actors':[]},
                            'Pump 1':{'widgets':[False,False,False,True],'relayPins':[],'actors':[]},
                            'Pump 2':{'widgets':[False,False,False,True],'relayPins':[],'actors':[]},
                         }
        self.test = True
        # except:
        #     self.test = True
        # print('Assitant to the brewer is running in {} mode'.format(['live','test'][self.test]))
             
        #add path locations
        self.cwd = Path.cwd()
        self.imageFP = str(self.cwd/'Images')
        name = 'brew_'+str(date.today()).replace('-','_')
        self.brewDayFP = str(Path(self.cwd).parents[0]/'brewDay'/name)
        self.configFP = str(Path(self.cwd).parents[0]/'configFiles')
        #if folder does not already exist for todays brew then create it
        Path(self.brewDayFP).mkdir(parents=True, exist_ok=True)
        Path(self.configFP).mkdir(parents=True, exist_ok=True)

        # self.database = str(self.cwd/'BrewDay')

        self.hwList = list(self.hardware)
        self.tempHardware = set()
        self.relayHardware = set()

        #store the databases as a dictionary here - probs get rid of this and assign it to the database class
        self.database = {}
        self.database['Type'] = {'fp':'filepath','data':'entire databse as pandas dataframe','lr':'last row of databse'}
       
        #dictionary which determines the address of the I2C sensor (Atlas only at the moment). Name of the keys MUST match the name of the keys in the probes dict
        self.I2C = {'temperature' : '102', 
                    'ph' : '99',
                    }
        self.probes = {}
        #initalise probe dictionary,pobeType: {probe name, last reading, hardware attached to NOT USED!!, protocol}       
        self.probes['temperature']= {   'fp':'somefp',
                                        'databaseClass':object,
                                        'actors':[],
                                        'readings':[],
                                        'hw':[],
                                        'protocol':[],
                                        'probeClass':[],
                                        'plotLabels':{  'title': 'Temperature',
                                                        'yLabel': 'Temp (°{})'.format(self.units('temperature'))
                                                        }
                                        }

        self.probes['ph'] = {           'fp':'somefp',
                                        'databaseClass':object,
                                        'actors':[],
                                        'readings':[],
                                        'hw':[],
                                        'protocol':[],
                                        'probeClass':[],
                                        'plotLabels':{  'title': 'PH',
                                                        'yLabel': 'PH'
                                                        }
                                        }
        #a list of all actors
        self.allActors = []
        #initialise GUI dicts        
        self.mainWindows = {}
        self.brewGUI = {}
        self.connectionsGUI = {}
        self.settingsGUI = {}
        self.plotGUI = {}

        #adjust pH based on temp
        self.phTempAdjust = True
        # self._DOCK_OPTS = QMainWindow.AnimatedDocks
        # self._DOCK_OPTS |= QMainWindow.AllowNestedDocks
        # self._DOCK_OPTS |= QMainWindow.AllowTabbedDocks

        self.cwd = os.getcwd()
#        print(self.cwd)
        self.tempDatabaseFP = ''
        self.units('temperature')
        self.colours = ['green','blue','orange','yellow','grey']
        self.plotColours = ['blue','green','red','cyan','magenta','yellow','black']

        self.defaults()


    def units(self,variable):
        if variable == 'temperature':
            return 'C'

    def defaults(self):
        self.tempTol = 1


def colourPick(colour,shade):
    colourDict = {  'green':{'light':'#a9d08e','medium':'#548235','dark':'#375623','button_on':'#de203f','button_off':'#94c925'},
                    'blue':{'light':'#9bc2e6','medium':'#2f75b5','dark':'#203764','button_on':'#de203f','button_off':'#94c925'},
                    'orange':{'light':'#f4b084','medium':'#c65911','dark':'#833c0c','button_on':'#de203f','button_off':'#94c925'},
                    'yellow':{'light':'#ffd966','medium':'#bf8f00','dark':'#806000','button_on':'#de203f','button_off':'#94c925'},
                    'grey':{'light':'#999999','medium':'#616161','medium-dark':'#4d4d4d','dark':'#383838', 'darker': '#1a1a1a','black':'#000000','button_on':'#de203f','button_off':'#94c925'}
                    }

    return colourDict[colour][shade]
        



