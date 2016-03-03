import json
import configuration
import unicodeHelper
import MReq

import time
import CurrentIO
import gpioDriverLime as gpio
import os
import updateGUI
import averager
import tempUtilities

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
		pass


class JCmdHysteresisSet(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "hysteresis_change"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):
		if value == "up":
			if configuration.Parameters.Hysteresis < 10:
				configuration.Parameters.Hysteresis += 1
		elif value == "down":
			if configuration.Parameters.Hysteresis > 0: 
				configuration.Parameters.Hysteresis -=1
		configuration.Save()
		
		hysteresis = str(configuration.Parameters.Hysteresis)	
		
		result = placeResponseInMessage('hysteresis', hysteresis, 'response')
		
		return str(result)	

class JCmdMeatTempGoal(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "meat_temperature_goal"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):
		if int(value):
			configuration.Parameters.MeatTemperatureGoal = int(value)		
		print configuration.Parameters.MeatTemperatureGoal
		configuration.Save()		
		goal_temp = str(configuration.Parameters.MeatTemperatureGoal)			
		result = placeResponseInMessage('meat_temperature_goal', goal_temp, 'response')				
		return str(result)	


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
		
		result = placeResponseInMessage('set_point', setPoint, 'response')
		
		return str(result)	
		
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
			exists = False  #phant TODO	
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
		#recorder.finishRecording()   #phant TODO
		emptyDict = {'name': 'Not', 'time': 'Recording'}
		result = placeResponseInMessage("details", str(emptyDict) , 'recording')
		return result	
			
class JCmdDeleteLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "delete_log"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):
		print value
		#recorder.deleteRecording(value)  #phant TODO
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
		#details = recorder.getCurrentRecordingDetails()  #phant TODO
		result = placeResponseInMessage("details", str(details), 'recording')
		return result	
			
class JCmdShowSavedLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "show_saved_log"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):	
		logIndex = value.split("_")[1]
		#details = recorder.getRecordingDetailsByIndex(logIndex)  #phant TODO
		result = placeResponseInMessage(str(details), 'saved_recording_details')
		return result		
	
	
class JCmdGraphLog(JsonCommand):
	def __init__(self):	
		JsonCommand.__init__(self)		
		self.key = "graph_log"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):			
		#dataset = grapher.getDataset(value)  #phant TODO
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
		print str(result)

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
		os.system("~/reset_interface.sh client")

class JCmdUnitSet(JsonCommand):
	def __init__(self):	
		JsonCommand.__init__(self)
		self.key = "units"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):
		#all numeric values must now be updated, 
		#as their unit is being changed
		
		if value == "F":
			if configuration.Parameters.Units == "C":
				configuration.Parameters.SetPoint =  tempUtilities.CtoF(configuration.Parameters.SetPoint)
				configuration.Parameters.MeatTemperatureGoal = tempUtilities.CtoF(configuration.Parameters.MeatTemperatureGoal)
				configuration.Parameters.Units = "F"
		elif value == "C":
			if configuration.Parameters.Units == "F":
				configuration.Parameters.SetPoint =  tempUtilities.FtoC(configuration.Parameters.SetPoint)
				configuration.Parameters.MeatTemperatureGoal = tempUtilities.FtoC(configuration.Parameters.MeatTemperatureGoal)
				configuration.Parameters.Units = "C"
		
		averager.clearAverage()
		configuration.Save()

		CurrentIO.ShouldPauseControl = True

		#return a special string that tells the caller, the websocket server, 
		#to use its own update function as this cmd's response
		return updateGUI.updateGUI()


jCmdUnitSet = JCmdUnitSet();
jcmdMeatTempGoal = JCmdMeatTempGoal();		
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


	
	
def placeResponseInMessage(string, val, key):

	messageDict = {
			'secret':'badass', 
			'target':key, 
			'value': { 
						string: val
					  }
			}
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

	
