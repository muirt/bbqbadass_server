import json 
import time
import ast


def getLogDictionary():
	logDictionary = {"current_log":{}, "saved_logs":[]}
	try:
		logDictionaryFile = open("logDictionary.json", "r")
	except IOError:
		saveLogDictionary(logDictionary)
		logDictionaryFile = open("logDictionary.json", "r")
	if logDictionaryFile != None:
		logDictionaryFileString = str(' '.join(logDictionaryFile.readlines()))		
		if len(logDictionaryFileString):
			logDictionary = ast.literal_eval(logDictionaryFileString)
	return logDictionary
	
def nameIsUnique(name,date):
	logDictionary = getLogDictionary()
	currentLog = logDictionary["current_log"]
	if currentLog:
		if currentLog["log_name"] == name:
			if currentLog["start_date"] == date:
				return False
	for dictionary in logDictionary["saved_logs"]:
		if dictionary["log_name"] == name:
			if dictionary["start_date"] == date:
				return False	
	return True	

def createNewLog(name, date, currentTime):
	finalizeCurrentLog()
	logDictionary = getLogDictionary()
	currentLog = {"log_name": name, "start_date": date, "start_time": currentTime}
	logDictionary["current_log"] = currentLog	
	saveLogDictionary(logDictionary)
	
def getCurrentLog():
	logDictionary = getLogDictionary()
	return logDictionary["current_log"]
	
def saveLogDictionary(logDictionary):
	logDictionaryFile = open("logDictionary.json", "w")
	if logDictionaryFile != None:		
		logDictionaryString = str(logDictionary)
		logDictionaryFile.write(logDictionaryString)
		
def getSavedLogByName(name):
	requestedLog = None
	logDictionary = getLogDictionary()
	savedLogsList = logDictionary["saved_logs"]
	for dictionary in savedLogsList:
		if dictionary["log_name"] == name:
			requestedLog = dictionary
			break
	return requestedLog
	
def deleteAllLogs():
	logDictionary = {"current_log":{}, "saved_logs":[]}
	saveLogDictionary(logDictionary)
	
def deleteCurrentLog():	
	currentLog = {}
	logDictionary = getLogDictionary()
	logDictionary["current_log"] = currentLog
	saveLogDictionary(logDictionary)

def deleteSavedLog(name):
	logDictionary = getLogDictionary()
	savedLogsList = logDictionary["saved_logs"]
	for dictionary in savedLogsList:
		if dictionary["log_name"] + dictionary["start_date"] == name:
			savedLogsList.remove(dictionary)
			logDictionary["saved_logs"] = savedLogsList
			saveLogDictionary(logDictionary)
			break
	
def getCurrentLogElapsedTime():
	logDictionary = getLogDictionary()
	currentLog = logDictionary["current_log"]
	seconds = 0
	if currentLog:
		seconds = (int(time.time()) - int(currentLog["start_time"]))
	timeString = "0h00m"
	if int(seconds) > 60:
		minutes = (seconds / 60) % 60
		hours = seconds/3600
		timeString = "%ih%02im" % (hours, minutes)
		#str(hours) + "h" + str(minutes) + "m"
	return timeString
		
def finalizeCurrentLog():
	logDictionary = getLogDictionary()
	currentLog = logDictionary["current_log"]
	if len(currentLog.keys()) > 0:		
		newSavedLogName = currentLog["log_name"]
		newSavedLogDate = currentLog["start_date"]
		newSavedLogDuration = getCurrentLogElapsedTime()
		newSavedLog = {"log_name" : newSavedLogName, "start_date": newSavedLogDate,  "duration" : newSavedLogDuration}
		savedLogList = logDictionary["saved_logs"]
		savedLogList.insert(0, newSavedLog)
		logDictionary["saved_logs"] = savedLogList
		logDictionary["current_log"] = {}
		saveLogDictionary(logDictionary)
		