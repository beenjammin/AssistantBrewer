import json, ast, csv, os
from Brewery_Parameters import Parameters
from pathlib import Path
from collections import Counter



class Config():
    def __init__(self):
        super().__init__()
        # self.parameters = parameters
        #initialise any dictionaries we might need
        self.initDicts()
        #file names
        self.connectionFN = 'connection_config'
        self.brewdayFN = 'brewery_config'
        #create the files if they do not exist
        self.createFile(self.connectionFN)
        self.createFile(self.brewdayFN)

    def loadConfig(self):
        self.loadSettingsConfig()
        self.loadBrewdayConfig()


    def initDicts(self):
        #hardware  dictionary of GUI {hardware:SimpleTemp,TempTgt,TempTimer,Relays}
        self.parameters.hwValues = {}
        for hw, value in self.parameters.hardware.items():
            if value['widgets'][0]:
                self.parameters.hwValues[hw] = {'SimpleTemp':None}
            #check if we are adding target temperature functionality to the hardware
            if value['widgets'][1]:
                self.parameters.hwValues[hw] = {'TempTgt':{'tgtLineTemp':'','tempLineTol':self.parameters.tempTol}}
            #check if we are adding temperature timer functionality to the hardware
            if value['widgets'][2]:
                self.parameters.hwValues[hw] = {'TempTimer':{   'temps':[65,70],
                                                                'times':[0,60],
                                                                'tempTolerance':self.parameters.tempTol,
                                                                'holdTemps':True,
                                                                'warmUp':False,
                                                                'plotLiveTemp':False,
                                                                }}
        print('hwValues are {}'.format(self.parameters.hwValues))

    def saveBrewdayConfig(self):
        self.brewdayFN = 'brewery_config'
        self.saveFile(self.brewdayFN,self.parameters.hwValues)

    def loadBrewdayConfig(self):
        td = self.loadFile(self.brewdayFN)
        if td == None:
            return None
        #loop through hw and check that the controls are the same for each
        for hw, values in td.items():
            if self.compareParameters(values, self.parameters.hwValues[hw]):
                self.parameters.hwValues[hw] = values

                
    def saveConnectionConfig(self):
        #pack dictionary
        ls = []
        lsA = []
        for probe in self.parameters.probes.keys():
            ls.append(self.parameters.probes[probe]['hw'])
            lsA.append(self.parameters.probes[probe]['actors'])
        td = {'relay':self.parameters.relayPins, 'floatSwitch':self.parameters.floatPins, 'hw': ls, 'actors':lsA}
        self.saveFile(self.connectionFN,td)


    def loadSettingsConfig(self):
        'need to compare active pins and probes to see if they match to the last config file'
        td = self.loadFile(self.connectionFN)
        if td == None:
            return None
        #unpack file
        relay = td['relay']
        floatSwitch = td['floatSwitch']
        actors = td['actors']
        hw = td['hw']
        #compare parameter keys and update if they match
        if self.compareParameters(relay,self.parameters.relayPins):
            self.parameters.relayPins = relay
        if self.compareParameters(floatSwitch,self.parameters.floatPins):
            self.parameters.floatPins = floatSwitch
        
        #actors is a special case
        lsA = []
        for probe in self.parameters.probes.keys():
            lsA.append(self.parameters.probes[probe]['actors'])
        if list(actors) == list(lsA):
            for count, probe in enumerate(self.parameters.probes.keys()):
                self.parameters.probes[probe]['hw'] = hw[count]


    def compareParameters(self,p1,p2):
        # print(ls)
        if list(p1) == list(p2):
            return True
            # print ('ls1 is now {}'.format(ls[1]))
        elif Counter(list(p1)) == Counter(list(p2)):
            print('items for {} are in a different order'.format(p2))
            return False
        else:
            print('could not load items for {} likely hardware change'.format(p2))
            return False


    def loadFile(self,fn):
        fp = self.parameters.configFP+'/'+fn+'.json'
        if os.stat(fp).st_size != 0:
            with open(fp) as f:
                td = json.load(f)   
        else:
            td = None            
        return td
         

    def saveFile(self,fn,td):
        fp = self.parameters.configFP+'/'+fn+'.json'
        print ('dict is {}'.format(td))
        with open(fp, "w") as a_file:
            json.dump(td, a_file)
        print('saved {} configuration'.format(fn))


    def createFile(self,fn):    
        fp = self.parameters.configFP+'/'+fn+'.json'
        print('trying to create file {}'.format(fp))
        print(Path(fp).is_file())
        if not Path(fp).is_file():
            Path(fp).touch()
            print('created new file --> {}'.format(fp))


