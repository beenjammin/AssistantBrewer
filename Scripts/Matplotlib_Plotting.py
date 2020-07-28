import sys
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import (Qt, pyqtSignal)
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import CheckButtons
import pandas as pd


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

        self.rax = self.canvas.figure.add_axes([0.02, 0.2, max(len(i) for i in self.df_columns)/85, (len(self.df_columns)-1)*0.04])
        # now we add checkboxes, one for each series
        self.check = CheckButtons(self.rax, (self.df_columns[1:]), (len(self.df_columns)-1)*[True])
        self.checkButtons_value = (len(self.df_columns)-1)*[True]
        self.canvas.figure.subplots_adjust(left=max(len(i) for i in self.df_columns)/50)
        self.plotFormat()
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
##        self.toolbar = NavigationToolbar(self.canvas, self)
        # set the layout
        layout = QVBoxLayout()
##        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start()
        self.canvas.draw()

    def updatePlot(self):
        self.updateDataFrame()
        color = ['blue','green','red','cyan','magenta','yellow','black']
        self.seriesList = []
        self.ax.clear()

        # this plots our series from the dataframe
        for count,col in enumerate(self.df_columns[1:]):
            self.seriesList.append(self.ax.plot(self.df_columns[0], col,data=self.df, label=col, color = color[count]))
        for count,self.series in enumerate(self.seriesList):
            self.series[0].set_visible(self.checkButtons_value[count])

        # bindings for checkboxes
        # we only want the bindings to happen once but the series has to be generated first
        if self.count < 1:
            # print('less than 1, connecting function')
            self.count += 1
            self.check.on_clicked(self.func)
        self.plotFormat()
        self.canvas.draw()

    def func(self,label):
        # print('clicked on, {}'.format(label))
        for count,self.series in enumerate(self.seriesList):
            if label == self.df_columns[1:][count]:
                self.series[0].set_visible(not self.series[0].get_visible())
                self.checkButtons_value[count] = self.series[0].get_visible()
        self.canvas.draw()



class ProbeData:
    def updateDataFrame(self):
        # print('updateDataFrame')
        self.df = pd.read_csv(self.fp)
        self.df_columns = list(self.df)
        self.df_lastRow = self.df.iloc[[-1]]

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
    def __init__(self,name,parameters):
        super(TempProbe, self).__init__()
        self.parameters = parameters
        self.name = name
        self.fp = self.name + '.csv'
        self.count = 0

    def plotFormat(self):
        colour = self.parameters.colour
        self.ax.set_xlabel('Time', color=colourPick(colour,'dark'),fontweight='bold')
        self.ax.set_ylabel('Temp (°{})'.format(self.parameters.tempUnit), color=colourPick(colour,'dark'),fontweight='bold')
        self.ax.set_title(label = self.name + ' probes', color=colourPick(colour,'dark'),fontweight='bold')
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