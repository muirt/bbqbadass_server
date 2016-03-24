import configuration
import unicodedata
import json
import commands
import jsonCommand

    

def JsonParse(payload):	
	result = None
	resultListString = ""
	resultList = []
	jsonObject = json.loads(payload)

	for key in jsonCommand.jCmdDictionary.keys():		
		if jsonObject.has_key(key):		
			result = process(key, jsonObject[key])			
		
	return result


def process(key, value):
	
	jCmdDictionary = jsonCommand.jCmdDictionary
	
	result = None
	if jCmdDictionary.has_key(key):		
		if(jCmdDictionary[key].hasReturnValue):
			result = jsonCommand.process_command(key, value)
			
		else:
			jCmdDictionary[key].processCommand(value)
			configuration.Save()
					
	return result