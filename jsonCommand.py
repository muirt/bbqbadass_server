class JsonCommand:
	
	def __init__(self, key, hasReturnValue):
		self.key = key
		self.hasReturnValue = hasReturnValue	
		register(self)	
			
	def hasKey(self, key):
		return self.key == key
		
	def processCommand(self, value):
		pass

jCmdDictionary = {}
			
#every class' init function must register itself in the dictionary
def register(jcmd):	
	jCmdDictionary[jcmd.key] = jcmd

def process_command(key, value):
	return jCmdDictionary[key].processCommand(value)