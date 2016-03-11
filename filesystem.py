import os
import csv

class filesystem():

	def __init__(self):
		pass

	def delete_file(self, name): 
		os.system("rm {0}".format(name))

	def write_to_file(self, name, list):

		if ".csv" not in name:
			name = name + ".csv"
		if os.path.exists(name):
			open_style = "a"
		else:
			open_style = "w"

		with open(name, open_style) as csvfile:
		    fieldnames = ['grill_temp', 'meat_temp', 'time']
		    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		    if(open_style == "w"):
		    	writer.writeheader()

		    field_list_dict = {}
		    for index, field in enumerate(fieldnames):
		    	field_list_dict[fieldnames[index]] = list[index]

		    writer.writerow(field_list_dict)

	def read_from_file(self, name):

		reader_list = []
		with open(name, 'rt') as f:
			reader = csv.reader(f)
			for row in reader:
				reader_list.append(row)
		return reader_list

	def list_all_files(self):
		os.system("ls *.csv > all_files.txt")
		file = open("all_files.txt", "r")
		lines = file.readlines()
		for index in range(len(lines)):
			lines[index] = lines[index].replace("\n", "")
		file.close()
		os.system("rm all_files.txt")
		return lines

	def file_exists(self, filename):
		return os.path.exists(filename)
