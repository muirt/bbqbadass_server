#gpioDriver.py works with A10 Lime
from pyA10Lime.gpio import gpio
from pyA10Lime.gpio import port
from pyA10Lime.gpio import connector
import time

outputConfigs = [
					{'pin': port.PG6, 'name': 'CS', 'level': gpio.HIGH},
				  	{'pin': port.PG7,  'name': 'TCSEL1', 'level': gpio.LOW},	
				  	{'pin': port.PG8, 'name': 'TCSEL2', 'level': gpio.LOW},	
				  	{'pin': port.PG9, 'name': 'FAN', 'level': gpio.LOW}			  				  			  
				]

def configPin(pin, dir, state):
	gpio.setcfg(pin, dir)
	gpio.output(pin, state)
	
def outputLevel(name, level):	
	for output in outputConfigs:
		if output['name'] == name:						
			gpio.output(output['pin'], level)
			break
			
def setup():
	gpio.init() 	
	for config in outputConfigs:
		configPin(config['pin'], gpio.OUTPUT, config['level'])
	
	