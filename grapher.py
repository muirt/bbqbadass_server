import filesystem
import unicodeHelper

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