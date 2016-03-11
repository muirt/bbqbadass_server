filename = "fake.csv"

out_file = open(filename, "w")




Year = 2016
Month = 3
Day = 10

Hour = 10
Minute = 29
Second = 37

for index in range(10000):
	Second += 1
	if Second == 60:
		Second = 0
		Minute += 1
		if Minute == 60:
			Hour += 1
			Minute = 0
			if Hour == 24:
				Day += 1
				Hour = 0
				if Day == 31:
					Month += 1
					Day = 0

	timestamp = "{0}-{1}-{2}T{3}:{4}:{5}.000000".format(Year, format(Month, "02"),  format(Day,"02"), format(Hour, "02"), format(Minute, "02"), format(Second, "02"))

	out_file.write("100,300,{0}\n".format(timestamp))