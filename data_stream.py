
meat_temp_value =               { "action": "register_control",   "data_stream": "meat_temperature",           "control": "meat_temperature_string",    "value_type": "text"}
grill_temp_value =              { "action": "register_control",   "data_stream": "grill_temperature",          "control": "grill_temperature_string",   "value_type": "text"}
fan_state =                     { "action": "register_control",   "data_stream": "fan_state",                  "control": "fan_state",                  "value_type": "bool"}
fan_control_state =             { "action": "register_control",   "data_stream": "fan_control_state",          "control": "fan_control_state",          "value_type": "int" }
grill_set_point =               { "action": "register_control",   "data_stream": "set_point",                  "control": "set_point_string",           "value_type": "text"}
cook_time =                     { "action": "register_control",   "data_stream": "cook_time",                  "control": "cook_time_string",           "value_type": "text"}
hysteresis =                    { "action": "register_control",   "data_stream": "hysteresis",                 "control": "hysteresis_input",           "value_type": "val" }
meat_temperature_goal =         { "action": "register_control",   "data_stream": "meat_temperature_goal",      "control": "goal_meat_input",            "value_type": "val" }
temperature_units =             { "action": "register_control",   "data_stream": "temperature_units",          "control": "temperature_units_switch",   "value_type": "bool"}
current_recording_name =        { "action": "register_control",	  "data_stream": "current_recording_name",     "control": "current_recording_name",     "value_type": "text"}
current_recording_date =        { "action": "register_control",	  "data_stream": "current_recording_date",     "control": "current_recording_date",     "value_type": "text"}
current_recording_duration =    { "action": "register_control",   "data_stream": "current_recording_duration", "control": "current_recording_duration", "value_type": "text"}
current_recording_state =       { "action": "register_control",   "data_stream": "recording_state",            "control": "current_recording_buttons",  "value_type": "bool"}

registration_list = [ meat_temp_value,
                    grill_temp_value,
                    fan_state,
                    fan_control_state,
                    grill_set_point,
                    cook_time,
                    hysteresis,
                    meat_temperature_goal,
                    temperature_units,
                    current_recording_name,
                    current_recording_date,
                    current_recording_duration,
                    current_recording_state
                    ]

master_streams_list = []

def register_stream(new_stream):

	duplicate = False

	for stream in master_streams_list:
		if stream["data_stream"] == new_stream["data_stream"]:
			duplicate = True
			break

	if duplicate == False:
		master_streams_list.append(new_stream)


def get_latest_value(stream):
    result = ""

    if stream == "meat_temperature":
        result = "170"
    elif stream == "grill_temperature":
        result = "250"
    elif stream == "fan_state":
        result = "true"
    elif stream == "fan_control_state":
        result = 0
    elif stream == "set_point":
        result = "235"
    elif stream == "cook_time":
        result = "0h04m"
    elif stream == "hysteresis":
        result = "4"
    elif stream == "meat_temperature_goal":
        result = "201"
    elif stream == "temperature_units":
        result = "true"
    elif stream == "current_recording_name":
        result = "pork"
    elif stream == "current_recording_date":
        result = "2016-03-19"
    elif stream == "current_recording_duration":
        result = "0h04m"
    elif stream == "recording_state":
        result = "true"
    return result

def create_data_stream_message(stream):
    value = get_latest_value(stream['data_stream'])
    control = stream['control']
    value_type = stream['value_type']
    message = {'control': control, 'value': value, 'value_type': value_type}
    return message

def update_all_streams():
    update_message_list = []
    for stream in master_streams_list:
        message = create_data_stream_message(stream)
        update_message_list.append(message)
    return update_message_list

def register_all_streams():
    for item in registration_list:
        register_stream(item)

def get_json(stream_name):
    result = ""
    for stream in master_streams_list:
        if stream_name == stream['data_stream']:
            result = create_data_stream_message(stream)
            stream_update_list = []
            stream_update_list.append(result)
            message = {
                            'secret':'badass',
                            'target':'magic',
                            'value': stream_update_list
            }

    return message

