
serverControl = None

def setQueue(queue):
	if serverControl != None:
		serverControl.setQueue(queue)

def firstPass():
	if serverControl != None:
		return serverControl.isFirstPass()

def clearFirstPass():
	if serverControl != None:
		serverControl.clearFirstPass()

def callDispatch():
	if serverControl == None:
		print "serverControl == None"
	print "attempting to dispatch"
	if serverControl != None:
		print "smokerControl.callDispatch()"
		serverControl.callDispatch()

def setServerControl(sc):
	serverControl = sc
	if sc == None:
		print "sc == None"

	if serverControl == None:
		print "serverControl == None"