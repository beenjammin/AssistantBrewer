# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:25:59 2020

@author: BTHRO
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json, ast

from Widget_Styles import *
from Actor_Classes import *
from Event_Functions import EventFunctions

class SettingsGUI(QMainWindow,EventFunctions):
    def __init__(self,parameters):
        print('initiating connections GUI')
        EventFunctions.__init__(self,parameters)
        QMainWindow.__init__(self,parameters=None)
        self.parameters=parameters
        # eF = EventFunctions(self.parameters)
        #Settings
        #Give user the option to set connections for relays
        VLayoutP = QVBoxLayout()  
        VLayout = QVBoxLayout()       
        relays = groupBox("Relays")
        self.headerFont = QFont()
        self.headerFont.setPointSize(14) 
        self.bodyFont = QFont()
        self.bodyFont.setPointSize(10)

        self.parameters.settingsGUI['relayDict'] = {}
        for relay in self.parameters.activePins:
            HLayout = QHBoxLayout()
            relayLabel = bodyLabel()
            relayLabel.setText('Select control for pin {}'.format(relay))
            cb = bodyComboBox()
            cb.addItems(['None']+list(self.parameters.relayHardware))
            self.parameters.settingsGUI ['relayDict'][relay]={  'QLabelRelay':{'widget':relayLabel},
                                                                'QCBRelay':{'widget':cb,'value':None}}
            
            cb.activated.connect(lambda:self.updatePins())
            HLayout.addWidget(relayLabel)
            HLayout.addWidget(cb)
            VLayout.addLayout(HLayout)
        relays.setLayout(VLayout)
        VLayoutP.addWidget(relays)
        

        #setting up connections to actors
        VLayout = QVBoxLayout()
        Actors = groupBox("Actors")
        self.parameters.settingsGUI['actorDict'] = {}
        for actor in self.parameters.actors['actors']:
            HLayout = QHBoxLayout()
            hwLabel = bodyLabel()
            hwLabel.setText('Select hardware for the {} actor'.format(actor))
            cb = bodyComboBox()
            cb.addItems(['None']+list(self.parameters.tempHardware))
            cb.activated.connect(lambda ignore, a=cb:self.updateActors(a))
            HLayout.addWidget(hwLabel)
            HLayout.addWidget(cb)
            VLayout.addLayout(HLayout)
            self.parameters.settingsGUI['actorDict'][actor]={    'QLabelActor':{'widget':hwLabel},
                                                                'QCBActor':{'widget':cb,'value':None}}

        # self.parameters.settingsGUI = {'relayDict':relayDict,'actorDict':actorDict}
        
        #load the actors
        HLayout = QHBoxLayout()    
        actorHeader = bodyLabel()
        actorHeader.setText('Actor')   
        actorHeader.setFont(self.headerFont)
        rawOutput = bodyLabel()
        rawOutput.setText('Raw Reading')   
        rawOutput.setFont(self.headerFont)
        HLayout.addWidget(actorHeader)
        HLayout.addWidget(rawOutput)
        VLayout.addLayout(HLayout)
        
        #load the raw output of each actor
        self.parameters.settingsGUI['actorReadingDict'] = {}
        for count, actor in enumerate(self.parameters.actors['actors']):
            HLayout = QHBoxLayout()  
            actorLabel = bodyLabel()
            actorLabel.setText(actor)   
            rawReading = bodyLabel()
            rawReading.setText('none')
            HLayout.addWidget(actorLabel)
            HLayout.addWidget(rawReading)
            VLayout.addLayout(HLayout)
            self.parameters.settingsGUI['actorReadingDict'][actor]={    'QLabelActor':{'widget':actorLabel},
                                                                        'QLabelReading':{'widget':rawReading,'value':'none'}
                                                                        }
        self.updateReadings()
           
        Actors.setLayout(VLayout)
        VLayoutP.addWidget(Actors)

        connections = groupBox("Connections") 
        connections.setLayout(VLayoutP)
        dock = dockable('Settings')            
        dock.addThisWidget(connections)
        dock.setCentralWidget()
        self.addDockWidget(Qt.RightDockWidgetArea,dock)
    

    def updatePins(self):
        #Could change this to just update based on combobox targeted, currently updates all for each focus event
        #reset pins
        for key, value in self.parameters.brewGUI.items():
            # print('key is {}'.format(key))
            # print('value is {}'.format(value))
            try:
                value['relayGroupBox']
                text = 'Relay pins attached --> no relays attached'
                self.parameters.brewGUI[key]['object'].pinList=[]
                self.parameters.brewGUI[key]['relayGroupBox']['QLabelCurrentPins']['widget'].setText(text)
                self.parameters.brewGUI[key]['relayGroupBox']['QLabelCurrentPins']['value']='no relays attached'
            #This hardware has no relay attached so we ignore it
            except KeyError:
                print('{} has no relay'.format(key))        
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

        #updating the brewGUI dictionary
        for key, value in self.parameters.settingsGUI['relayDict'].items():
            #set the relay pin
            pin = key
            #set the combobox in the GUI associated with the pin
            cb = value['QCBRelay']['widget']
            #get the combox value
            hw = cb.currentText()
            #update the dictionary, adding the selected combobox value for the pin
            value['QCBRelay']['value'] = hw
            #going to try and add the associate the pin with the hardware
            self.parameters.activePins[pin][1] = hw
            try:
                #check if hw is in the list, if not, display default text
                if hw in list(self.parameters.hardware):
                    self.parameters.brewGUI[hw]['object'].pinList.append(pin)
                    if self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['value'] == 'no relays attached':
                        self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['value'] = []
                        self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].setText('Relay pins attached -->')
                    #add the pin to the dictionary
                    text = self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].text()
                    self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['value'].append(pin)
                    #updating the GUI with hardware connected pins
                    text +=' {}'.format(pin)
                    self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].setText(text)                       
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise     
        

    def updateActors(self,cb):
        #runs on actor combobox change event - update associated actors
        print(cb.currentText())
        #reset text labels and actor dictionary
        self.parameters.actors['hw'] = [None]*len(self.parameters.actors['readings'])
        for key, value in self.parameters.brewGUI.items():
            # print('key is {}'.format(key))
            # print('value is {}'.format(value))
            try:
                value['tempGroupBox']
                text = 'Current temperature --> no reading'
                self.parameters.brewGUI[key]['object'].actorList=[]
                self.parameters.brewGUI[key]['tempGroupBox']['QLabelCurrentTemp']['widget'].setText(text)
            except:pass
        #loop through cbs and get parameters
        for key, value in self.parameters.settingsGUI['actorDict'].items():
            #set the relay pin
            actor = key
            #set the combobox in the GUI associated with the pin
            cb = value['QCBActor']['widget']
            #get the combox value
            hw = cb.currentText()
            #update the dictionary, adding the selected combobox value for the pin
            value['QCBActor']['value'] = hw
            self.parameters.actors['hw'][self.parameters.actors['actors'].index(actor)] = hw
            try:
                self.parameters.brewGUI[hw]['object'].actorList.append(actor)
                self.parameters.brewGUI[hw]['object'].updateTempLabel()
            except KeyError: pass
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise 
            try:
                self.parameters.plotGUI['checkBoxes'][actor]['widget'].setText(hw)
                self.parameters.plotGUI['checkBoxes'][actor]['hw']=hw
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise 

        
def main():
    app = QApplication(sys.argv)
    parameters = Parameters()
    controller = SettingsGUI(parameters)
    controller.show()
#    controller.timer.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()