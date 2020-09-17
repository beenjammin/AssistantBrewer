from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Database import DatabaseFunctions
from Event_Functions import EventFunctions

class MyTimer(EventFunctions):
    def __init__(self,parameters,plot):
        print('timer started')
        super().__init__()
        self.parameters = parameters
        self.plot = plot
        # self.database = DatabaseFunctions(self.parameters)
        
    def startTimer(self):   
        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.runFunctions)
        self.timer.start()
    
    def runFunctions(self):
        # self.database.readLastRow()
        self.plot.plotDialog.updatePlot()
        self.assignProbeReadings()
        for key in self.parameters.hardware:
            for function in self.parameters.brewGUI[key]['object'].updateFunctions:
                print('running function {}'.format(function))
                function() #runs function that have been appended to the update set

#        self.paramaters.settingsGUI['object'].clickedUpdateReadings()