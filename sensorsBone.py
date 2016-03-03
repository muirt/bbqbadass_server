#sensorsLime.py


import MAX31855

import averager

import time
import configuration


def setup():
	#spiDriverLime.setup()
	pass
	
def SelectThermocoupleChannel(channel):
	#if channel < 2:	
		#gpioDriverLime.outputLevel('TCSEL1', channel)
		#gpioDriverLime.outputLevel('TCSEL2', channel)		
	pass
	
def GetThermocoupleTemperature(channel):
	'''temperature = -1
	rawTCBytes = spiDriverLime.read()	
	if rawTCBytes:
		temperature = MAX31855.ProcessBytes(rawTCBytes)		
		if configuration.Parameters.Units == "F":
			temperature = temperature * 9/5 + 32
	if temperature > 3000:
		temperature = 0
	return int(averager.addReadingGetAverage(channel, temperature))
	'''

def GetProbeValue(channel):
	'''
	SelectThermocoupleChannel(channel)
	time.sleep(0.2)
	value = GetThermocoupleTemperature(channel)	
	return value'''
	return 70

