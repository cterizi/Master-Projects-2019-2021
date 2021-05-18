import numpy as np

def load(path, path1):
	day = []
	data = []
	day_divided = []
	data_divided = []

	# Load days and cases #
	file = open(path, 'r')
	for line in file:
		line = line.replace("\n", "").strip().split("  ")
		
		day.append(int(line[0]))
		data.append(int(line[1]))

		# Change scale of data
		day_divided.append(int(line[0]) / 10)
		data_divided.append(int(line[1]) / 10000)
	file.close()

	day = np.asarray(day)
	data = np.asarray(data)
	day_divided = np.asarray(day_divided)
	data_divided = np.asarray(data_divided)

	# Load initial points #
	points = []
	file = open(path1, 'r')
	for line in file:
		line = [float(i) for i in (line.replace("\n", '').replace('\'', "").replace(']', "").split("= ["))[1].strip().split(" ")]
		points.append(line)
	file.close()

	return(day, data, day_divided, data_divided, points)
