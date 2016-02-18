#sensorsLime.py

import spiDriverLime
import MAX31855

import averager
import gpioDriverLime
import time


def setup():
	spiDriverLime.setup()
	
def SelectThermocoupleChannel(channel):
	if channel < 2:	
		gpioDriverLime.outputLevel('TCSEL1', channel)
		gpioDriverLime.outputLevel('TCSEL2', channel)		
	
def GetThermocoupleTemperature(channel):
	temperature = -1
	rawTCBytes = spiDriverLime.read()	
	if rawTCBytes:
		temperature = MAX31855.ProcessBytes(rawTCBytes) * 9/5 + 32
	if temperature > 3000:
		temperature = 0
	return int(averager.addReadingGetAverage(channel, temperature))

def GetProbeValue(channel):
	SelectThermocoupleChannel(channel)
	time.sleep(0.2)
	value = GetThermocoupleTemperature(channel)	
	return value
