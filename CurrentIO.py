currentInputReadings = {}
currentOutputReadings = {}

ShouldControl = False
ShouldPauseControl = False

def getInputState(inputName):
	value = None	
	if str(inputName) in currentInputReadings.keys():
		value = currentInputReadings[inputName]		
	return value
	
def setInputState(inputName, value):
	currentInputReadings[inputName] = value 
	

def getOutputState(outputName):
	value = None	
	if outputName in currentOutputReadings.keys():		
		value = currentOutputReadings[outputName]		
	return value	
	
def setOutputState(outputName, value):	
	currentOutputReadings[outputName] = value 

def toggleOutputState(outputName):
	currentOutputReadings[outputName] = not currentOutputReadings[outputName]
	