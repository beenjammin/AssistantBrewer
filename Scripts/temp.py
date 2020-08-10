import sys
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import (Qt, pyqtSignal)
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import CheckButtons
import pandas as pd

from Widget_Styles import *
from Brewery_Parameters import colourPick


class PlotWindow(QDialog):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        self._want_to_close = False
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.rows = 2

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

        # self.plotFormat()
        self.layout = QVBoxLayout()
##        layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.addInputBoxes()
        self.setLayout(self.layout)

        self.canvas.draw()


    def updatePlot(self):
        #this function draws the temp profile based on the users inputs
        colour = ['blue','green','red','cyan','magenta','yellow','black']
        self.seriesList = []
        self.ax.clear()

        # this plots our series from the dataframe
        for count,col in enumerate(self.df_columns[1:]):
            if col in self.plotSeries:
                self.seriesList.append(self.ax.plot(self.df_columns[0], col,data=self.df, label=col, color = colour[count]))
        self.plotFormat()
        self.canvas.draw()


    def addToolbar(self):
        #add the toolbar at bottom of the plot
        self.parameters.plotGUI['checkBoxes']={}
        hlayout = QHBoxLayout()
        for actor in self.parameters.actors['actors']:
            cb = bodyCheckBox(actor[-8:])
            cb.setChecked(True)
            cb.stateChanged.connect(lambda:self.btnState())
            hlayout.addWidget(cb)
            self.parameters.plotGUI['checkBoxes'][actor]={'hw':actor,'widget':cb,'state':True}
        self.layout.addLayout(hlayout)
        

if __name__ == '__main__':pass
