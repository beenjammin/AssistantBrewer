from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class EventFunctions():
	def __init__(self,parameters):
		self.parameters = parameters

	def updatePins(self):
		#reset pins
		for key, value in self.parameters.brewGUI.items():
			try:
				value['relayGroupBox']
				text = 'Relay pins attached --> no relays attached'
				self.parameters.brewGUI[key]['relayGroupBox']['QLabelCurrentPins']['widget'].setText(text)
				self.parameters.brewGUI[key]['relayGroupBox']['QLabelCurrentPins']['value']='no relays attached' 
			except:
				print("Unexpected error:", sys.exc_info()[0])
				raise       


		#updating the brewGUI dictionary
		for key, value in self.parameters.settingsGUI['relayDict'].items():
			#set the relay pin
			pin = key
			#set the combobox in the GUI associated with the pin
			cb = value['QCBRelay']['widget']
			#get the combox value
			hw = cb.currentText()
			#update the dictionary, adding the selected combobox value for the pin
			value['QCBRelay']['value'] = hw
			#going to try and add the associate the pin with the hardware
			try:
				#check if hw is in the list, if not, display default text
				if hw in list(self.parameters.hardware):
					if self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['value'] == 'no relays attached':
						self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['value'] = []
						self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].setText('Relay pins attached -->')
					#add the pin to the dictionary
					text = self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].text()
					self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['value'].append(pin)
					#updating the GUI with hardware connected pins
					text +=' {}'.format(pin)
					self.parameters.brewGUI[hw]['relayGroupBox']['QLabelCurrentPins']['widget'].setText(text)						
			except:
				print("Unexpected error:", sys.exc_info()[0])
				raise
			
