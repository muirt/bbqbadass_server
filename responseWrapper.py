def placeResponseInMessage(string, val, key):

	messageDict = {
    	'secret':'badass', 
         'target':key, 
         'value': { 
                  string: val
                 }
         }
	return  str(messageDict).replace('"', ' ')