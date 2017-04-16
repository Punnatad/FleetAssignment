import csv
import string
import copy

flight = []
turnTime = 30 #depends on Aircraft Type -- A319 = 30 mins
AircraftType = []
Max_AirType = []
flight_scheduled = []

def readToArray(file):
	lines = []
	for line in file.xreadlines():
		lines.append(string.split(line, ','))
	return lines

def convertToMin(timeString):
	#print "before : " + str(timeString)
	if len(timeString) == 3:
		timeString = "0" + str(timeString)

	#print "after : " + str(timeString) + "\n"
	hour = timeString[0]+timeString[1]
	minute = timeString[2]+timeString[3]
	#print "hour : " + hour + " minute : " + minute
	hourMin = int(hour)*60
	#print "hourMin : " , hourMin
	minMin = int(minute)
	#print "minMin : " , minMin
	totalMin = hourMin + minMin
	#print "totalMin : " , totalMin
	return totalMin

def convertToTimeString(minTime):
	hour = minTime/60
	minute = minTime%60
	if minute == 0:
		minute = "0"+str(minute)
	time = str(hour) + ":" + str(minute)
	return time

def toDefaultTimeFormat(flight):
	#print "check toDefaultTimeFormat"
	for i in range(len(flight)):
		if i > 0:
			#print type(flight[i][4])

			if int(flight[i][5]) > 1440:
				#print "To Default --- > "
				t = int(flight[i][5]) - 60*24
				#print flight[i]
				#print str(flight[i][0]) + " -- " + str(flight[i][5]) + " >>>>>> " +str(t)

				flight[i][5] = t

			for j in range(len(flight[i])):
				if j == 4 or j == 5 :
					temp = flight[i][j]
					t_hour = temp/60
					t_min = temp%60
					if t_hour < 10 :
						t_hour = "0" + str(t_hour)
					else :
						t_hour = str(t_hour)
					if t_min < 10 :
						t_min = "0" + str(t_min)
					else :
						t_min = str(t_min)
					temp = t_hour + t_min
					flight[i][j] = temp



# --------------------- Scheduling ---------------------------------------

def schedule_Flight(flight):
	#Max_AirType = [1]*len(AircraftType)

	flight_scheduled = [""]*len(flight)
	count = 1
	h = 1
	w = len(AircraftType)
	print "AircraftType : " + str(w) + "\n"
	multiCount = [["" for x in range(h)] for y in range(w)]
	for i in range(w):
		multiCount[i][0] = 1

	for i in range(len(flight)):
		if i > 0:
			for j in range(len(flight)):
				if j > i:
					if flight[i][5] + turnTime <= flight[j][4]:
						if flight[i][3] == flight[j][2] and flight[i][1] == flight[j][1] and (flight_scheduled[j] == ""):
							if flight_scheduled[i] == "" :

								#print " ########## ", flight[i]

								for k in range(len(AircraftType)):
									if flight[i][1] == AircraftType[k]:
										flight_scheduled[i] = multiCount[k][0]
										flight_scheduled[j] = multiCount[k][0]
										multiCount[k][0] += 1
										#Max_AirType[k] += 1
								break
							else :
								#print " >>>>>>>> ", flight[i]

								flight_scheduled[j] = flight_scheduled[i]
								break
			if flight_scheduled[i] == "" :
				#print "\n _>_>_>_>_>_>_>_>_  ", flight[i]
				for k in range(len(AircraftType)):
					if flight[i][1] == AircraftType[k]:

						flight_scheduled[i] = multiCount[k][0]
						#print str(flight_scheduled[i]) + "\n"
						multiCount[k][0] += 1


	#----- DEFINE LAST AIRCRAFT OF EACH TYPE
	Max_AirCraft = [1]*len(AircraftType)

	for i in range(len(flight_scheduled)):
		for j in range(len(AircraftType)):
			if i > 0 and flight[i][1] == AircraftType[j]:
				if flight_scheduled[i] > Max_AirCraft[j]:
					if flight_scheduled[i] == '': #------ IF FLIGHT[i] HAS NO PAIR

						#print "null flight : " + str(flight[i])
						Max_AirCraft[j] +=1
						#print "Max_AirCraft - " + str(flight[i][1]) + " : " + str(Max_AirCraft[j])
						flight_scheduled[i] = int(Max_AirCraft[j])
						#print flight_scheduled[i]

						#print "\n"
					else:
						Max_AirCraft[j] = flight_scheduled[i]

	#----- PRINT NUMBERS OF EACH AIRCRAFT_TYPE
	print "Numbers of Aircraft:"
	for i in range(len(AircraftType)):
		print AircraftType[i] + " : " + str(Max_AirCraft[i])


	#----- ASSIGN FLEET_SCHEDULED TO FLIGHT
	for i in range(len(flight_scheduled)):
		if i == 0:
			flight[i].append('Aircraft No')
		if i > 0:
			flight[i].append(flight_scheduled[i])
			#print "FlightNo. : " + str(flight[i][0]) + " - AircraftNo. : " + str(flight_scheduled[i])

	#print "\n"


	print("\n--------------------------------------------------\n")



# --------------------- Main ---------------------------------------

def main():

# --------------------- Read & Write CSV ---------------------------------------

	# Read csv file to list
	file = open("Planner_BkkAirways_Rev.csv", "rb")
	flight = readToArray(file)
	#flight.pop(0)

	#for i in range (len(flight)):
		#print flight[i]

	for i in range(len(flight)):
		flight[i][6] = flight[i][6].replace("\r\n","")


	for i in range( len(flight) ):
		if i > 0 :
			flight[i][4] = convertToMin(flight[i][4])
			flight[i][5] = convertToMin(flight[i][5])

			if flight[i][5] < flight[i][4]:
				"""
				print "CHANGE AT FIRST"
				print flight[i]
				print "flight : " + flight[i][0] + " -->>>> "+ str(flight[i][4]),str(flight[i][5])
				"""
				temp = int(flight[i][5]) + 60*24
				#print "temp : " + str(temp)
				flight[i][5] = temp
				#print "flight[i][5] : " + str(flight[i][5]) + "\n"
				#print flight[i]

		#----- Count AircraftType
		if flight[i][1] not in AircraftType and i > 0:
			AircraftType.append(flight[i][1])



	print("\n--------------------------------------------------\n")

	temp = flight[0]
	#print "temp :  " + str(temp)
	flight.pop(0)
	flight.sort(key=lambda tup: tup[4])
	flight.insert(0,temp)

	"""
	for i in range (len(flight)):
		print flight[i]
	"""
	schedule_Flight(flight)

	toDefaultTimeFormat(flight)

	for i in range (len(flight)):
		if i > 0:
			print flight[i]

	# Write list to csv file
	out = open("Main_Output.csv", "wb")
	writer = csv.writer(out)
	for i in range(len(flight)):
		writer.writerow(flight[i])


# ---------------------------  ----------------------------------------
	print("\n-------------------------- DONE ------------------------\n")

if __name__ == '__main__':
	main()
