import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json, ast
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from Widget_Styles import *


class TemperatureWidgets():
    def __init__(self):
        #the temperature of the actor(s) connected to the hardware
        self.temp = ''
        #if more than one probe connected to the actor, specifies the methodology for taking the reading (min, max, default is average)
        self.tempCalc = 'average'

    #update the set of hardware with temperature properties
    def __updateTempHardware(self):
        try:
            self.parameters.tempHardware
        except:
            self.parameters.tempHardware = set()
        self.parameters.tempHardware.add(self.name)

    #get the temperature of the hardware by going to the select actor and 
    def getTemp(self):
        if self.actorList['temperature']:
            indices = [self.parameters.probes['temperature']['actors'].index(b) for b in self.actorList['temperature']]
            temps = [float(self.parameters.probes['temperature']['readings'][b]) for b in indices]
#            print('temps for {} is {}'.format(self.name,temps))
            self.tempCalc = 'max'
            if self.tempCalc == 'max':
                self.temp = max(temps)
                print(self.temp)
            elif self.tempCalc == 'min':
                self.temp = min(temps)
            else:
                self.temp = average(temps)
        else:
            self.temp = None

    #initialise the widget by creating a groupbox with a vertical layout 
    def __initialiseTempWidget(self, dock):
        VLayout = QVBoxLayout()
        gb = groupBox('Temperature')
        gb.setLayout(VLayout) 
        dock.addThisWidget(gb)
        tempGroupBox = {'widget':gb,
                        'layout':VLayout,
                        }
        self.parameters.brewGUI[self.name]['tempGroupBox'] = tempGroupBox

    # add a simple temp readout widget to the GUI
    def __simpleTempReadout(self):
        #should also connect this to the live update function
        layout = self.parameters.brewGUI[self.name]['tempGroupBox']['layout']
        currentTemp = bodyLabel('Current temperature --> no reading')
        layout.addWidget(currentTemp)
        self.parameters.brewGUI[self.name]['tempGroupBox']['QLabelCurrentTemp'] = {'widget':currentTemp,'value':'no reading'}

    # add a widget which lets user set the target temperature of the hardware and associated tolerance
    def __tgtTempWithTolerance(self):
        layout = self.parameters.brewGUI[self.name]['tempGroupBox']['layout']

        HLayout = QHBoxLayout()
        tgtTemp = bodyLabel('Target temperature:')
        tgtLineTemp = bodyLineEdit()
        HLayout.addWidget(tgtTemp)
        HLayout.addWidget(tgtLineTemp)
        layout.addLayout(HLayout)

        HLayout = QHBoxLayout()
        tempTol = bodyLabel('Temperature tolerance:')
        tempLineTolerance = bodyLineEdit()
        HLayout.addWidget(tempTol)
        HLayout.addWidget(tempLineTolerance)
        layout.addLayout(HLayout)

        newItems = {    'QLineEditTgtTemp':{'widget':tgtLineTemp,'value':None},
                        'QLineEditTempTol':{'widget':tempLineTolerance,'value':None},
                        'QLabelTgtTemp':{'widget':tgtTemp},
                        'QLabelTempTol':{'widget':tempTol}
                    }
        self.parameters.brewGUI[self.name]['tempGroupBox'].update(newItems)


    def addSimpleTemp(self, dock):
        self.__updateTempHardware()
        self.__initialiseTempWidget(dock)
        self.__simpleTempReadout()
   
    # add a target temperature widget to the GUI
    def addTempTgt(self,dock):
        self.hwStatus['TempTgt']=False
        self.__updateTempHardware()
        self.__initialiseTempWidget(dock)
        self.__tgtTempWithTolerance()
        self.__simpleTempReadout()
        
    #update the status (on/off) for the TempTgt widget
    def updateTempTgtStatus(self):
        try:
            tgtTemp = float(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTemp']['widget'].text())
            tempTol = float(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTempTol']['widget'].text())
            currentTemp = float(self.temp)
            pinStatus = all([self.parameters.relayPins[a[0]] for a in self.pinList['relay']])
            if currentTemp < tgtTemp - tempTol:
                self.hwStatus['TempTgt']=True
            elif currentTemp < tgtTemp and pinStatus:
                self.hwStatus['TempTgt']=True
            else:
                self.hwStatus['TempTgt']=False
        except ValueError: pass
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise 
 
     # add a temperature timer widget to the GUI    
    def addTempTimer(self,dock):
        self.__updateTempHardware()
        #initialise set-up, need to add checkboxes, drop down list for selecting profiles etc
        #number of additional points
        self.plotPoints = 0
        #flat line the temps if true, gradients if false
        self.holdTemps = True
        #if True, only count the time if the temp is within tolerance of target
        self.warmUp = False
        #the tolerance for the target temp
        self.tempTolerance = 5
        #add the connected live temp
        self.plotLiveTemp = False
        self.populateWidgets(dock)
        self.initialisePlot()
        self.addToolbar()
        self.valueChange()

    def initialisePlot(self):
        self.dlg = QDialog()
        self.dlg.canvas = FigureCanvas(Figure(figsize=(4, 4)))
        self.ax = self.dlg.canvas.figure.subplots()
        VLayout = self.parameters.brewGUI[self.name]['tempGroupBox']['layout']
        VLayout.addWidget(self.dlg.canvas)

    def widgetChange(self):
        #function to define what happens when there is a widget change
        self.populateWidgets()
        self.initialisePlot()
        self.addToolbar()
        self.valueChange()

    def valueChange(self):
        #function to define what happens when there is a value change
        s1, s2 = self.updateTgtTempSeries()
        if self.plotLiveTemp:
            s3 = self.updateTempReadingSeries(self.actorList['temperature'])
        else:
            s3 = None
        self.updatePlot(s1, s2, s3)
 
    #returns the series of actors passed
    def updateTempReadingSeries(self,actor):
        if not actor:
            print('no actors attached to {} - check your connections tab'.format(self.name))
        headers = ['Time']
        headers += actor
        liveTempSeries = self.parameters.database['temperature'].loc[:,headers]
        return liveTempSeries
   
    def updateTgtTempSeries(self):
    #updates the plot but should change this so it takes the plots as an argument 
    #get temps from GUI
        times = [float(a) if a or a == 0 else None for a in self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTimes']['values']]
        temps = [float(a) if a or a == 0 else None for a in self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTemps']['values']]
        # print (times)
        # print ('dict list is {}'.format(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTimes']['values']))
        tl = []
        tl2 = []

        for count, time in enumerate(times):
            #if both values are present
            if isinstance(temps[count],int) or isinstance(temps[count],float):
                if isinstance(times[count],int) or isinstance(times[count],float):     
                    tl.append(times[count])
                    tl2.append(temps[count])
  
        if tl:
            #if we are holding temps we need to add indices for plotting
            if self.holdTemps:
                plotTime = [tl[0]]
                plotTemp = [tl2[0]]
                for count in range(len(tl)):
                    #check to make sure it is not the first indice
                    if count is not 0:
                        #append a value just before
                        plotTime += [tl[count]-0.01,tl[count]]
                        plotTemp += [tl2[count-1],tl2[count]]
            else:
                plotTime = tl
                plotTemp = tl2

            # print ('x axis is {}'.format(plotTime))
            # print ('y axis is {}'.format(plotTemp))
            try:
                tempTolPlot = [[a - self.tempTolerance for a in plotTemp],[a + self.tempTolerance for a in plotTemp]]
            except TypeError:
                tempTolPlot = None
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

            return [plotTime, plotTemp], tempTolPlot

    def updatePlot(self,tempTgtSeries=None,tempTolPlot=None,liveTempSeries=None):
        #update the plot, takes series as inputs
        #tempTgtSeries is a 2 by n list (x and y)
        #tempTolPlot is a 2 by n list (y+tol and y-tol)
        #liveTempSeries is an m by n dataframe (x and m'y series)
            print('updating plot')
            self.ax.clear()
            colour = self.parameters.plotColours
            #check we have a list to plots
            if tempTgtSeries[0] and tempTgtSeries[1]:
                self.ax.plot(tempTgtSeries[0], tempTgtSeries[1], lw=2, label='Temperature Target', color='blue')
            if self.tempTolerance:
                self.ax.fill_between(tempTgtSeries[0], tempTolPlot[0], tempTolPlot[1], facecolor='blue', alpha=0.35,label='Tolerance')
            if self.plotLiveTemp:
                headers = liveTempSeries.columns.values.tolist()
                for count, actor in enumerate(headers[1:]):
                    print('adding {}'.format(actor))
                    self.ax.plot(headers[0], actor, data=liveTempSeries, label=actor, color=colour[count])
            self.formatPlotTemp()
            self.dlg.canvas.draw()
    
    def formatPlotTemp(self):
        colour = self.parameters.colour
        self.ax.set_xlabel('Time', color=colourPick(colour,'dark'),fontweight='bold')
        self.ax.set_ylabel('Temp (°{}) for {}'.format(self.parameters.units('temperature'),self.name), color=colourPick(colour,'dark'),fontweight='bold')
        # self.ax.set_title(label = 'Temperature probes', color=colourPick(colour,'dark'),fontweight='bold')
        self.ax.legend(loc='upper left')
        self.ax.set_facecolor(colourPick(colour,'dark'))
        self.dlg.canvas.figure.patch.set_facecolor(colourPick(colour,'light'))
        self.ax.tick_params(color=colourPick(colour,'dark'))
        self.ax.grid(b=True, which='major', color=colourPick(colour,'light'), linestyle='-')

    def addDataPoint(self,widget):
        #adds data point based on click location
        indice = self.parameters.brewGUI[self.name]['tempGroupBox']['QButtonAdd']['widgets'].index(widget)
        ls_1 = self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTimes']['values']
        ls_2 = self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTemps']['values']
        # print('ls_2 is {}'.format(ls_2))
        timeInterp = float(ls_1[indice-1])/2 + float(ls_1[indice])/2
        tempInterp = float(ls_2[indice-1])/2 + float(ls_2[indice])/2
        self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTimes']['values'].insert(indice,timeInterp)
        self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTemps']['values'].insert(indice,tempInterp)
        self.clearLayout(self.parameters.brewGUI[self.name]['tempGroupBox']['layout'])
        self.plotPoints += 1
        self.widgetChange()
        
    def removeDataPoint(self,widget):
        #removes data point based on click location
        indice = self.parameters.brewGUI[self.name]['tempGroupBox']['QButtonRemove']['widgets'].index(widget)
        self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTimes']['values'].pop(indice)
        self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTemps']['values'].pop(indice)
        self.clearLayout(self.parameters.brewGUI[self.name]['tempGroupBox']['layout'])
        self.plotPoints -= 1
        self.widgetChange()

    def updateDict(self):
        #function to track what numbers the user has selected
        ls_1, ls_2, = [], []
        for count in range(self.plotPoints+2):
            ls_1.append(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTimes']['widgets'][count].value())
            ls_2.append(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTemps']['widgets'][count].value())
        self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTimes']['values'] = ls_1
        self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTemps']['values'] = ls_2
        self.valueChange()

    def populateWidgets(self,dock=None):
        #initialise, this always happens
        addRemoveBtnSize = QSize(15, 15)
        try:
            gb = self.parameters.brewGUI[self.name]['tempGroupBox']['widget']
            startTempVal = float(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTemps']['values'][0])
            endTempVal = float(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTemps']['values'][-1])
            startTimeVal = float(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTimes']['values'][0])
            endTimeVal = float(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTimes']['values'][-1])
        except KeyError:
            gb = groupBox('Temperature')
            startTempVal = 65
            endTempVal = 70
            startTimeVal = 0
            endTimeVal = 60
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        tempGroupBox = {}
        startLabel = bodyLabel('Time (min)')
        startLabel2 = bodyLabel('Temp (°{})'.format(self.parameters.units('temperature')))
        startTime = bodySpinBox()
        startTime.setValue(startTimeVal)
        startTime.valueChanged.connect(self.updateDict)
        startTemp = bodySpinBox()
        startTemp.setValue(startTempVal)

        startTemp.valueChanged.connect(self.updateDict)

        HLayout = QHBoxLayout()
        VLayout = QVBoxLayout()
        VLayout.addWidget(startLabel)
        VLayout.addWidget(startLabel2)
        HLayout.addLayout(VLayout)

        VLayout = QVBoxLayout()
        VLayout.addWidget(startTime)
        VLayout.addWidget(startTemp)
        HLayout.addLayout(VLayout)

        tempGroupBox = {'widget':gb,
                        'QLineEditTgtTimes':{'widgets':[startTime],'values':[startTimeVal]},
                        'QLineEditTgtTemps':{'widgets':[startTemp],'values':[startTempVal]},
                        'QButtonAdd':{'widgets':[None]},
                        'QButtonRemove':{'widgets':[None]},
                        }


        #now we add the intermediary steps
        for count in range(self.plotPoints):
            VLayout = QVBoxLayout()
            addButton = bodyButton('+')
            addButton.setFixedSize(addRemoveBtnSize)
            addButton.clicked.connect(lambda ignore, a=addButton:self.addDataPoint(a))
            removeButton = bodyButton('-')
            removeButton.clicked.connect(lambda ignore, a=removeButton:self.removeDataPoint(a))
            removeButton.setFixedSize(addRemoveBtnSize)
            VLayout.addWidget(addButton)
            VLayout.addWidget(removeButton)
            HLayout.addLayout(VLayout)
            #see if we have value already
            try:
                tempVal = float(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTemps']['values'][count+1])
                timeVal = float(self.parameters.brewGUI[self.name]['tempGroupBox']['QLineEditTgtTimes']['values'][count+1])
            #if we don't lets set to empty
            except KeyError:
                tempVal = None
                timeVal = None
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

            VLayout = QVBoxLayout()
            thisTime = bodySpinBox()
            thisTime.setValue(timeVal)
            thisTime.valueChanged.connect(self.updateDict)
            thisTemp = bodySpinBox()
            thisTemp.setValue(tempVal)
            thisTemp.valueChanged.connect(self.updateDict)
            VLayout.addWidget(thisTime)
            VLayout.addWidget(thisTemp)
            HLayout.addLayout(VLayout)

            tempGroupBox['QLineEditTgtTimes']['widgets'].append(thisTime)
            tempGroupBox['QLineEditTgtTemps']['widgets'].append(thisTemp)
            tempGroupBox['QLineEditTgtTimes']['values'].append(timeVal)
            tempGroupBox['QLineEditTgtTemps']['values'].append(tempVal)
            tempGroupBox['QButtonAdd']['widgets'].append(addButton)
            tempGroupBox['QButtonRemove']['widgets'].append(removeButton)

        #add final buttons
        addButton = bodyButton('+')
        addButton.setFixedSize(addRemoveBtnSize)
        addButton.clicked.connect(lambda ignore, a=addButton:self.addDataPoint(addButton))
        endTime = bodySpinBox()
        endTime.setValue(endTimeVal)
        endTime.valueChanged.connect(self.updateDict)
        endTemp = bodySpinBox()
        endTemp.setValue(endTempVal)
        endTemp.valueChanged.connect(self.updateDict)


        VLayout = QVBoxLayout()
        VLayout.addWidget(addButton)
        HLayout.addLayout(VLayout)
        VLayout = QVBoxLayout()
        VLayout.addWidget(endTime)
        VLayout.addWidget(endTemp)
        HLayout.addLayout(VLayout)  

        try:
            VLayout = self.parameters.brewGUI[self.name]['tempGroupBox']['layout']
        except:
            VLayout = QVBoxLayout()
        
        currentTemp = bodyLabel('Current temperature --> no reading')
        VLayout.addLayout(HLayout)
        VLayout.addWidget(currentTemp)
        tempGroupBox['QButtonAdd']['widgets'].append(addButton)
        tempGroupBox['QLineEditTgtTimes']['widgets'].append(endTime)
        tempGroupBox['QLineEditTgtTimes']['values'].append(endTimeVal)
        tempGroupBox['QLineEditTgtTemps']['widgets'].append(endTemp)
        tempGroupBox['QLineEditTgtTemps']['values'].append(endTempVal)
        tempGroupBox['QLabelCurrentTemp'] = {'widget':currentTemp,'values':'no reading'}
        tempGroupBox['layout'] = VLayout

        gb.setLayout(VLayout)
        try:
            self.parameters.brewGUI[self.name]['tempGroupBox']
        except:        
            dock.addThisWidget(gb)

        self.parameters.brewGUI[self.name]['tempGroupBox'] = tempGroupBox     

    def addToolbar(self):
        holdTemps = bodyCheckBox('Hold temperatures constant')
        holdTemps.setChecked(self.holdTemps)
        holdTemps.stateChanged.connect(lambda ignore, a='holdTemps':self.switchState(a))
        warmUp = bodyCheckBox('Heating time is included')
        warmUp.setChecked(self.warmUp)
        holdTemps.stateChanged.connect(lambda ignore, a='warmUp':self.switchState(a))
        plotLiveTemp = bodyCheckBox('Add live temp')
        plotLiveTemp.stateChanged.connect(lambda ignore, a='plotLiveTemp':self.switchState(a))
        plotLiveTemp.setChecked(self.plotLiveTemp)
        HLayout = QHBoxLayout()
        HLayout.addWidget(holdTemps)
        HLayout.addWidget(warmUp)
        HLayout.addWidget(plotLiveTemp)

        tempTolLbl = bodyLabel('Temperature tolerance')
        tempTolerance = bodySpinBox()
        tempTolerance.setValue(self.tempTolerance)
        tempTolerance.valueChanged.connect(self.updateTol)
        # HLayout2 = QHBoxLayout()
        HLayout.addWidget(tempTolLbl)
        HLayout.addWidget(tempTolerance)

        toolBar = {'holdTemps':holdTemps,'warmUp':warmUp,'tempTolerance':tempTolerance,'plotLiveTemp':plotLiveTemp}
        self.parameters.brewGUI[self.name]['tempGroupBox']['toolBar'] = toolBar
        self.parameters.brewGUI[self.name]['tempGroupBox']['layout'].addLayout(HLayout) 


    def switchState(self,a):
        if a == 'holdTemps':
            self.holdTemps = self.parameters.brewGUI[self.name]['tempGroupBox']['toolBar']['holdTemps'].isChecked()
        elif a == 'warmUp':
            self.warmUp = self.parameters.brewGUI[self.name]['tempGroupBox']['toolBar']['warmUp'].isChecked()
        elif a == 'plotLiveTemp':
            self.plotLiveTemp = self.parameters.brewGUI[self.name]['tempGroupBox']['toolBar']['plotLiveTemp'].isChecked()
        if self.plotLiveTemp:
            self.updateFunctions.add(self.valueChange)
            # print('updated funcitons {}'.format(self.updateFunctions))
        else:
            try:
                self.updateFunctions.remove(self.valueChange)
            except KeyError: pass
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        self.valueChange()

    def updateTol(self):
        self.tempTolerance = self.parameters.brewGUI[self.name]['tempGroupBox']['toolBar']['tempTolerance'].value()
        self.valueChange()

    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())