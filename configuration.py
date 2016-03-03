import json
import os.path

class Parameters:
	CollectionPeriod = 3
	StoragePeriod = 3
	SetPoint = 225
	Hysteresis = 3
	ControlInput = 1
	ControlOutput = 0
	CurrentTempList = []
	OnState = True	
	MeatTemperatureGoal = 203	
	Units = "F"
	
	def Serialize(self):
		configString = json.dumps(
		{
			"CollectionPeriod" : self.CollectionPeriod,
			"StoragePeriod" : self.StoragePeriod,
			"SetPoint" : self.SetPoint,
			"Hysteresis" : self.Hysteresis,
			"ControlInput" : self.ControlInput,
			"ControlOutput" : self.ControlOutput,
			"OnState": self.OnState,
			"CurrentTempList": self.CurrentTempList,
			"MeatTemperatureGoal": self.MeatTemperatureGoal,
			"Units": self.Units
		})           
		return configString
    	
	def Deserialize(self, jsonString):
		data = json.loads(jsonString)
		self.CollectionPeriod = data["CollectionPeriod"]
		self.StoragePeriod = data["StoragePeriod"]		
		self.SetPoint = data["SetPoint"]
		self.Hysteresis = data["Hysteresis"]
		self.ControlInput = data["ControlInput"]
		self.ControlOutput = data["ControlOutput"]
		self.OnState = data["OnState"]
		self.CurrentTempList = data["CurrentTempList"]
		self.MeatTemperatureGoal = data["MeatTemperatureGoal"]
		self.Units = data["Units"]

class InputRecord:

	Name = ""
	MultiplexerChannel = 0
	    
	def Serialize(self):
		return json.dumps(
		{            
			"Name" : self.Name,			
			"MultiplexerChannel" : self.MultiplexerChannel,
		})       
        
	def Deserialize(self, jsonString):
		data = json.loads(jsonString)
		self.Name = data["Name"]				
		self.MultiplexerChannel = data["MultiplexerChannel"]
		        

Parameters = Parameters()
InputList = []
FileName = "config1.json"


def Serialize():
    configString = '{ "Parameters" :' + Parameters.Serialize()
    if len(InputList) != 0:
        configString += ', "InputRecords": ['
        for input in InputList:
            configString += input.Serialize()
            if input != InputList[-1]:
                configString += ','
        configString += ']'
    configString += '}'
    return configString;

def Deserialize(jsonString):
    data = json.loads(jsonString)
    Parameters.Deserialize(json.JSONEncoder().encode(data["Parameters"]))
    del InputList[:]
    for inputJson in data["InputRecords"]:
        inputRecord = InputRecord()
        inputRecord.Deserialize(json.JSONEncoder().encode(inputJson))
        InputList.append(inputRecord)

def Save():
    configString = Serialize()
    configFile = open(FileName, "w")
    configFile.write(configString)
    configFile.close()

def Load():
    if(os.path.isfile(FileName)):
        configFile = open(FileName, "r")
        configString = ' '.join(configFile.readlines())
        Deserialize(configString)
        configFile.close()
    else:
        CreateDefault()

def CreateDefault():
    inputRecord1 = InputRecord()
    inputRecord2 = InputRecord()
    inputRecord1.Name = "Meat"
    inputRecord1.MultiplexerChannel = 0
    inputRecord2.Name = "Grill"    
    inputRecord2.MultiplexerChannel = 1
    InputList.append(inputRecord1)
    InputList.append(inputRecord2)
    Parameters.CollectionPeriod = 3
    Parameters.StoragePeriod = 3    
    Parameters.SetPoint = 50
    Parameters.Hysteresis = 3
    Parameters.ControlInput = 1
    Parameters.ControlOutput = 0
    Parameters.OnState = True
    Parameters.CurrentTempList = [0,1]
    Parameters.MeatTemperatureGoal = 203
    Parameters.Units = "F"
    Save()
