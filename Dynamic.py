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

#----------------------- DYNAMIC ----------------


def Dynamic_Flight(flight):
	n = len(flight)
	t = [0]*len(flight)
	key = ['']*len(flight)
	queue = []
	t[0] = int(flight[0][6])
	temp = []
	path = []
	zz = []
	for i in range(1,len(flight)):
		if (len(flight[i]) == 7):
			t[i] = max(int(t[i]-1), int(flight[i][6]))
			for j in range(i-1,-1,-1):
				#----- CHECK DEP & ARR TIME and CHECK ORIGIN - DESTINATION AIRPORT
				if int(flight[j][5]) + turnTime <= int(flight[i][4]) and str(flight[i][2]) == str(flight[j][3]):
					#print "flight  " + str(j+1) + " : " + str(flight[j])
					#print "flight  " + str(i+1) + " : " + str(flight[i])
					key[i] = [str(flight[j][0]),str(flight[i][0])]


					#---- CHECK WEATHER TO CHOOSE flight "J" for not
					if int(t[i]) > int(flight[i][6])+int(t[j]):
						t[i] = int(t[i])
						#print "> DIDN'T add : " + str(flight[i][0])
						#temp = [key[i]]
					else:
						#print "To-Add : " + str(key[i])
						t[i] = int(flight[i][6])+int(t[j])
						temp = [key[j],key[i]]
						#print "After Add : " + str(key[j]) + " " + str(key[i]) + "\n"

						if key[j] != '':
							zz = [key[j][0],key[j][1],key[i][1],t[i]]
						else :
							zz = [key[i][0],key[i][1],t[i]]
						path.append(zz)
					#print "total : " + str(t[i])

		queue.append(temp)
		#print "QUEUE : " + str(queue)

		#print ">>>>>>>>>>>>>  queue : " + str(queue) + " with weight : " + str(t[i])
		#print "------------------ \n"

	maxVal = 0
	keyMax = 0
	for i in range(len(t)):
		if int(t[i]) > maxVal:
			maxVal = int(t[i])
			keyMax = i
	#print ">>>>>>> " + str(maxVal) + " with path" + str(queue[keyMax-1]) + "\n"
	#print "------------------ \n"

	max_path = []
	maxProf = 0
	for i in range(len(path)):
		#print path[i]
		x = len(path[i])
		if path[i][x-1] > maxProf:
			maxProf = path[i][x-1]
			max_path = path[i]
	#print "MAX >>>> " , max_path
	#print "\n"
	#count = len(max_path)-3
	next_path = max_path
	while (len(next_path) > 3 ):
		for i in range(len(path)):
			x = len(path[i])
			#print path[i][x-2]
			#print "x"
			if path[i][x-2] == max_path[1]:
				print "max path : " +str(max_path)
				#print "NEXT path : "  +str(path[i]) + "\n"
				print ">>>>> ADD : " + str(path[i][1])
				max_path.insert(1, path[i][1])
				#count -= 1
				#print "max path : " +str(max_path)
				for j in range(len(path)):
					if path[j][len(path[j])-2] == max_path[1]:
						print "NEXT Path : " +str(path[j]) + "\n"
						next_path = path[j]

	#print " >>>> " , max_path, len(max_path)
	if len(max_path) != 0:
		max_path.pop(0)
		max_path.insert(0,next_path[0])
	#print " >>>> " , max_path
	#print "Maxy Maxx : " , max_path[count]
	return max_path


#-----------------------  MAIN ------------------

def main():

	file = open("dyTest.csv", "rb")
	flight = readToArray(file)

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

	temp = flight[0]
	#print "temp :  " + str(temp)
	flight.pop(0)
	flight.sort(key=lambda tup: tup[5])

	""" ********************
	flight.insert(0,temp)
	"""

	"""
	for i in range(len(flight)):
		print flight[i]
	"""

	s_h = 1
	s_w = len(AircraftType)
	#print "AircraftType : " + str(s_w) + "\n"
	seperated_flight = [["" for x in range(s_h)] for y in range(s_w)]

	for i in range(len(flight)):
		for j in range(len(AircraftType)):
			if flight[i][1] == AircraftType[j]:
				#print flight[i]
				#print seperated_flight[j]
				seperated_flight[j].append(flight[i])
				#print seperated_flight[j]
		#print "\n"

	for i in range(len(seperated_flight)):
		seperated_flight[i].pop(0)
		#for j in range(len(seperated_flight[i])):
			#print str(seperated_flight[i][j])
		#print "\n"

	total_rev = 0
	schedule_num = 1
	#assigned = False
	assigned = [False]*len(AircraftType)
	#print assigned



	#print "check 0"
	m_Path =  Dynamic_Flight(seperated_flight[0])
	#print m_Path
	#print len(m_Path)-1
	rev = m_Path.pop(len(m_Path)-1)
	#print rev
	for i in range(len(seperated_flight[0])):
		for j in range(len(m_Path)):
			if  seperated_flight[0][i][0] == m_Path[j]:
				seperated_flight[0][i].append(schedule_num)
				break

	checker = all(len(s_flight) == 8 for s_flight in seperated_flight[0])
	#print "checker 0 : " + str(checker) + "\n"
	if checker == True:
		assigned[0] = True
	schedule_num += 1

	#print assigned


	for i in range(len(seperated_flight[0])):
		print seperated_flight[0][i]


#------------



	print "\n"

	#for i in range(len(seperated_flight[0])):
		#print seperated_flight[0][i]
		#if seperated_flight[0][i][]

	toDefaultTimeFormat(flight)



	"""
	for i in range (len(flight)):
		if i > 0:
			print flight[i]
	"""

if __name__ == '__main__':
	main()
