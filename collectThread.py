import configuration

import threading
import time
import processorDefinition

import Queue

import sensorsLime as sensors

import CurrentIO



class CollectThread:
	
	def __init__(self):
		self.ShouldStop = False
		sensors.setup()
		self.count = 0		



	def PeriodicCollect(self):        
		self.ShouldStop = False		
				
		while self.ShouldStop == False:	
			self.ReadInputs(configuration.InputList)				
						
			# must wait 0.2 seconds after switching before reading TC
			timeAlreadySlept = len(configuration.InputList) * 0.2 			
			time.sleep(configuration.Parameters.CollectionPeriod - timeAlreadySlept)


	def ReadInputs(self, inputList):
		inputReadingList = []
			 
		for input in inputList:					
			value = sensors.GetProbeValue(input.MultiplexerChannel) 					
			CurrentIO.setInputState(input.Name, value)
			
			
					
