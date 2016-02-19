import dbHelper
import logHelper
import time
import unicodeHelper
import dateHelper
import DataStorer

db = dbHelper.dbHelper()

isRecording = False

if logHelper.getCurrentLog():
	isRecording = True

def startRecording(name):
	nameExists = True
	if db.isValidFilename(name):
		date = dateHelper.getCurrentDate()
		currentTime = int(time.time())
		if logHelper.nameIsUnique(name,date):
			logHelper.createNewLog(name, date, currentTime)
			db.createNewDb(name+date)
			DataStorer.StoreData()
			isRecording = True
			nameExists = false
	return nameExists
	
def deleteRecording(name):
	if name == "current":
		logDetails = logHelper.getCurrentLog()
		isRecording = False
		if len(logDetails.keys()):
			dbName = str(logDetails["log_name"]) + str(logDetails["start_date"]) 
			logHelper.deleteCurrentLog()
			db.deleteDatabaseByName(dbName)		
	else:
		logHelper.deleteSavedLog(name)
		db.deleteDatabaseByName(name.lower())
		
def getCurrentRecordingDetails():
	currentLog = logHelper.getCurrentLog()
	logList = []
	name = ""
	duration = ""
	startTime = ""
	if currentLog:
		name = unicodeHelper.getAscii(currentLog["log_name"])
		duration = getCurrentRecordingElapsedTime()
	dataDict = {'name': name, 'time': str(duration)}
	
	return str(dataDict)
	
def getRecordingDetailsByIndex(index):
	logDictionary = logHelper.getLogDictionary()
	#data_string = ""		
	log = logDictionary["saved_logs"][int(index)]
	name = unicodeHelper.getAscii(log["log_name"])
	#data_string = "saved_log_details=" + name + "," + log["start_date"] + "," + log["duration"] 
	dataDict = {'name': name, 'start_date': log['start_date'], 'time': log['duration']}
	return unicodeHelper.getAscii(str(dataDict))
		

def getCurrentRecordingName():
	currentLog = logHelper.getCurrentLog()
	return currentLog["log_name"] + currentLog["start_date"]
		
def listAllRecordings():
	logDictionary = logHelper.getLogDictionary()
	logIndex = 0
	dataList = []
	for savedLog in logDictionary["saved_logs"]:
		nameListString = savedLog["log_name"] + '_' + savedLog["start_date"] + '_' + str(logIndex)
		nameListString = unicodeHelper.getAscii(nameListString)
		dataDict = {'name': nameListString}
		dataList.append(dataDict)
		logIndex += 1
	
	if len(dataList) == 0:
		dataList.append('empty')
			
	return str(dataList)

def addInputReading(reading):
	db.addInputEntry(reading)
	
def addOutputReading(reading):
	db.addOutputEntry(reading)
	
def getAllReadingsFromCurrentRecording(readingType):
	currentLog = logHelper.getCurrentLog()	
	dbName = currentLog["log_name"] + currentLog["start_date"]
	dbName = unicodeHelper.getAscii(dbName)
	return db.readSavedDatabaseValues(dbName, readingType)
	

def getAllReadingsFromRecording(name, readingType):
	return db.readSavedDatabaseValues(name, readingType)
	
def finishRecording():
	logHelper.finalizeCurrentLog()
	db.finalizeCurrentDb()
	isRecording = False

def getCurrentRecordingElapsedTime():
	return logHelper.getCurrentLogElapsedTime()