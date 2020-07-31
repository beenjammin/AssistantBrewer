from Vertical_Tabs import mainGUI
from Brewery_Parameters import Parameters
from Actor_Classes import csvFunctions, actor_read_raw
from multiprocessing import Process



class intialiseBrewery():
    def __init__(self,parameters):
        print('initialising brewery')
        self.parameters = parameters
        if not self.parameters.test:
            print('starting another process')
            self.dataWrite = csvFunctions(self.parameters)
            self.dataWrite.createFile()
            p1 = Process(target=self.outputData)
            p1.start()
            print('loading GUI')
            b = mainGUI(self.parameters)
            
#        p2 = Process(target=self.initialiseGUI)
#        p2.start()
#        p2.join()

    def outputData(self):
        while True:
            print('writing data')
            readings = [actor_read_raw(a+'/w1_slave') for a in self.parameters.actors['actors']]
            self.dataWrite.appendRow(readings)
     
#    def initialiseGUI(self):        
#        b = mainGUI(self.parameters)
	
if __name__ == '__main__':
    parameters = Parameters()
    a = intialiseBrewery(parameters)
    
#    b = mainGUI(parameters)
    
