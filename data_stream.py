
#meat_temp_value =               { "action": "register_control",   "data_stream": "meat_temperature",           "control": "meat_temperature_string",    "value_type": "text"}

player_token =  { "action": "register_control",   "data_stream": "player_token", "control": "button", "value_type": "button"}
clear_board =  { "action": "register_control",   "data_stream": "clear_board", "control": "button", "value_type": "button_clear"}


registration_list = [player_token, clear_board]

master_streams_list = []

def register_stream(new_stream):

    duplicate = False

    for stream in master_streams_list:
        if stream["data_stream"] == new_stream["data_stream"]:
            duplicate = True
            break

    if duplicate == False:
        master_streams_list.append(new_stream)


player_tokens = [ 'X', 'O']

def get_latest_value(stream, player):
    result = ""

    if stream == "player_token":
        result = player_tokens[player-1]
    if stream == 'clear_board':
        result = 0
    
    return result

def create_data_stream_message(stream, player):
    value = get_latest_value(stream['data_stream'], player)
    control = stream['control']
    value_type = stream['value_type']
    message = {'control': control, 'value': value, 'value_type': value_type}
    return message

def update_all_streams(player):
    update_message_list = []
    for stream in master_streams_list:
        message = create_data_stream_message(stream, player)
        update_message_list.append(message)
    return update_message_list

def register_all_streams():
    
    for item in registration_list:
        register_stream(item)

def get_json(stream_name, player):
    result = ""
    for stream in master_streams_list:        
        if stream_name == stream['data_stream']:
            
            result = create_data_stream_message(stream, player)
            stream_update_list = []
            stream_update_list.append(result)
            message = {
                            'secret':'badass',
                            'target':'magic',
                            'value': stream_update_list
            }
            
    return str(message)

