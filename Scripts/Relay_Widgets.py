import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json, ast
from Event_Functions import EventFunctions
from Widget_Styles import *

class RelayWidgets(EventFunctions):
    def __init__(self):
        super().__init__()

    def __updateRelayHardware(self):
        try:
            self.parameters.relayHardware
        except:
            self.parameters.relayHardware = set()
        self.parameters.relayHardware.add(self.name)

    #adds basic relay to the GUI
    def addRelay(self,dock):
        self.__updateRelayHardware()
        self.hwStatus['relay']=False
        gb = groupBox('Relay')
        # VLayout = QVBoxLayout()
        HLayout = QHBoxLayout()
        currentPins = bodyLabel('Relay pins attached --> no relays attached')
        HLayout.addWidget(currentPins)       
        switch = bodyButton()
        switch.setText(self.name+' - Off')
        switch.setCheckable(True)
        switch.clicked.connect(lambda ignore, a=self.name:self.whichbtn(a))
        HLayout.addWidget(switch)
        # VLayout.addLayout(HLayout)

        gb.setLayout(HLayout)          
        dock.addThisWidget(gb)

        #update widget dictionary with all widgets we created
        relayGroupBox = {'widget':gb,
                        'QLabelCurrentPins':{'widget':currentPins,'value':'no relays attached'},
                        'QPushButton':{'widget':switch,'value':False}
                        }
        self.parameters.brewGUI[self.name]['relayGroupBox'] = relayGroupBox

    #handles the QPushButton click event
    def whichbtn(self,hardware):
        b = self.parameters.brewGUI[hardware]['relayGroupBox']['QPushButton']['widget']
        hw = b.text()[:b.text().find('-')-1]
        if b.isChecked():
            b.setText(b.text()[:-6]+' - On')
            switch = True
        else:
            b.setText(b.text()[:-5]+' - Off')
            switch = False
        #updating the status dictionary
        self.parameters.brewGUI[hw]['object'].hwStatus['relay']=switch
        print('Trying to switch {}{}'.format(hw,b.text()[b.text().find('-')+1:]))
        #check to see if any pins are connected to the hardware
        pins = self.parameters.brewGUI[hw]['object'].pinList
        print(pins)
        if not pins:
            print('Warning, no relays connected')
        else:
            self.checkPinStatus(pins)
