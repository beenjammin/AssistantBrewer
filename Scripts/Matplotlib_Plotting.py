import sys
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import (Qt, pyqtSignal)
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

from Widget_Styles import *
from Brewery_Parameters import colourPick

class PlotWindow(QDialog):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        self._want_to_close = False
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

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
        self.ax = self.canvas.figure.subplots()
        self.count = 0
        self.updateDataFrame()


        self.plotFormat()
        self.layout = QVBoxLayout()
##        layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.addCheckBoxes()
        self.setLayout(self.layout)

        self.canvas.draw()

    def updatePlot(self):
        self.updateDataFrame()
#        print(self.df)
        colour = ['blue','green','red','cyan','magenta','yellow','black']
        self.seriesList = []
        self.ax.clear()

        # this plots our series from the dataframe
        for count,col in enumerate(self.df_columns[1:]):
            if col in self.plotSeries:
                self.seriesList.append(self.ax.plot(self.df_columns[0], col,data=self.df, label=col, color = colour[count]))
        self.plotFormat()
        self.canvas.draw()

    def addCheckBoxes(self):
        self.parameters.plotGUI['checkBoxes']={}
        hlayout = QHBoxLayout()
        for actor in self.parameters.actors['actors']:
            cb = bodyCheckBox(actor[-8:])
            cb.setChecked(True)
            cb.stateChanged.connect(lambda:self.btnState())
            hlayout.addWidget(cb)
            self.parameters.plotGUI['checkBoxes'][actor]={'hw':actor,'widget':cb,'state':True}
        self.layout.addLayout(hlayout)
        
    def btnState(self):
        self.plotSeries=['Time']
        for actor in self.parameters.actors['actors']:
            state = self.parameters.plotGUI['checkBoxes'][actor]['widget'].isChecked()
            self.parameters.plotGUI['checkBoxes'][actor]['state'] = state
            if state:
                self.plotSeries.append(actor)
        self.updatePlot()


class ProbeData:
    def updateDataFrame(self):       
        try:
            self.df = pd.read_csv(self.fp)
            self.df_columns = list(self.df)
            self.df_lastRow = self.df.iloc[[-1]]
        except: pass

##class PHProbe:
##    def __init__(self):
##        #do some stuff
##
##class SpecificGravityProbe:
##    def __init__(self):
##        #do some stuff
##
##class DissolvedOxygenProbe:
##    def __init__(self):
##        #do some stuff
##
##class ElectricalConductivityProbe:
##    def __init__(self):
##        #do some stuff



class TempProbe(ProbeData,PlotWindow):
    def __init__(self,parameters):
        super(TempProbe, self).__init__()
        self.parameters = parameters
        if self.parameters.test:
            self.name = 'Temperatures'
        self.fp = self.parameters.tempDatabaseFP 
        # self.count = 0
        self.plotSeries=['Time']+self.parameters.actors['actors']

    def plotFormat(self):
        colour = self.parameters.colour
        self.ax.set_xlabel('Time', color=colourPick(colour,'dark'),fontweight='bold')
        self.ax.set_ylabel('Temp (°{})'.format(self.parameters.units('temperature')), color=colourPick(colour,'dark'),fontweight='bold')
        self.ax.set_title(label = 'Temperature probes', color=colourPick(colour,'dark'),fontweight='bold')
        self.ax.set_facecolor(colourPick(colour,'dark'))
        self.canvas.figure.patch.set_facecolor(colourPick(colour,'light'))
        self.ax.tick_params(color=colourPick(colour,'dark'))
        # self.canvas.rc('grid', linestyle="-", color=colourPick(colour,'light'))
        self.ax.grid(b=True, which='major', color=colourPick(colour,'light'), linestyle='-')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main =  TempProbe('Temperatures')
    main.plot()
    main.show()
    sys.exit(app.exec_())