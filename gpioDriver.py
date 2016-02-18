#gpioDriver.py
from pyA10Lime.gpio import gpio
from pyA10Lime.gpio import port
from pyA10Lime.gpio import connector
import time

outputConfigs = [
				  {'pin': port.PI10, 'name': 'CS0'},
				  {'pin': port.PI14, 'name': 'CS1'},
				  {'pin': port.PI7,  'name': 'CS2'},
				  {'pin': port.PI8,  'name': 'CS3'},
				  {'pin': port.PI13, 'name': 'MISO'},
				  {'pin': port.PI9, 'name': 'Fan'},
				  ]

def configPinOutput(pin, dir, state):
	gpio.setcfg(pin, dir)
	outputLevel(config['name'], state)
	#gpio.pullup(pin, gpio.PULLDOWN)    
	#gpio.pullup(pin, gpio.PULLUP)  
	#gpio.pullup(pin, 0)   #Clear pullups

def outputLevel(name, level):
	for output in outputConfigs:
		if output['name'] == name: 
			gpio.output(output['pin'], level)
			return
			
def 