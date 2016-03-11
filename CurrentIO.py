import math

currentInputReadings = {}
currentOutputReadings = {}

ShouldControl = False
ShouldPauseControl = False

class Sensor():

	def __init__(self):
		self.reading_count = 0

	def get_sensor_value(self, name):
		value = 0
		if name == "Meat":
			value = 120 + 15 * math.cos(6.28 * self.reading_count/60)
		elif name == "Grill":
			value = 190 + 20 * math.sin(3.14 * self.reading_count/60)

		value = int(value)
		self.reading_count += 1

		if self.reading_count == 60:
			self.reading_count = 0

		return value

sensor1 = Sensor()

def getInputState(inputName):
	value = None	
	if str(inputName) in currentInputReadings.keys():
		value = currentInputReadings[inputName]	

	value = sensor1.get_sensor_value(inputName)
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
	