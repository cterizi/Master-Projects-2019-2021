'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Import libraries
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
from sklearn.metrics import accuracy_score
from PNN import PNN_
import numpy as np
import time


def returnGroups(d, g):
	class1 = []
	class2 = []
	for i in range(0, len(g)):
		if(g[i] == 1):
			class1.append(d[i])
		else:
			class2.append(d[i])
	return(class1, class2)


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Main function
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
def random_search(trainData, trainDataGroups, testData_, testGroup_, trainTest_id, experiment_id):
	number_of_features = 9
	number_of_classes = 2
	std = 1
	kmax = 100 # 10 per step

	# Generate 100 random values for p vector (random direction). Write data in file.
	# file = open('seeds/random_search/kfold_' + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt", '+w')
	# for i in range(0, kmax):
	# 	tmp_sigma = np.random.normal(0, std)
	# 	file.write("sigma_" + str(i) + ":" + str(tmp_sigma) + "\n")
	# 	file.flush()
	# file.close()

	# Load from file the initial x step and p random directions
	file = open('seeds/random_search/kfold_' + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt", 'r')
	tmp_sigma_list = []
	for line in file:
		line = line.replace("\n", "").split(":")
		if("sigma_" in line[0]):
			tmp_sigma_list.append(float(line[1]))
	file.close()

	# Generate a list of values for k_max factor. Initial k_max = 1000
	k_max = [10]
	while(True):
		k_max.append(k_max[-1] + k_max[0])
		if(k_max[-1] == kmax):
			break

	mapSigmaAccuracy = []
	for iter_ in range(0, kmax):
		print("Iteration", iter_)
		# Select sigma from a Gaussian distribution with mean = 0 and standard deviation = 1
		tmp_sigma = tmp_sigma_list[iter_]
		trainPredictedResults = []

		for train_id in range(0, len(trainData)):
			testVector = [trainData[train_id]]
			testGroup = trainDataGroups[train_id]

			if(train_id == 0):
				trainArray = trainData[1:]
				groupArray = trainDataGroups[1:]
			elif(train_id == len(trainData) - 1):
				trainArray = trainData[0:-1]
				groupArray = trainDataGroups[0:-1]
			else:
				trainArray_first = list(trainData[0:train_id])
				trainArray_second = list(trainData[train_id+1:len(trainData)])
				trainArray = trainArray_first + trainArray_second
				groupArray_first = list(trainDataGroups[0:train_id])
				groupArray_second = list(trainDataGroups[train_id+1:len(trainData)])
				groupArray = groupArray_first + groupArray_second
			
			[trainData_class_1, trainData_class_2] =  returnGroups(trainArray, groupArray)
			
			predictedGroup = PNN_(tmp_sigma, trainData_class_1, trainData_class_2, testVector, number_of_features, number_of_classes)
			trainPredictedResults.append(predictedGroup)
			
		mapSigmaAccuracy.append([tmp_sigma, accuracy_score(trainDataGroups, trainPredictedResults)])


	# Find sigma with best accuracy score
	bestSigmaAndAccuracyForDifferentKMax = {}
	for kmax_values in k_max:
		bestSigma = -1
		bestAccuracy = -1
		for element in mapSigmaAccuracy[0:kmax_values]:
			if(element[1] > bestAccuracy):
				bestAccuracy = element[1]
				bestSigma = element[0]
		bestSigmaAndAccuracyForDifferentKMax[kmax_values] = [bestSigma, bestAccuracy]


	# Split X_train into two sublists for PNN on test set
	X_train_class_1 = []
	X_train_class_2 = []
	for i in range(0, len(trainDataGroups)):
		if(trainDataGroups[i] == 1):
			X_train_class_1.append(trainData[i])
		else:
			X_train_class_2.append(trainData[i])

	# Test best sigma on test set
	accuracyOnTest = {}
	for kmax_values in bestSigmaAndAccuracyForDifferentKMax:
		predictedGroups_testSet = PNN_(bestSigmaAndAccuracyForDifferentKMax[kmax_values][0], X_train_class_1, X_train_class_2, testData_, number_of_features, number_of_classes)
		accuracy_testSet = accuracy_score(testGroup_, np.asarray(predictedGroups_testSet))
		accuracyOnTest[kmax_values] = [bestSigmaAndAccuracyForDifferentKMax[kmax_values][0], accuracy_testSet]
	
	return(bestSigmaAndAccuracyForDifferentKMax, accuracyOnTest)