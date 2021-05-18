'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Import libraries
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
from sklearn import preprocessing
import numpy as np
import random


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Function load data from file "breast-cancer-wisconsin"
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
def loadData():
	data = []
	file = open("breast-cancer-wisconsin.data", 'r')
	for line in file:
		try:
			line = [int(i) for i in line.replace("\n", "").split(",")]
		except:
			'''
				Six-th feature is missing for some records.
				Select a random feature from 1-10.
			'''
			line = line.replace("\n", "").split(",")
			line[6] = random.uniform(1, 11)
			line = [int(i) for i in line]

		# Set group 2 -> 1 and group 4 -> 2
		if(line[-1] == 2):
			line[-1] = 1
		else:
			line[-1] = 2
		data.append(line)
	file.close()
	data = np.asarray(data)
	ids = data[:, 0]
	groups = data[:, -1]

	# Normalize values for features
	features = data[:, 1:-1] 
	features_scaled = preprocessing.scale(features)

	return(ids, features_scaled, groups)
	# return(ids, features, groups)