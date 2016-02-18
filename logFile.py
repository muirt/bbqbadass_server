from time import strftime

class LogFile:
	
	def __init__(self):
		self.logFile = open("log.txt", "a")
		
	def write(self, logString):
		timeString = strftime("%Y-%m-%d %H:%M:%S ") + logString + "\n"
		self.logFile.write(timeString)

		