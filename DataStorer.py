import time
import recorder
import configuration
import CurrentIO


	
		
def StoreData():
	currentTime = int(time.time())

	dbEntry = {'inputs': [], 'time': currentTime }
	for input in configuration.InputList:
		name = input.Name
		state = CurrentIO.getInputState(name)
		inputEntry = {'name': name, 'state': state}
		dbEntry['inputs'].append(inputEntry)	
	recorder.addInputReading(dbEntry)	
	##get output states and put them in the output database	
	outputEntry = { 'state': CurrentIO.getOutputState('controlOutput'), 'time': currentTime}
	recorder.addOutputReading(outputEntry)
		
		
		