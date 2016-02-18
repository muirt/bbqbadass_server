import configuration
import unicodeHelper
import recorder
import time

class MenuRequest:

	def __init__(self):
		self.key = "baseMenuRequest"
		
	def hasKey(key):
		return self.key == key

MReqDictionary = {}

def Register(mreq):
	MReqDictionary[mreq.key] = mreq
		

		
class MReqControl(MenuRequest):	
	
	def __init__(self):
		self.key = "control"
		Register(self)
		
	def GetMenuData(self):
		choiceList = []
		probeNamesString = ""
		for input in configuration.InputList:
			choiceList.append(unicodeHelper.getAscii(input.Name)) 
		'''
		resultList.append("control_menu_input_names=" + probeNamesString)
		resultList.append("control_menu_hysteresis=" + str(configuration.Parameters.Hysteresis))
		resultList.append("control_menu_selected_input=" + str(configuration.InputList[configuration.Parameters.ControlInput].Name))
		'''
		dataDict = {'choices':choiceList, 'hysteresis':str(configuration.Parameters.Hysteresis), 'selected':str(configuration.InputList[configuration.Parameters.ControlInput].Name)}
		
		return placeResponseInMessage(str(dataDict), 'control_menu')


		
class MReqCurrentLog(MenuRequest):	
	
	def __init__(self):
		self.key = "current_log"
		Register(self)
		
	def GetElapsedTime(self, startTime):
		seconds = (int(time.time())) - int(startTime)
		timeString = "0h0m"
		if int(seconds) > 60:
			minutes = (seconds / 60) % 60
			hours = seconds/3600
			timeString = str(hours) + "h" + str(minutes) + "m"
		return timeString
		
	def GetMenuData(self):		
		return placeResponseInMessage(recorder.getCurrentRecordingDetails(), 'current_log')
		
class MReqSavedLogs(MenuRequest):	
	
	def __init__(self):
		self.key = "list_saved_logs"
		Register(self)
		
	def GetMenuData(self):
		logs = placeResponseInMessage(recorder.listAllRecordings(), 'saved_logs')		
		return logs
				

mreqSavedLogs = MReqSavedLogs()
mreqCurrentLog = MReqCurrentLog()
mreqControl = MReqControl()


def placeResponseInMessage(response, key):
	messageDict = {'secret': 'badass', 'target': key, 'value': response}
	return  str(messageDict).replace('"', ' ')


def Process(key):
	result = None
	if MReqDictionary.has_key(key):
		result = MReqDictionary[key].GetMenuData()
	return result
		