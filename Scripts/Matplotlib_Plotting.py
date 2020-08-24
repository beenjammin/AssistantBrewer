import sys
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import (Qt, pyqtSignal)
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from Database import databaseManager
from Widget_Styles import *


class PlotWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
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
        self.plotFormat()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.addCheckBoxes()
        self.setLayout(self.layout)

        self.canvas.draw()

    def updatePlot(self):
        self.updateDatabase()
#        print(self.df)
        colour = self.parameters.plotColours
        self.ax.clear()
        labelList = []
        for count, label in enumerate(self.parameters.probes['temperature']['hw']):
            if label:
                labelList.append(label)
            else:
                labelList.append(self.headers[count+1])
        # this plots our series from the dataframe
        for count, col in enumerate(self.headers[1:]):
            if col in self.plotSeries:
                self.ax.plot(self.headers[0], col, data=self.data, label=labelList[count], color=colour[count])
        self.plotFormat()
        self.canvas.draw()

    def addCheckBoxes(self):
        self.parameters.plotGUI['checkBoxes']={}
        hlayout = QHBoxLayout()
        for actor in self.parameters.probes['temperature']['probes']:
            cb = bodyCheckBox(actor[-8:])
            cb.setChecked(True)
            cb.stateChanged.connect(lambda:self.btnState())
            hlayout.addWidget(cb)
            self.parameters.plotGUI['checkBoxes'][actor]={'hw':actor,'widget':cb,'state':True}
        self.layout.addLayout(hlayout)
        
    def btnState(self):
        self.plotSeries=['Time']
        for actor in self.parameters.probes['temperature']['probes']:
            state = self.parameters.plotGUI['checkBoxes'][actor]['widget'].isChecked()
            self.parameters.plotGUI['checkBoxes'][actor]['state'] = state
            if state:
                self.plotSeries.append(actor)
        self.updatePlot()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main =  TempProbe('Temperatures')
    main.plot()
    main.show()
    sys.exit(app.exec_())