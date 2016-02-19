import unicodeHelper
import debugger
import recorder
import configuration

def getDataset(log):

	logNameString = None	
	inputsObject = None
	outputsObject = None
		
	if log == "current":
		inputsObject = recorder.getAllReadingsFromCurrentRecording("input")
		outputsObject = recorder.getAllReadingsFromCurrentRecording("output")
		logNameString = unicodeHelper.getAscii(recorder.getCurrentRecordingName())
	else:			
		inputsObject = recorder.getAllReadingsFromRecording(log, "input")
		outputsObject = recorder.getAllReadingsFromRecording(log,"output")
		logNameString = unicodeHelper.getAscii(log)
	dataset = []

	if inputsObject:
		minTime = inputsObject.rows[0].value["time"]
		
		
	dataSetDict = {}
	for row in inputsObject.rows:
		minutes = int((row.value["time"] - minTime)/60	)		
		inputList = row.value["inputs"]
		inputCount = 0
		for inputRecord in inputList:					
			inputRecord['name'] = configuration.InputList[inputCount].Name 
			inputCount += 1
			graphTuple = [minutes,inputRecord['state'], 1]
	
			if inputRecord['name'] not in dataSetDict:				
				dataSetDict[inputRecord['name']] = []
			dataSetDict[inputRecord['name']].append(graphTuple)
	
	seriesIndex = 0
		
	dataDict = {"title": logNameString, "graphData": []}
	
	for key in dataSetDict.keys():
		series = {"data" : "", "label": ""}
		series["data"] = unicodeHelper.getAscii(str(dataSetDict[key]))
		series["label"] = unicodeHelper.getAscii(key)
		dataDict["graphData"].append(series)		
	
	
	return str(dataDict)

		
		
	