import time
from Adafruit_BBIO.SPI import SPI
from Adafruit_BBIO import GPIO
class Inputs:
	muxPinNames = ["","","",""]
	
	
		
def SetDigitalOutput(pin, value):
	valueString = "off"
	if value == True:
		valueString = "on"
