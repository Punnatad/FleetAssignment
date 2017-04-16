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
	if len(timeString) == 3:
		timeString = "0"+str(timeString)
		#print timeString
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
	for i in range(len(flight)):
		if i > 0:

			if int(flight[i][5]) > 1440:
				t = int(flight[i][5]) - 60*24
				flight[i][5] = t
				
			#print type(flight[i][4])
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

			if flight_scheduled[i] == "" :
				#print "ROOT NODE"
				#print "i : " + str(i)
				fare_list = []
				count = 0
				for j in range(len(flight)):
					if j > i:
						if flight[i][5] + turnTime <= flight[j][4] and count < 3:
							if flight[i][3] == flight[j][2] and flight[i][1] == flight[j][1] and (flight_scheduled[j] == ""):
								fare_list.extend([flight[j]])
								count += 1
								"""
								#print "PAIR (" + str(i) + "," + str(j) + ")"
								print "PAIR (" + str(flight[i][0]) + "," + str(flight[j][0]) + ")"

								#----- Check Time -----
								arrTime = convertToTimeString(flight[i][5] + turnTime)
								print "[arrived] Flight No:" + flight[i][0] + " - Ready At: " + str(arrTime)
								arrTime = convertToTimeString(flight[j][4])
								print "[next] Flight No:" + flight[j][0] + " - DepTime: " + str(arrTime)
								print "------"
								"""
								#if flight[i][0] == '298':
								#	print fare_list
								key = 0
								if count == 3:
									#print "count = 3"
									print ">>> flight : " + str(flight[i])
									t = 0
									for fare in range(len(fare_list)):
										print str(fare) + " fare : " + str(fare_list[fare][6])
										#if int(fare_list[fare][6]) > int(t):
											#t = fare_list[fare][6]
											#print "----- check > t " + str(t)

									#t = max(fare_list[0][6],fare_list[1][6])
									t = max(int(fare_list[0][6]),max(int(fare_list[1][6]),int(fare_list[2][6])))
									print "T ---- > " +str(t)

									for fare in range(len(fare_list)):
										if int(fare_list[fare][6]) == int(t):
											temp_Fare = fare_list[fare]
											break
									print "Choose : " + str(temp_Fare)

									for m in range(len(flight)):
										if flight[m] == temp_Fare:
											key = m

									for k in range(len(AircraftType)):
										if flight[i][1] == AircraftType[k]:
											print "multiCount : " + str(multiCount[k][0]) + "\n"
											flight_scheduled[i] = multiCount[k][0]
											flight_scheduled[key] = multiCount[k][0]
											multiCount[k][0] += 1
											#Max_AirType[k] += 1
									break


								elif (count == 1 or count == 2) :
									#print fare_list
									#print ">>>>> Less Than 3 : " +str(flight[i][0])
									#key = 0
									print "less 3"
									print ">>> flight : " + str(flight[i])
									t = 0
									for fare in range(len(fare_list)):
										if int(fare_list[fare][6]) > int(t):
											t = fare_list[fare][6]
										print str(fare) + " fare : " + str(fare_list[fare])
									print "T ---- > " +str(t)

									for fare in range(len(fare_list)):
										if int(fare_list[fare][6]) == int(t):
											temp_Fare = fare_list[fare]
											break
									#print "fare_list : " + str(fare_list)
									print "Choose : " + str(temp_Fare)

									for m in range(len(flight)):
										if flight[m] == temp_Fare:
											#print temp_Fare
											key = m

									for k in range(len(AircraftType)):
										if flight[i][1] == AircraftType[k]:
											print "multiCount : " + str(multiCount[k][0]) + "\n"
											flight_scheduled[i] = multiCount[k][0]
											flight_scheduled[key] = multiCount[k][0]
											multiCount[k][0] += 1

											#Max_AirType[k] += 1

								"""
								for k in range(len(AircraftType)):
									if flight[i][1] == AircraftType[k]:
										flight_scheduled[i] = multiCount[k][0]
										flight_scheduled[key] = multiCount[k][0]
										multiCount[k][0] += 1
										#Max_AirType[k] += 1
								#break
								"""
			else :
				#print "CONTINUOUS NODE"
				#print "i : " + str(i)
				for j in range(len(flight)):
					if j > i:
						if flight[i][5] + turnTime <= flight[j][4]:
							#print "j : " + str(j)

							if (flight[i][3] == flight[j][2]) and (flight_scheduled[j] == "") and (flight[i][1] == flight[j][1]) :
								"""
								print "PAIR (" + str(flight[i][0]) + "," + str(flight[j][0]) + ")"
								#----- Check Time -----
								arrTime = convertToTimeString(flight[i][5] + turnTime)
								print "[arrived] Flight No:" + flight[i][0] + " - Ready At: " + str(arrTime)
								arrTime = convertToTimeString(flight[j][4])
								print "[next] Flight No:" + flight[j][0] + " - DepTime: " + str(arrTime)
								print "------"
								"""
								flight_scheduled[j] = flight_scheduled[i]

								break


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

		#print item.append()

	for i in range( len(flight) ):
		if i > 0 :
			flight[i][4] = convertToMin(flight[i][4])
			flight[i][5] = convertToMin(flight[i][5])
			if flight[i][5] < flight[i][4]:
				temp = int(flight[i][5]) + 60*24
				flight[i][5] = temp

		if flight[i][1] not in AircraftType and i > 0:
			AircraftType.append(flight[i][1])



	print("\n--------------------------------------------------\n")

	temp = flight[0]
	#print "temp :  " + str(temp)
	flight.pop(0)
	flight.sort(key=lambda tup: tup[4])
	flight.insert(0,temp)

	schedule_Flight(flight)

	toDefaultTimeFormat(flight)


	"""
	for i in range (len(flight)):
		if i > 0:
			print flight[i]
	"""



	# Write list to csv file
	out = open("Fare_output.csv", "wb")
	writer = csv.writer(out)
	for i in range(len(flight)):
		writer.writerow(flight[i])


# ---------------------------  ----------------------------------------
	print("\n-------------------------- DONE ------------------------\n")

if __name__ == '__main__':
	main()
