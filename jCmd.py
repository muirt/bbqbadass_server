import json
import configuration
import unicodeHelper
import MReq

import time
import recorder

import dateHelper
import grapher
import CurrentIO

import debugger
import gpioDriverLime as gpio
import os

jCmdDictionary = {}


			
def register(jcmd):
	jCmdDictionary[jcmd.key] = jcmd

def GetElementFromName(name):
	inputNumber = 0
	returnVal = -1
	for input in configuration.InputList:
		if input.Name == name:
			returnVal = inputNumber
			break
		inputNumber += 1
	return returnVal

class JsonCommand:
	
	def __init__(self):
		self.key = "baseJsonCommand"
		self.hasReturnValue = False		
			
	def hasKey(self, key):
		return self.key == key
		
	def processCommand(self, value):
		debugger.dPrint(str(value))


class JCmdHysteresisSet(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "hysteresis_set"
		register(self)
		
	def processCommand(self, value):
		configuration.Parameters.Hysteresis = int(value)


class JCmdCollectionPeriodSet(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "collection_period_set"
		register(self)
		
	def processCommand(self, value):
		configuration.Parameters.CollectionPeriod = value
	

class JCmdOutputMode(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "output_mode"
		register(self)
		
	def processCommand(self, value):	
		if value == 'auto':
			CurrentIO.ShouldControl = True			
		else :			
			CurrentIO.ShouldControl = False
			if value == 'on':
				CurrentIO.setOutputState('controlOutput', True)
				gpio.outputLevel("FAN", 1)
			elif value == 'off':
				CurrentIO.setOutputState('controlOutput', False)
				gpio.outputLevel("FAN", 0)
			
	
class JCmdSetPointSet(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "set_point"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):
		if value == 'up':
			configuration.Parameters.SetPoint += 1
		if value == 'down':
			if configuration.Parameters.SetPoint >= 0:
				configuration.Parameters.SetPoint -= 1
		configuration.Save()
		
		setPoint = str(configuration.Parameters.SetPoint)	
		
		dataDict = {
					'secret':'badass', 
					'target':'periodic_update', 
					'value': { 
								'set_point': setPoint								
							  }
					}		
		
		return str(dataDict)	
		
class JCmdControlOutputSet(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "control_output_set"
		register(self)
		
	def processCommand(self, value):
		configuration.Parameters.ControlOutput = value

class JCmdCreateNewLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "create_new_log"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):		
		exists = False
		result = ""
		if len(value):			
			exists = recorder.startRecording(value)		
		if exists:
			result = placeResponseInMessage(value, "recording_already_exists")		
		return result	
	
class JCmdFinishCurrentLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "finish_current_log"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):
		recorder.finishRecording()
		
		##send confirmation, which triggers menu refresh
		return "result=success"
	
class JCmdDeleteLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "delete_log"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):
		print value
		recorder.deleteRecording(value)
		if value != "current":
			return MReq.MReqDictionary["list_saved_logs"].GetMenuData()	
		else:
			return None
			
	
class JCmdShowCurrentLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "show_current_log"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):	
		details = recorder.getCurrentRecordingDetails()
		result = placeResponseInMessage(str(details), 'current_recording_details')
		return result	
			
class JCmdShowSavedLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "show_saved_log"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):	
		logIndex = value.split("_")[1]
		details = recorder.getRecordingDetailsByIndex(logIndex)
		result = placeResponseInMessage(str(details), 'saved_recording_details')
		return result		
	
	
class JCmdGraphLog(JsonCommand):
	def __init__(self):	
		JsonCommand.__init__(self)		
		self.key = "graph_log"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):			
		dataset = grapher.getDataset(value)
		return placeResponseInMessage(str(dataset), 'graph_data')
		
class JCmdMenuRequest(JsonCommand):
	def __init__(self):	
		JsonCommand.__init__(self)
		self.key = "menu_request"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):
		result = None
		if value in MReq.MReqDictionary.keys():
			result = MReq.MReqDictionary[value].GetMenuData()		
		return result

class JCmdLogin(JsonCommand):
	def __init__(self):	
		JsonCommand.__init__(self)
		self.key = "login"
		self.hasReturnValue = False
		register(self)
		
	def processCommand(self, value):
		if value != "existing":
			value_list = value.split(",")
			if len(value_list) == 2:
				os.system("~/update_login.sh {0} {1}".format(value_list[0], value_list[1]))
		print "asdf"
		os.system("~/reset_interface.sh client")

		
jcmdLogin = JCmdLogin();
jcmdHysteresisSet = JCmdHysteresisSet()
jcmdCollectionPeriodSet = JCmdCollectionPeriodSet()
jcmdSetPointSet = JCmdSetPointSet()
jcmdMenuRequest = JCmdMenuRequest()
jCmdCreateNewLog = JCmdCreateNewLog()
jCmdFinishCurrentLog = JCmdFinishCurrentLog()
jCmdDeleteLog = JCmdDeleteLog()
jCmdShowCurrentLog = JCmdShowCurrentLog()
jCmdShowSavedLog = JCmdShowSavedLog()
jCmdGraphLog = JCmdGraphLog()
jCmdOutputMode = JCmdOutputMode()


	
	
def placeResponseInMessage(response, key):
	messageDict = {'secret': 'badass', 'target': key, 'value': response}
	return  str(messageDict).replace('"', ' ')
	
def process(key, value):
	
	result = None
	if jCmdDictionary.has_key(key):		
		if(jCmdDictionary[key].hasReturnValue):
			result = jCmdDictionary[key].processCommand(value)
		else:
			jCmdDictionary[key].processCommand(value)
			configuration.Save()
		
	return result

	
