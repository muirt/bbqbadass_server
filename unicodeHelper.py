import unicodedata

def getValue(dictionary, key):
	value = None
	unicodeKey = unicode(key)
	
	if dictionary.has_key(unicodeKey):		
		unicodeValue = dictionary[unicodeKey]	
		value = unicodedata.normalize('NFKD', unicodeValue).encode('ascii', 'ignore')
	return value
				
def getAscii(unicodeString):
	ascii = unicodeString
	if isinstance(unicodeString,unicode):
		ascii = unicodedata.normalize('NFKD', unicodeString).encode('ascii', 'ignore')
	return ascii