import csv
import string
import copy

flight = []
result = []
turnTime = 30 #depends on Aircraft Type -- A319 = 30 mins
AircraftType = []
Max_AirType = []
ErrorFlight = []

def readToArray(file):
	lines = []
	for line in file.xreadlines():
		lines.append(string.split(line, ','))
	return lines

def convertToMin(timeString):
	if len(timeString) == 3:
		timeString = "0"+str(timeString)
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

#---------------------- Check --------------------------------------

def CheckFlightType(result):
	#print "function IN!"
	AircraftError = True
	for i in range(len(result)):
		for j in range(len(result)):
			if i > 0 and result[i][7] == result[j][7] and result[i][0] != result[j][0] and result[i][1] == result[j][1]:
				if j > i :
					if int(result[j][4]) - int(result[i][5]) < turnTime :
						AircraftError = False
						error = [result[i][0],result[j][0]]
						if error not in ErrorFlight:
							ErrorFlight.append(error)
				if j < i :
					if int(result[i][4]) - int(result[j][5]) < turnTime :
						AircraftError = False
						error = [result[j][0],result[i][0]]
						if error not in ErrorFlight:
							ErrorFlight.append(error)

	if AircraftError == False :
		print "\n AircraftType is Invalid \n"
		for i in range(len(ErrorFlight)):
			print ErrorFlight[i]
		print "\n"
		"""
		for k in range(len(ErrorFlight)):
			for j in range(len(flight)):
				print ErrorFlight[k][0],flight[k][0]
				if ErrorFlight[k][0] == flight[j][0] or ErrorFlight[k][1] == flight[j][0]:
					print flight[j]
		"""
	else:
		print "\n AircraftType is Corrected \n"


# --------------------- Main ---------------------------------------

def main():

# --------------------- Read & Write CSV ---------------------------------------

	# Read csv file to list
	file = open("Planner_NokAir.csv", "rb")
	flight = readToArray(file)

	#file = open("Main_Output.csv","rb")
	file = open("Main_Output.csv","rb")
	result = readToArray(file)
	#flight.pop(0)

	for i in range( len(flight) ):
		if i > 0 :
			flight[i][4] = convertToMin(flight[i][4])
			flight[i][5] = convertToMin(flight[i][5])
			if flight[i][5] < flight[i][4]:
				#print "flight : " + flight[i][0] + " -->>>> "+ str(flight[i][4]),str(flight[i][5])
				temp = int(flight[i][5]) + 60*24
				#print "temp : " + str(temp)
				flight[i][5] = temp
				#print "flight[i][5] : " + str(flight[i][5]) + "\n"

	for i in range(len(result)):
		if i > 0 :
			#print result[i]
			result[i][4] = convertToMin(result[i][4])
			result[i][5] = convertToMin(result[i][5])

	print "Total Flight : " + str(len(flight)-1)
	CheckFlightType(result)






# ---------------------------  ----------------------------------------
	print("\n ----- Done ----- \n")

if __name__ == '__main__':
	main()
