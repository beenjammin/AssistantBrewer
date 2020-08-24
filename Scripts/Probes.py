from Database import databaseManager
from Matplotlib_Plotting import PlotWindow
from Brewery_Parameters import colourPick


class TempProbe(databaseManager,PlotWindow):
    """
    This class defines the temperature probes, currently links to a database and defines the plot formatting
    """
    def __init__(self,parameters):
        super().__init__()
        self.parameters = parameters
        self.fp = self.parameters.probes['temperature']['fp']
        self.plotSeries = ['Time'] + self.parameters.probes['temperature']['probes']


    def plotFormat(self):
        colour = self.parameters.colour
        self.ax.legend(loc='upper left')
        #the next three lines are the only ones specific to temperature, the rest could be in a more generic class that can be inherited by all plots
        self.ax.set_xlabel('Time', color=colourPick(colour,'dark'),fontweight='bold')
        self.ax.set_ylabel('Temp (°{})'.format(self.parameters.units('temperature')), color=colourPick(colour,'dark'),fontweight='bold')
        self.ax.set_title(label = 'Temperature probes', color=colourPick(colour,'dark'),fontweight='bold')

        self.ax.set_facecolor(colourPick(colour,'dark'))
        self.canvas.figure.patch.set_facecolor(colourPick(colour,'light'))
        self.ax.tick_params(color=colourPick(colour,'dark'))
        # self.canvas.rc('grid', linestyle="-", color=colourPick(colour,'light'))
        self.ax.grid(b=True, which='major', color=colourPick(colour,'light'), linestyle='-')