import datetime

def getCurrentDate():
	today = datetime.datetime.now()
	dateString = "%s-%s-%s" % (today.month, today.day, today.year)
	return dateString