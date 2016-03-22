import filesystem
import unicodeHelper
import timeHelper
import configuration

def getDataset(log):
	dataDict = {}
	fs = filesystem.filesystem()

	if fs.file_exists(log):

		data = fs.read_from_file(log)

		for index in range(len(data)):
			data[index][2] = data[index][2].replace(" ", "T")
			
		dataDict = {"title": unicodeHelper.getAscii(log), "graphData": data}

	return str(dataDict)

def get_all_files():
	fs = filesystem.filesystem()

	return fs.list_all_files() 

NAME_ELEMENT = 0
FILE_ELEMENT = 1
TIME_ELEMENT = 2   
DATE_ELEMENT = 3

def get_log_file_details():
	NAME_ELEMENT = 0
	FILE_ELEMENT = 1
	TIME_ELEMENT = 2   
	DATE_ELEMENT = 3

	logs = get_all_files()

	log_dict_list = []   
	fs = filesystem.filesystem()   
	for log in logs:
		log_filename = "{0}.csv".format(log)
		header = fs.read_header_from_file(log_filename)

		log_dict = {}
		log_dict["name"] = header[NAME_ELEMENT]
		log_dict["file"] = header[FILE_ELEMENT]
		log_dict["date"] = header[TIME_ELEMENT].split(" ")[0]

		last_line_list = fs.get_last_line_list(log_filename)

		log_length_sec = timeHelper.get_time_difference(last_line_list[TIME_ELEMENT], header[TIME_ELEMENT])

		time_string = "{0}h{1}m".format(int(log_length_sec/3600), format((int(log_length_sec)/60) % 60,"02"))

		log_dict["duration"] = time_string

		log_dict_list.append(log_dict)

	return log_dict_list

def get_current_log_file_details():
	log_filename = "{0}".format(configuration.Parameters.CurrentRecordingName)
	fs = filesystem.filesystem()   
	header = fs.read_header_from_file(log_filename)

	log_dict = {}
	log_dict["name"] = header[NAME_ELEMENT]
	log_dict["file"] = header[FILE_ELEMENT]
	log_dict["date"] = header[TIME_ELEMENT].split(" ")[0]

	last_line_list = fs.get_last_line_list(log_filename)

	log_length_sec = timeHelper.get_time_difference(last_line_list[TIME_ELEMENT], header[TIME_ELEMENT])

	time_string = "{0}h{1}m".format(int(log_length_sec/3600), format((int(log_length_sec)/60) % 60,"02"))

	log_dict["duration"] = time_string
	
	return log_dict