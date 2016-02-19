##import hardware
import processorDefinition
if processorDefinition.processor == "BBB":
	import gpioDriverBBB as gpio
elif processorDefinition.processor == "Lime":
	import gpioDriverLime as gpio
	
import time
import configuration
import CurrentIO

class OutputControl:
		
	outputDict = {True: 'on', False: 'off'}

	def __init__(self):
		self.SetOutputState(False)
		
		
	def GetInputState(self, inputName):
		return CurrentIO.getInputState(inputName)
        
	def SetOutputState(self, outputState):
		CurrentIO.setOutputState('controlOutput', outputState)
	
	def GetOutputState(self):
		return CurrentIO.getOutputState('controlOutput')

	def ControlLoopPass(self, controlOutput, controlInput, setPoint, hysteresis, onState):
		inputValue = self.GetInputState(configuration.InputList[controlInput].Name)
		##print 'input = ' + str(inputValue) + ' setpoint = ' + str(setPoint)
		
		if(self.GetOutputState() == True):  #fan is on
			if(inputValue >= setPoint):	#fan should turn off
				outputState = False
				outputStateInt = 0
				if outputState:
					outputStateInt = 1
				gpio.outputLevel("FAN", outputStateInt)
				self.SetOutputState(outputState)

		else:	#fan is off 
			if(inputValue < setPoint - hysteresis): #fan should turn on
				outputState = True
				outputStateInt = 0
				if outputState:
					outputStateInt = 1
				gpio.outputLevel("FAN", outputStateInt)
				self.SetOutputState(outputState)
		#print self.GetOutputState()