import sys
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QMainWindow
from PyQt5 import QtCore
from PyQt5.QtCore import (Qt, pyqtSignal)
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from Database import databaseManager
from Widget_Styles import *

class PlotGUI(QMainWindow):
    def __init__(self,parameters):
        print('initiating plot GUI')
        super().__init__()
        self.parameters = parameters
        dock = dockable('Plotting Probes', objectName = 'plotTab')
        self.plotDialog = PlotWindow(self.parameters)
        dock.addThisWidget(self.plotDialog)
        dock.setCentralWidget()
        self.addDockWidget(Qt.RightDockWidgetArea,dock)


class PlotWindow(QDialog):
    def __init__(self, parameters, parent=None):
        super().__init__()
        self.parameters = parameters
        self._want_to_close = False
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #the probes that should be plotted on each axis
        self.primaryAxis = None
        self.secondaryAxis = None
        #the series to show on the plot - maintained by the checkboxes
        self.plotSeries = []
        #layout for the checkboxes
        self.cbLayout = QHBoxLayout()
        #set the dictionary for checkboxes
        self.parameters.plotGUI['checkBoxes']={}

    def closeEvent(self, evnt):
        if self._want_to_close:
            super(PlotWindow, self).closeEvent(evnt)
        else:
            evnt.ignore()
            super(PlotWindow, self).closeEvent(evnt)
            print('exit 2')         
            userList = ['plot']
            self.closePlotWindow.emit(userList)
            print('exit 1')

            self.setWindowState(QtCore.Qt.WindowMinimized)

    def plot(self):
        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))
        self.ax1 = self.canvas.figure.subplots()
        self.ax2 = self.ax1.twinx()
        self.plotFormat()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.axisPlotCbs()
        self.comboBoxChanged()
        # self.addCheckBoxes()
        self.setLayout(self.layout)

        self.canvas.draw()

    def resetPlot(self,axis):
        axis.clear()
        axis.axis('off')

    def updatePlot(self):
        self.plotCount = 0
        self.plotAxis(self.ax1,probe=self.primaryAxis)
        self.plotAxis(self.ax2,probe=self.secondaryAxis)
        self.plotFormat()
        self.canvas.draw()

    def plotAxis(self,axis,probe=None):
        self.resetPlot(axis)
        #print(self.df)
        colour = self.parameters.plotColours
        #set the linestle
        ls = '-' if axis == self.ax1 else '--'
        #reset the plot window
        if probe:
            #update the database and get data as datframe
            self.parameters.probes[probe]['databaseClass'].updateDatabase()
            df = self.parameters.probes[probe]['databaseClass'].data
            dfHeader = self.parameters.probes[probe]['databaseClass'].header 
            labelList = []
            #check if hardware has been assigned, if not use the header in the database
            for count, label in enumerate(self.parameters.probes[probe]['hw']):
                if label:
                    labelList.append(label)
                else:
                    labelList.append(dfHeader[count+1])
            # this plots our series from the dataframe
            for count, col in enumerate(dfHeader[1:]):
                if col in self.plotSeries:
                    axis.plot(dfHeader[0], col, data=df, label=labelList[count], color=colour[self.plotCount],linestyle=ls)
                    self.plotCount += 1
            axis.axis('on')

    def plotFormat(self):
        #plots the format based on the axis present
        colour = self.parameters.colour
        self.canvas.figure.patch.set_facecolor(colourPick(colour,'light'))

        title = ''
        count = 0
        # print ('p axis is {} and s is {}'.format(self.primaryAxis,self.secondaryAxis))
        for axis, probe in zip([self.ax1, self.ax2],[self.primaryAxis,self.secondaryAxis]):
            # print('axis is and probe is {}'.format(axis,probe))
        #test if anything has been assigned
            if probe:
                # print('probe to format is {}'.format(probe))
                count +=1
                yLabel = self.parameters.probes[probe]['plotLabels']['yLabel']
                axis.tick_params(color=colourPick(colour,'dark'))
                axis.set_ylabel(yLabel, color=colourPick(colour,'dark'),fontweight='bold')
                if count == 2:
                    title += 'and '
                title += self.parameters.probes[probe]['plotLabels']['title']+' '
        title += 'probes'

        #We want to set the formatting for the active axis but only once if both are present
        if self.primaryAxis:
            self.ax1.set_xlabel('Time', color=colourPick(colour,'dark'),fontweight='bold')
            self.ax1.set_facecolor(colourPick(colour,'dark'))
            self.ax1.set_title(label = title, color=colourPick(colour,'dark'),fontweight='bold')
            self.ax1.grid(b=True, which='major', color=colourPick(colour,'light'), linestyle='-')
            self.ax1.legend(loc='upper left')
        elif self.secondaryAxis:
            self.ax2.set_xlabel('Time', color=colourPick(colour,'dark'),fontweight='bold')
            self.ax2.set_facecolor(colourPick(colour,'dark'))
            self.ax2.set_title(label = title, color=colourPick(colour,'dark'),fontweight='bold')

        if self.secondaryAxis:
            self.ax2.legend(loc='upper right')
            self.ax2.grid(b=True, which='major', color=colourPick(colour,'light'), linestyle='--')

    def axisPlotCbs(self):
        #function to generate checkbox options for what we plot on which axis.  Should be set to what is currently plot and update based on plot date
        hlayout = QHBoxLayout()
        pLabel = bodyLabel('Select plot for the primary axis')
        pCB = bodyComboBox()
        pCB.addItems([None]+list(self.parameters.probes.keys()))
        pCB.activated.connect(lambda:self.comboBoxChanged())
        #set the combox so we have something to plot
        pCB.setCurrentIndex(1)
        hlayout.addWidget(pLabel)
        hlayout.addWidget(pCB)
        sLabel = bodyLabel('Select plot for the secondary axis')
        sCB = bodyComboBox()
        sCB.addItems([None]+list(self.parameters.probes.keys()))
        sCB.activated.connect(lambda:self.comboBoxChanged())
        hlayout.addWidget(sLabel)
        hlayout.addWidget(sCB)
        self.layout.addLayout(hlayout)
        self.parameters.plotGUI['primaryCB'] = pCB
        self.parameters.plotGUI['secondaryCB'] = sCB

    def comboBoxChanged(self):
        self.primaryAxis = self.parameters.plotGUI['primaryCB'].currentText()
        self.secondaryAxis = self.parameters.plotGUI['secondaryCB'].currentText()
        #reset the checkbox layout and the series to be plotted
        self.clearLayout(self.cbLayout)
        self.plotSeries=['Time']
        for axis, probe in zip([self.ax1, self.ax2],[self.primaryAxis,self.secondaryAxis]):
            if probe:
                #adding checkboxes, one for each series
                 self.addCheckBoxes(probe, self.parameters.probes[probe]['probes'])
        self.updatePlot()
        #some funciton to update checkboxes

    def addCheckBoxes(self, probe, probeList):
        #function to add check boxes for the primary and secondary axis
        #reset the plot series
        
        lbl = bodyLabel('{} series -->'.format(probe))
        self.cbLayout.addWidget(lbl)
        for actor in probeList:
            #try and set the check box to the last known state, if no info, set to true
            try:
                currentState = self.parameters.plotGUI['checkBoxes'][actor]['state']
                label = self.parameters.plotGUI['checkBoxes'][actor]['hw']         
            except KeyError:
                currentState = True
                label = actor
            except:
                print("Unexpected error:", sys.exc_info()[0])
            cb = bodyCheckBox(label)
            cb.setChecked(currentState)
            cb.stateChanged.connect(lambda ignore, a=actor:self.btnState(a))
            if currentState:
                self.plotSeries.append(actor)
            self.cbLayout.addWidget(cb)
            self.parameters.plotGUI['checkBoxes'][actor]={'hw':actor,'widget':cb,'state':currentState}

        self.layout.addLayout(self.cbLayout)

    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

    def btnState(self,actor):
        if actor in self.plotSeries:
            self.plotSeries.remove(actor)
        else:
            self.plotSeries.append(actor)
        #updates the plot series list based on if checkboxes are selected or not
        self.updatePlot()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main =  PlotProbe('Temperatures')
    main.plot()
    main.show()
    sys.exit(app.exec_())