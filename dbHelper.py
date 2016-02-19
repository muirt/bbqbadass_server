import couchdb
import json
import time
import logHelper
import unicodeHelper
import debugger


class dbHelper:

	def __init__(self):    
		self.couch = couchdb.Server()
		currentLog = logHelper.getCurrentLog()
		self.inputdb = None
		self.outputdb = None
		if len(currentLog.keys()) > 0:
			nameBase = currentLog["log_name"].lower() + currentLog["start_date"]
			inputName = nameBase + "input"
			outputName = nameBase + "output"
			
			try:
				self.inputdb = self.couch[inputName]				
			except couchdb.http.ResourceNotFound:
				self.inputdb = self.couch.create(inputName)			
			try:
				self.outputdb = self.couch[outputName]
			except couchdb.http.ResourceNotFound:
				self.outputdb = self.couch.create(outputName)
	
	def isValidFilename(self, name):
		isValid = True
		name = unicodeHelper.getAscii(name).lower()
		acceptableChars = ('abcdefghijklmnopqrstuvwxyz0123456789')
		for char in name:
			if char not in acceptableChars:
				isValid = False
				break
		return isValid
		
	def createNewDb(self, name):
		name = name.lower()
		inputName = name + "input"
		outputName = name + "output"
		self.inputdb = self.couch.create(inputName)
		self.outputdb = self.couch.create(outputName)
		
	def finalizeCurrentDb(self):
		self.inputdb = None
		self.outputdb = None
		
	def deleteDatabaseByName(self, name):
		inputName = name + "input"
		outputName = name + "output"
		self.couch.delete(inputName)
		self.couch.delete(outputName)
    
	def deleteAllDbs(self):
		self.couch.delete('/_all_dbs')
	
	def addInputEntry(self, entry):
		if self.inputdb:				
			self.inputdb.save(entry)
        
	def findAllInputEntries(self, map_func):   
		allEntries = None
		if self.inputdb:
			allEntries = self.inputdb.query(map_func)
		return allEntries
		
		
	def getLatestInputEntry(self):
		latestEntry = None
		result = None
		map_func = '''function(doc){
				emit(doc.time, {time: doc.time, inputs: doc.state});
		   }'''
		if self.inputdb:
			result = self.inputdb.query(map_func, descending=True)
			if result:
				latestEntry = result.rows[0].value
		return latestEntry
		
	def addOutputEntry(self, entry):
		if self.outputdb:
			self.outputdb.save(entry)
		
	def findAllOutputEntries(self, map_func):    	
		result = None
		if self.inputdb:
			result = self.inputdb.query(map_func)
		return result
		
	def getLatestOutputEntry(self):
		latestEntry = None
		result = None
		map_func = '''function(doc){
				emit(doc.time, {time: doc.time, outputState: doc.outputState});
			}'''
		if self.outputdb:
			result = self.outputdb.query(map_func, descending=True)
			if result:
				latestEntry = result.rows[0].value
		return latestEntry

	def readSavedDatabaseValues(self, dbName, readingType):
		dbName = dbName.lower()
		if readingType == "input":
			filename = dbName + "input"			
		else:	
			filename = dbName + "output"
				
		dbExists = True
		try:
			self.saveddb = self.couch[filename]	
		except couchdb.http.ResourceNotFound:
			dbExists = False
			
		result = None
		if dbExists:			
			map_func = None
			if readingType == "input":
				map_func = '''function(doc){
					emit(doc.time, {time: doc.time, inputs: doc.inputs});
					}'''
			else:
				map_func = '''function(doc){
					emit(doc.time, {time: doc.time, outputs: doc.state});
					}'''
			result = self.saveddb.query(map_func, descending=False)
			
		   
		return result
			