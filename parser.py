import configuration
import unicodedata
import json
import jCmd
import debugger
    

def JsonParse(payload):	
	result = None
	resultListString = ""
	resultList = []
	jsonObject = json.loads(payload)

	for key in jCmd.jCmdDictionary.keys():
		if jsonObject.has_key(key):		
			result = jCmd.process(key, jsonObject[key])			
			
	return result