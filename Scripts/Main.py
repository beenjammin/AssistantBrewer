from Vertical_Tabs import mainGUI
from Brewery_Parameters import Parameters
from Actor_Classes import csvFunctions
from multiprocessing import Process
from time import time.sleep


class intialiseBrewery():
	def __init__(self,parameters):
		self.parameters = parameters
		if not self.parameters.test:
			p1 = multiprocessing.Process(target=self.outputData)
			p1.start()
			p1.join()

	def outputData(self):
		while True:
			dataWrite = csvFunctions(self.parameters)
			readings = [actor_read_raw(a+'/w1_slave') for a in self.parameters.actors['actors']]
			dataWrite.appendRow(readings)
	
if __name__ == '__main__':
	parameters = Parameters()
	a = intialiseBrewery(parameters)
	b = mainGUI(parameters)