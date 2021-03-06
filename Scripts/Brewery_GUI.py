import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json, ast
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

try:
    import RPi.GPIO as GPIO #incase we are in test mode
except: 
    print('could not import RPi.GPIO')

from Widget_Styles import *
from Event_Functions import EventFunctions
from Temperature_Widgets import TemperatureWidgets
from Relay_Widgets import RelayWidgets
from Save_Load_Config import Config

class BreweryGUI(QMainWindow):
    def __init__(self,parameters):
        print('initiating brewery GUI')
        super().__init__()

        self.parameters = parameters
        # self.parameters.colour = 'blue'
        # self.setDockOptions(self.parameters._DOCK_OPTS)
        VLayoutP = QVBoxLayout()#Delete?
        
        #loop over hardware and set up based on booleans in list
        for key, value in self.parameters.hardware.items():
            self.parameters.brewGUI[key] = {}
            self.parameters.brewGUI[key]['object'] = Hardware(key,self.parameters)
            print (key)
            #create a dockable widget which will contain child widgets only if at least one value
            if any(value):
                self.dock = dockable(key,objectName = 'childTab')
                self.parameters.brewGUI[key]['dockwidget']=[self.dock]

            #check if we are adding simple temperature functionality to the hardware
            if value['widgets'][0]: 
                self.parameters.brewGUI[key]['object'].addSimpleTemp(self.dock)
            print ('added temptgt0')
            #check if we are adding target temperature functionality to the hardware
            if value['widgets'][1]:
                self.parameters.brewGUI[key]['object'].addTempTgt(self.dock)

            print ('added temptgt1')
            #check if we are adding temperature timer functionality to the hardware
            if value['widgets'][2]:
                self.parameters.brewGUI[key]['object'].addTempTimer(self.dock)
            print ('added temptgt2')
            #check if we are adding relay functionality to the hardware
            if value['widgets'][3]:
                self.parameters.brewGUI[key]['object'].addRelay(self.dock)
            print ('added temptgt3')
            #add and set the widget
            self.dock.setCentralWidget()
            self.addDockWidget(Qt.RightDockWidgetArea,self.dock)
        # print (self.parameters.brewGUI)


    #adding the temperature funcitonality
    #multiple probes connected to one hardware item - use min, max or average of readings


#a super class that will inherit all properties of probes and relays
class Hardware(TemperatureWidgets,RelayWidgets,Config):
    def __init__(self,name,parameters):
        self.parameters = parameters
        super().__init__()
        self.name = name
        #list of actors connected to hw and most recent reading {Type: {actors:[],reading:}}
        # self.probes = {a:{'name':{'currentValue':None},'allCurrentValues':[]} for a in self.parameters.probes.keys()}

        #list of actors connected to hw and most recent reading {Type: {actors:[],reading:}}
        self.probes = {a:{'actors':[]} for a in self.parameters.probes.keys()}
        #list of pins connected to hw (relays and float switches)
        self.pinList = {'relay':[],
                        'floatSwitch':[]}
        #staus of hw controls (boolean)
        self.hwStatus={}
        #functions to be updated
        self.updateFunctions = set()
        #the curreny status of the hardware, currently can only have one status - could update this
        self.status = False
        #the last state of the relay - need this for temp tolerances
        self.lastRelayState = False
        #controls for switching the relay on and off
        self.relayControl = {}


    #function to update the temp label associated with the hardware class
    def updateTempLabel(self):
        self.getTemp()
        if self.temp:
            text = self.parameters.brewGUI[self.name]['tempGroupBox']['QLabelCurrentTemp']['widget'].text()
            text = text[:text.find('-->')+4]+'{}'.format(round(self.temp,1))
            self.parameters.brewGUI[self.name]['tempGroupBox']['QLabelCurrentTemp']['widget'].setText(text)
        else:
            text = 'Current temperature --> no reading'
            self.parameters.brewGUI[self.name]['tempGroupBox']['QLabelCurrentTemp']['widget'].setText(text)

    #function to determine if relay connected to HW should be switched on - it will always be switched off if an off signal is recieved.
    def updateStatus(self):
        if 'TempTgt' in self.hwStatus:
            self.updateTempTgtStatus()
        self.status=all(list(self.hwStatus.values()))
        print(self.hwStatus)
        self.setPinStatus()

    #function to set status of pins
    def setPinStatus(self):
        for pin in self.pinList['relay']:
            self.parameters.relayPins[pin][0] = self.status




def main():   
    app = QApplication(sys.argv)
    parameters = Parameters()
    controller = BreweryGUI(parameters)
    controller.show()
#    controller.timer.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()