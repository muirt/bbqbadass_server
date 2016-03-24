import json
import configuration
import unicodeHelper
import MReq
import datetime
import time
import CurrentIO
import os
import updateGUI
import averager
import tempUtilities
import filesystem
import grapher
import data_stream
from jsonCommand import JsonCommand

import processorDefinition
if processorDefinition.processor == "BBB":
	import gpioDriverBBB as gpio
elif processorDefinition.processor == "Lime":
	import gpioDriverLime as gpio


class JCmdHysteresisSet(JsonCommand):
	def __init__(self):
								  #      key,     hasReturnValue
		JsonCommand.__init__(self, "hysteresis_change",True)
				
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
		JsonCommand.__init__(self, "meat_temperature_goal", True)
		
	def processCommand(self, value):
		if int(value):
			configuration.Parameters.MeatTemperatureGoal = int(value)		
		#print configuration.Parameters.MeatTemperatureGoal
		configuration.Save()		
		goal_temp = str(configuration.Parameters.MeatTemperatureGoal)			
		result = placeResponseInMessage('meat_temperature_goal', goal_temp, 'response')				
		return str(result)	


class JCmdCollectionPeriodSet(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self, "collection_period_set", False)
		
	def processCommand(self, value):
		configuration.Parameters.CollectionPeriod = value
	

class JCmdOutputMode(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self, "output_mode", False)
		
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
		JsonCommand.__init__(self, "set_point", True)		

		
	def processCommand(self, value):
		if value == 'up':
			configuration.Parameters.SetPoint += 1
		if value == 'down':
			if configuration.Parameters.SetPoint >= 0:
				configuration.Parameters.SetPoint -= 1
		configuration.Save()
			
		message = data_stream.get_json('set_point')		

		message['value'][0]['value'] = 237

		return str(message)	
		
'''
	error dialog

		messageDict = {'title': 'Error', 'body': 'you cant do that!', 'button': 'OK'}
		result = placeResponseInMessage('message', messageDict, 'error')
		print str(result)
'''


class JCmdControlOutputSet(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self, "control_output_set", False)
		
	def processCommand(self, value):
		configuration.Parameters.ControlOutput = value

class JCmdCreateNewLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self, "create_new_log", True)
		
	def processCommand(self, value):	
		fs = filesystem.filesystem()

		validFileName = value.replace(" ", "_")
		exists = fs.file_exists(validFileName + ".csv")
		
		result = ""
		
		if exists:
			messageDict = {'title': 'Error', 'body': 'File Exists', 'button': 'OK'}
			result = placeResponseInMessage('message', messageDict, 'error')
			return result		

		
		right_now = str(datetime.datetime.now())

		header_list = []
		header_list.append(value)
		header_list.append(validFileName) 
		header_list.append(right_now)

		
		for index in range(len(header_list)):
			header_list[index] = unicodeHelper.getAscii(header_list[index])
		

		fs = filesystem.filesystem()
		fs.write_to_file(validFileName, header_list)
		
		os.system("./link_csv.sh " + validFileName + ".csv")	

		# configuration.Parameters.CurrentRecordingName = validFileName
		# configuration.Parameters.CurrentlyRecording = True


		log_dict_list = grapher.get_log_file_details()
		
		result = placeResponseInMessage("logs", str(log_dict_list), 'saved_logs')
		return result
	
class JCmdFinishCurrentLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self, "finish_current_log",True)
		
		
	def processCommand(self, value):
		#recorder.finishRecording()   #phant TODO
		emptyDict = {'name': 'Not', 'time': 'Recording'}
		result = placeResponseInMessage("details", str(emptyDict) , 'recording')
		return result	
			
class JCmdDeleteLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self, "delete_log", True)
		
	def processCommand(self, value):
		
		if ".csv" in value:
			delete_cmd = "/home/olimex/bbqbadass_server/{0}".format(value)
			delete_ln = "/var/www/bbq_badass_webapp_bootstrap/{0}".format(value)
			
			os.remove(delete_cmd)
			os.remove(delete_ln)
			

		log_dict_list = grapher.get_log_file_details()
		
		result = placeResponseInMessage("logs", str(log_dict_list), 'saved_logs')
		return result
			
	
class JCmdShowLogs(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self, "list_logs", True)
		
	def processCommand(self, value):	
		pass
			
class JCmdShowSavedLog(JsonCommand):
	def __init__(self):
		JsonCommand.__init__(self, "show_saved_log", True)
		
	def processCommand(self, value):	
		logIndex = value.split("_")[1]
		details = recorder.getRecordingDetailsByIndex(logIndex)  #phant TODO
		result = placeResponseInMessage(str(details), 'saved_recording_details')
		return result		
	
class JCmdGraphLog(JsonCommand):
	def __init__(self):	
		JsonCommand.__init__(self, "graph_log", True)
		
	def processCommand(self, value):		
		dataset = grapher.getDataset(value) 
		return placeResponseInMessage('graph_data', dataset, 'graphing')
		
class JCmdMenuRequest(JsonCommand):
	def __init__(self):	
		JsonCommand.__init__(self, "menu_request", True)
		
	def processCommand(self, value):
		result = None
		if value in MReq.MReqDictionary.keys():
			result = MReq.MReqDictionary[value].GetMenuData()		
		#str(result)

		return result

class JCmdLogin(JsonCommand):
	def __init__(self):	
		JsonCommand.__init__(self,"login",False)
		
	def processCommand(self, value):
		if value != "existing":
			value_list = value.split(",")
			if len(value_list) == 2:
				os.system("~/update_login.sh {0} {1}".format(value_list[0], value_list[1]))
		os.system("~/reset_interface.sh client")

class JCmdUnitSet(JsonCommand):
	def __init__(self):	
		JsonCommand.__init__(self, "units",False)
		
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


def placeResponseInMessage(string, val, key):

	messageDict = {
			'secret':'badass', 
			'target':key, 
			'value': { 
						string: val
					  }
			}
	return  str(messageDict).replace('"', ' ')




jcmdSetPointSet = JCmdSetPointSet()
jCmdUnitSet = JCmdUnitSet()
jcmdMeatTempGoal = JCmdMeatTempGoal()		
jcmdLogin = JCmdLogin()
jcmdHysteresisSet = JCmdHysteresisSet()
jcmdCollectionPeriodSet = JCmdCollectionPeriodSet()
jcmdMenuRequest = JCmdMenuRequest()
jCmdCreateNewLog = JCmdCreateNewLog()
jCmdFinishCurrentLog = JCmdFinishCurrentLog()
jCmdDeleteLog = JCmdDeleteLog()
JCmdShowLogs = JCmdShowLogs()
jCmdShowSavedLog = JCmdShowSavedLog()
jCmdGraphLog = JCmdGraphLog()
jCmdOutputMode = JCmdOutputMode()