import configuration

import threading
import time
import processorDefinition
import logFile

import sensorsLime as sensors

import CurrentIO

class CollectThread:
	
	def __init__(self):
		self.ShouldStop = False
		sensors.setup()
			
	def PeriodicCollect(self):        
		self.ShouldStop = False
		self.log = logFile.LogFile()
		self.readingCount = 0
		
		while self.ShouldStop == False:			
			self.ReadInputs(configuration.InputList)
			# must wait 0.2 seconds after switching before reading TC
			timeAlreadySlept = len(configuration.InputList) * 0.2 			
			time.sleep(configuration.Parameters.CollectionPeriod - timeAlreadySlept)

	def ReadInputs(self, inputList):
		inputReadingList = []
		logString = ""		 
		for input in inputList:					
			value = sensors.GetProbeValue(input.MultiplexerChannel) 					
			CurrentIO.setInputState(input.Name, value)
			logString += input.Name + ": " + str(value) + " "
		self.readingCount += 1
		if self.readingCount >= 20:
			self.readingCount = 0
			self.log.write(logString)
			
					