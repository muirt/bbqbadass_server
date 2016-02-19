from pyA10Lime.gpio import gpio
from pyA10Lime.gpio import port
from pyA10Lime.gpio import connector
import time
from pyA10Lime import spi

outputConfigs = [
					{'pin': port.PG6, 'name': 'CS', 'level': gpio.HIGH},
				  	{'pin': port.PG7,  'name': 'TCSEL1', 'level': gpio.LOW},	
				  	{'pin': port.PG8, 'name': 'TCSEL2', 'level': gpio.LOW}				  				  			  
				]
				
def spiSetup():
	spi.open("/dev/spidev2.0")
	gpioSetup()
	
def spi_cs(level):				##TC AMP
	outputLevel("CS", level)

def readMAX31855():
	bytes = []	
	spi_cs(0)		
	bytes = spi.read(4)		
	spi_cs(1)
	return bytes
	
def close():
	spi.close() 
	
def configPin(pin, dir, state):
	gpio.setcfg(pin, dir)
	gpio.output(pin, state)
	
def outputLevel(name, level):	
	for output in outputConfigs:
		if output['name'] == name: 
			gpio.output(output['pin'], level)
			break
			
def gpioSetup():
	gpio.init() 	
	for config in outputConfigs:
		configPin(config['pin'], gpio.OUTPUT, config['level'])
	
def processBytes(bytes):
	result = None		
	if len(bytes) == 4:
		result = (bytes[0] << 24) | ( bytes[1] << 16) | (bytes[2] << 8) | (bytes[3])
		print result
		result >>= 18
		if result & 0x00002000:
			result -= 16384
		result *= 0.25	
	return result

def readTC(channel):
	if channel == 1:
		outputLevel('TCSEL1', 1)
		outputLevel('TCSEL2', 1)
	elif channel == 2:
		outputLevel('TCSEL1', 0)
		outputLevel('TCSEL2', 0)
		
	return processBytes(readMAX31855())

spiSetup()
while True:
	temp1 = readTC(1) * 9/5 + 32
	time.sleep(0.1)
	temp2 = readTC(2) * 9/5 + 32
	print 'TC1 = ' + str(temp1) + ' TC2 = ' + str(temp2)
	time.sleep(0.9)
	
	