import fileinput
import sys

for arg in sys.argv:
	print arg
	
for line in fileinput.input(sys.argv[3], inplace=True):
        if sys.argv[1] in line:
                print sys.argv[2]
        else:
                print line[:-1]
