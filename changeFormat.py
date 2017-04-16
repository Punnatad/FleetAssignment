import csv
import string

flight = []


def readToArray(file):
	lines = []
	for line in file.xreadlines():
		lines.append(string.split(line, ','))
	return lines

# --------------------- Main ---------------------------------------

def main():

# --------------------- Read & Write CSV ---------------------------------------

	# Read csv file to list
	file = open("Planner_AirAsia_b4.csv", "rb")
	flight = readToArray(file)

	#------ Change Time Format (06:00 to 0600)
	for i in range(len(flight)):
		if i > 0:
			temp = str(flight[i][4])
			temp_temp = str(temp[0])+str(temp[1])+str(temp[3])+str(temp[4])
			flight[i][4] = temp_temp

			temp = str(flight[i][5])
			temp_temp = str(temp[0])+str(temp[1])+str(temp[3])+str(temp[4])
			flight[i][5] = temp_temp

	for i in range(len(flight)):
		flight[i][6] = flight[i][6].replace("\r\n","")


	# Write list to csv file
	out = open("Planner_AirAsia.csv", "wb")
	writer = csv.writer(out)
	for i in range(len(flight)):
		writer.writerow(flight[i])

	for i in range(len(flight)):
		print flight[i]

	#file = open("out.csv", "rb")
	#reout = readToArray(file)



# ---------------------------  ----------------------------------------
	print("\n ----- Done ----- \n")

if __name__ == '__main__':
	main()
