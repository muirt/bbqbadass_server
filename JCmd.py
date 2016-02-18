import json
import configuration
import unicodeHelper
import MReq
import os
import time
import recorder

import dateHelper
import grapher
import CurrentIO
##import hardware
import debugger
import processorDefinition

if processorDefinition.processor == "Lime":
	import gpioDriverLime as gpio
elif processorDefinition.processor == "BBB":
	import gpioDriverBBB as gpio

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
		print(str(value))


class JCmdHysteresisSet(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "hysteresis_set"
		register(self)
		
	def processCommand(self, value):
		configuration.Parameters.Hysteresis = int(value)

class JCmdControlInputSet(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "control_input_set"
		register(self)
		
	def processCommand(self, value):
		configuration.Parameters.ControlInput = GetElementFromName(value)

	
class JCmdCollectionPeriodSet(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "collection_period_set"
		register(self)
		
	def processCommand(self, value):
		configuration.Parameters.CollectionPeriod = value
	
	
class JCmdUnitsSet(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "units_set"
		register(self)
		
	def processCommand(self, value):
		configuration.Parameters.Units = value

class JCmdOutputMode(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "output_manual_mode"
		register(self)
		
	def processCommand(self, value):	
		if value:
			CurrentIO.ShouldControl = True			
		else:			
			CurrentIO.ShouldControl = False
			
class JCmdManualOutput(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "output_manual"
		register(self)
		
	def processCommand(self, value):
		if value == "toggle":						
			CurrentIO.toggleOutputState('controlOutput')							
			level = 0
			if CurrentIO.getOutputState('controlOutput'):
				level = 1
			gpio.outputLevel("Fan", level)		
		
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
		
		setPoint = configuration.Parameters.SetPoint
		controlInput = configuration.Parameters.ControlInput
		controlInputName = configuration.InputList[controlInput].Name
		
		controlDict = {'set_point_input_name': unicodeHelper.getAscii(controlInputName), 'set_point_value': setPoint}
		
		dataDict = {
					'secret':'badass', 
					'target':'periodic_update', 
					'value': { 
								'control': controlDict								
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
		
class JCmdCurrentTemp1Set(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "current_probe_1"
		register(self)
		
	def processCommand(self, value):
		configuration.Parameters.CurrentTempList[0] = GetElementFromName(value)
		
class JCmdCurrentTemp2Set(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "current_probe_2"
		register(self)
		
	def processCommand(self, value):
		configuration.Parameters.CurrentTempList[1] = GetElementFromName(value)

class JCmdCreateNewLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "create_new_log"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):
		if len(value):			
			recorder.startRecording(value)				
			return "result=success"
		
	
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
		register(self)
		
	def processCommand(self, value):
		recorder.deleteRecording(value)
		
class JCmdShowSavedLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "show_saved_log"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):		
		logIndex = value.split("_")[1]
		return recorder.getRecordingDetailsByIndex(logIndex)		
				
class JCmdEditProbeDetails(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "edit_probe_details"
		self.hasReturnValue = True
		register(self)
		
	def processCommand(self, value):
		probeNumber = value[-1]
		probe = configuration.InputList[int(probeNumber)]	
		response = {'probe_name': str(probe.Name), 'probe_type': str(probe.Type), 'probe_number': str(probeNumber)}		
		messageString = placeResponseInMessage(response, self.key)
		return messageString
		
class JCmdEditProbeUpdate(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self)
		self.key = "edit_probe_update"
		register(self)
		
	def processCommand(self, value):		
		probeDetails = value
		probeNumberArray = unicodeHelper.getValue(probeDetails, 'probe_number').split('_')
		probeNumber = int(probeNumberArray[-1]) - 1
		configuration.InputList[probeNumber].Name = unicodeHelper.getValue(probeDetails,'probe_name')
		configuration.InputList[probeNumber].Type =unicodeHelper.getValue(probeDetails,'probe_type')	
		configuration.Save()

class JCmdSetUnits(JsonCommand):
	def __init__(self):	
		JsonCommand.__init__(self)
		self.key = "units"		
		register(self)
		
	def processCommand(self, value):
		if value == "farenheit":
			configuration.Parameters.Units = "F"
		elif value == "celcius":
			configuration.Parameters.Units = "C"
		
class JCmdSetStoragePeriod(JsonCommand):
	def __init__(self):	
		JsonCommand.__init__(self)
		self.key = "storage_period"
		register(self)
		
	def processCommand(self, value):
		configuration.Parameters.StoragePeriod = value
		
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
		print "a"
		if value != "existing":
			print "b"
			value_list = value.split(",")
			if len(value_list) == 2:
				print "c"
				os.system("~/update_login.sh {0} {1}".format(value_list[0], value_list[1]))
				os.system("~/build_interface.sh")
		#os.system("~/reset_interface.sh client")

		
jcmdLogin = JCmdLogin();
jcmdHysteresisSet = JCmdHysteresisSet()
jcmdControlInputSet = JCmdControlInputSet()
jcmdCollectionPeriodSet = JCmdCollectionPeriodSet()
jcmdUnitsSet = JCmdUnitsSet()
jcmdSetPointSet = JCmdSetPointSet()
jcmdControlOutputSet = JCmdControlOutputSet()
JCmdCurrentTemp1Set = JCmdCurrentTemp1Set()
JCmdCurrentTemp2Set = JCmdCurrentTemp2Set()
jcmdMenuRequest = JCmdMenuRequest()
jcmdEditProbeDetails = JCmdEditProbeDetails()
jCmdEditProbeUpdate = JCmdEditProbeUpdate()
jCmdCreateNewLog = JCmdCreateNewLog()
jCmdFinishCurrentLog = JCmdFinishCurrentLog()

jCmdDeleteLog = JCmdDeleteLog()
jCmdShowSavedLog = JCmdShowSavedLog()
jCmdGraphLog = JCmdGraphLog()
jCmdManualOutput = JCmdManualOutput()
jCmdOutputMode = JCmdOutputMode()

jCmdSetStoragePeriod = JCmdSetStoragePeriod()
jCmdSetUnits = JCmdSetUnits()
	
	
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

	
