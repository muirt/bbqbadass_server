

thermocoupleReadingsList = [[] for x in range(2)] 

maxListSize = 10

def addReadingGetAverage(channel, newReading):
	addReading(channel, newReading)
	return getAverage(channel)
	
def addReading(channel, newReading):
	thermocoupleReadingsList[channel].append(newReading)
	if len(thermocoupleReadingsList[channel]) > maxListSize:
		del thermocoupleReadingsList[channel][0]
		
def getAverage(channel):
	sum = 0
	for reading in thermocoupleReadingsList[channel]:
		sum += reading
	average = sum/len(thermocoupleReadingsList[channel])
	return average