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


def train(trainData, trainDataGroups, sigma):
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
		
		[trainData_class_1, trainData_class_2] = returnGroups(trainArray, groupArray)
		
		predictedGroup = PNN_(sigma, trainData_class_1, trainData_class_2, testVector, 9, 2)
		trainPredictedResults.append(predictedGroup)
	return(accuracy_score(trainDataGroups, trainPredictedResults))


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Main function
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
def nelder_mead(trainData, trainDataGroups, testData_, testGroup_, trainTest_id, experiment_id):
	number_of_features = 9
	number_of_classes = 2
	std = 1
	a = 1
	gamma = 2
	p = 0.5
	p_in = -0.5
	# kmax = 500 # 100 per step
	kmax = 100 # 100 per step

	totalReflectionPoints = 0
	totalExpansionPoints = 0
	totalOuterContractionPoints = 0
	totalInContractionPoints = 0
	totalShrinkPoints = 0
	totalPointsAccuracy = []

	bestFirst = []

	# Generate 100 random values for p vector (random direction). Write data in file.
	# file = open('seeds/nelder_mead/kfold_' + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt", '+w')
	# file.write(str(np.random.uniform(0, std)) + "\n")
	# file.write(str(np.random.uniform(0, std)) + "\n")
	# file.write(str(np.random.uniform(0, std)) + "\n")
	# file.close()

	# Load from file the initial x step and p random directions
	file = open('seeds/nelder_mead/kfold_' + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt", 'r')
	tmp_sigma_list = []
	for line in file:
		tmp_sigma_list.append(float(line.replace("\n", "")))
	file.close()

	# Load three initial points
	initial_1 = tmp_sigma_list[0]
	initial_2 = tmp_sigma_list[1]
	initial_3 = tmp_sigma_list[2]

	# Generate a list of values for k_max factor. Initial k_max = 1000
	k_max = [10]
	while(True):
		k_max.append(k_max[-1] + k_max[0])
		if(k_max[-1] == kmax):
			break

	# Calculate for these sigmas the accuracy on train test
	f_1 = train(trainData, trainDataGroups, initial_1)
	f_2 = train(trainData, trainDataGroups, initial_2)
	f_3 = train(trainData, trainDataGroups, initial_3)

	totalPointsAccuracy.append([initial_1, f_1])
	totalPointsAccuracy.append([initial_2, f_2])
	totalPointsAccuracy.append([initial_3, f_3])

	k = 0
	while(k < kmax):
		print("Iteration", k, totalPointsAccuracy)
		totalPointsAccuracy.sort(key=lambda x: x[1], reverse=True)
		# best = totalPointsAccuracy[0][1]
		bestFirst.append([totalPointsAccuracy[0][0], totalPointsAccuracy[0][1]])

		x_bar = (totalPointsAccuracy[0][0] + totalPointsAccuracy[1][0])/2

		# Reflection
		# print("Reflection")
		# reflected_point = x_bar - a*(x_bar - totalPointsAccuracy[-1][0])
		reflected_point = (1 + a) * x_bar - a * totalPointsAccuracy[-1][0]
		reflected_accuracy = train(trainData, trainDataGroups, reflected_point)
		if(reflected_accuracy > totalPointsAccuracy[-2][1] and not(reflected_accuracy > totalPointsAccuracy[0][1])):
			totalPointsAccuracy[-1][0] = reflected_point
			totalPointsAccuracy[-1][1] = reflected_accuracy
			k += 1
			totalReflectionPoints += 1
			continue
		print("Reflection", reflected_accuracy, "Best accuracy", totalPointsAccuracy[0][1])

		# Expansion
		# print("Expansion")
		if(reflected_accuracy > totalPointsAccuracy[0][1]):
			# expanded_point = x_bar + gamma * (reflected_point - x_bar)
			expanded_point = (1 + gamma) * x_bar - gamma * totalPointsAccuracy[-1][0]
			expanded_accuracy = train(trainData, trainDataGroups, expanded_point)
			if(expanded_accuracy > reflected_accuracy):
				totalPointsAccuracy[-1][0] = expanded_point
				totalPointsAccuracy[-1][1] = expanded_accuracy
				k += 1
				totalExpansionPoints += 1
				continue
			else:
				totalPointsAccuracy[-1][0] = reflected_point
				totalPointsAccuracy[-1][1] = reflected_accuracy
				k += 1
				totalReflectionPoints += 1
				continue
			print("Expansion", expanded_accuracy, "Best accuracy", totalPointsAccuracy[0][1])

		# Outer Contraction
		# print("Outer - Contraction")
		# contracted_point = x_bar + p * (totalPointsAccuracy[-1][0] - x_bar)
		contracted_point = (1 + p) * x_bar - p * totalPointsAccuracy[-1][0]
		contracted_accuracy = train(trainData, trainDataGroups, contracted_point)
		if(contracted_accuracy > totalPointsAccuracy[-1][1]):
			totalPointsAccuracy[-1][0] = contracted_point
			totalPointsAccuracy[-1][1] = contracted_accuracy
			k += 1
			totalOuterContractionPoints += 1
			continue
		print("Outer Contraction", contracted_accuracy, "Best accuracy", totalPointsAccuracy[0][1])

		# In Contraction
		# print("In Contraction")
		contracted_point_in = (1 + p_in) * x_bar - p_in * totalPointsAccuracy[-1][0]
		contracted_point_in_accuracy = train(trainData, trainDataGroups, contracted_point_in)
		if(contracted_point_in_accuracy > totalPointsAccuracy[-1][1]):
			totalPointsAccuracy[-1][0] = contracted_point_in
			totalPointsAccuracy[-1][1] = contracted_point_in_accuracy
			k += 1
			totalInContractionPoints += 1
			continue
		print("In Contraction", contracted_point_in_accuracy, "Best accuracy", totalPointsAccuracy[0][1])

		# Shrink
		# print("Shrink")
		for point in range(1, len(totalPointsAccuracy)):
			totalPointsAccuracy[point][0] = totalPointsAccuracy[0][0] - ((totalPointsAccuracy[point][0] - totalPointsAccuracy[0][0])/2)
		k +=1
		totalShrinkPoints += 1

	# Find sigma with best accuracy score
	bestSigmaAndAccuracyForDifferentKMax = {}
	for kmax_values in k_max:
		bestSigma = -1
		bestAccuracy = -1
		for element in bestFirst[0:kmax_values]:
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

	# Write results in files
	path = "results/nelder_mead//kfold_" + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt"
	file = open(path, '+w')
	file.write("Reflection: " + str(totalReflectionPoints) + "\n")
	file.write("Expansion: " + str(totalExpansionPoints) + "\n")
	file.write("OuterContraction: " + str(totalOuterContractionPoints) + "\n")
	file.write("InContraction: " + str(totalInContractionPoints) + "\n")
	file.write("Shrink: " + str(totalShrinkPoints) + "\n")
	file.write("K_max\tBest Sigma\tAccuracy\n")
	for result in bestSigmaAndAccuracyForDifferentKMax:
		file.write(str(result) + "\t" + str(abs(bestSigmaAndAccuracyForDifferentKMax[result][0])) + "\t" + str(bestSigmaAndAccuracyForDifferentKMax[result][1]) + "\n")
		file.flush()
	file.write("---------\n")
	for result in accuracyOnTest:
		file.write(str(result) + "\t" + str(abs(accuracyOnTest[result][0])) + "\t" + str(accuracyOnTest[result][1]) + "\n")
		file.flush()
	file.close()