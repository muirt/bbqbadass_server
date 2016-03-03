import configuration
import CurrentIO
import unicodeHelper

def updateGUI():
	fan_control = ''
	hysteresis = configuration.Parameters.Hysteresis
	setPoint = configuration.Parameters.SetPoint
	goal_temp = configuration.Parameters.MeatTemperatureGoal
	if CurrentIO.ShouldControl:
		fan_control = 'auto'
	else:
		if CurrentIO.getOutputState('controlOutput'):
			fan_control = 'on'
		else:
			fan_control = 'off'


	temp_units = configuration.Parameters.Units;
	controlInput = configuration.Parameters.ControlInput
	controlInputName = configuration.InputList[controlInput].Name
	currentTempList = configuration.Parameters.CurrentTempList
	currentTempName1 = str(configuration.InputList[currentTempList[0]].Name)
	currentTempName2 = str(configuration.InputList[currentTempList[1]].Name)
	dataListDict = {	
						'secret': 'badass', 
						'target': 'initial_update', 
						'value': {
							'set_point_input_name':str(controlInputName),
							'set_point_value':setPoint,
							'current_temp_1_name':currentTempName1,
							'current_temp_2_name':currentTempName2,
							'fan_control':fan_control,
							'hysteresis':hysteresis,
							'meat_temperature_goal': goal_temp,
							'temperature_units': unicodeHelper.getAscii(temp_units)
							}
					}
	
	return str(dataListDict)