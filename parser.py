import configuration
import unicodedata
import json
import commands
import jsonCommand

    

def JsonParse(payload, player):	
	result = None
	resultListString = ""
	resultList = []
	jsonObject = json.loads(payload)

	for key in jsonCommand.jCmdDictionary.keys():		
		if jsonObject.has_key(key):		
			result = process(key, jsonObject[key] , player)			
		
	return result


def process(key, value, player):
	
	jCmdDictionary = jsonCommand.jCmdDictionary
	
	result = None
	if jCmdDictionary.has_key(key):		
		if(jCmdDictionary[key].hasReturnValue):
			result = jCmdDictionary[key].processCommand(value, player)
			
		else:
			jCmdDictionary[key].processCommand(value, player)
		configuration.Save()
					
	return result