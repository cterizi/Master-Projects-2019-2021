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
import math


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Funtions for train PNN using leave-one-out process
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
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
def simulated_annealing(trainData, trainDataGroups, testData_, testGroup_, trainTest_id, experiment_id):
	number_of_features = 9
	number_of_classes = 2
	std = 1
	kmax = 100 # 10 per step
	beta = [1, 5, 10]
	alpha = [1, 2]

	# Generate 100 random values for p vector (random direction). Write data in file.
	# file = open('seeds/simulated_annealing/kfold_' + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt", '+w')
	# initial_x_step = np.random.uniform(0, std)
	# file.write("initial_step:" + str(initial_x_step) + "\n")
	# initial_temperature = np.random.uniform(0, 100)
	# file.write("initial_temperature:" + str(initial_temperature) + "\n")
	# for i in range(0, kmax + 1):
	# 	p = np.random.uniform(0, 1)
	# 	file.write("p_" + str(i) + ":" + str(p) + "\n")
	# 	s = np.random.uniform(-1, 1)
	# 	file.write("s_" + str(i) + ":" + str(s) + "\n")
	# 	rand = np.random.uniform(0, 1)
	# 	file.write("rand_" + str(i) + ":" + str(rand) + "\n")
	# 	file.flush()
	# file.close()


	# Load from file the initial values
	file = open('seeds/simulated_annealing/kfold_' + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt", 'r')
	p_directions = []
	s_directions = []
	rand_directions = []
	for line in file:
		line = line.replace("\n", "").split(":")
		if("initial_step" == line[0]):
			initial_x = float(line[1])
		elif("initial_temperature" == line[0]):
			initial_temperature = float((line[1]))
		elif("p_" in line[0]):
			p_directions.append(float(line[1]))
		elif("s_" in line[0]):
			if(float(line[1]) > 0):
				s_directions.append(1)
			else:
				s_directions.append(-1)
		elif("rand_" in line[0]):
			rand_directions.append(float(line[1]))
	file.close()


	# Generate a list of values for k_max factor. Initial k_max = 1000
	k_max = [10]
	while(True):
		k_max.append(k_max[-1] + k_max[0])
		if(k_max[-1] == kmax):
			break

	bestSigmaAndAccuracyForDifferentKMax = {}
	accuracyOnTest = {}
	uppoints = {}

	for beta_values in beta:
		bestSigmaAndAccuracyForDifferentKMax[beta_values] = {}
		accuracyOnTest[beta_values] = {}
		uppoints[beta_values] = {}
		for alpha_values in alpha:
			bestSigmaAndAccuracyForDifferentKMax[beta_values][alpha_values] = {}
			accuracyOnTest[beta_values][alpha_values] = {}
			uppoints[beta_values][alpha_values] = {}
			print("beta_values", beta_values, "alpha_values", alpha_values)

			k = 0
			# initial_x = np.random.uniform(0, std)
			x_best = initial_x
			z = [initial_x]
			t = [initial_temperature]
			accuraciesPerSigma = {initial_x: train(trainData, trainDataGroups, initial_x)}
			up_points = 0
			bestSigmaPerIteration = []

			while(k < kmax):
				print("Iteration", k)

				# Sample point
				y_k_1 = initial_x + p_directions[k] * s_directions[k]

				# Calculate Facc funtion
				accuracy_x = accuraciesPerSigma[initial_x]
				accuracy_y = train(trainData, trainDataGroups, y_k_1)
				accuraciesPerSigma[y_k_1] = accuracy_y
				if(accuracy_y > accuracy_x):
					facc = 1
				else:
					facc = math.exp((-1)*(((1 - accuracy_y) - (1 - accuracy_x))/t[k]))
				if(rand_directions[k] <= facc):
					up_points += 1
					initial_x = y_k_1

					# Update set Z
					z.append(y_k_1)

				# Update temperature value - Cooling schedule
				f_star = 0.01
				t_k_1 = beta_values * (1 - accuraciesPerSigma[initial_x] - f_star)**alpha_values
				t.append(t_k_1)

				# Update best sigma
				if(accuraciesPerSigma[initial_x] > accuraciesPerSigma[x_best]):
					x_best = initial_x

				bestSigmaPerIteration.append([x_best, accuraciesPerSigma[x_best]])
				k += 1

				uppoints[beta_values][alpha_values][k] = up_points
			

			# Find sigma with best accuracy score
			# bestSigmaAndAccuracyForDifferentKMax = {}
			for kmax_values in k_max:
				bestSigma = -1
				bestAccuracy = -1
				for element in bestSigmaPerIteration[0:kmax_values]:
					if(element[1] > bestAccuracy):
						bestAccuracy = element[1]
						bestSigma = element[0]
				bestSigmaAndAccuracyForDifferentKMax[beta_values][alpha_values][kmax_values] = [bestSigma, bestAccuracy]

			
			# Split X_train into two sublists for PNN on test set
			X_train_class_1 = []
			X_train_class_2 = []
			for i in range(0, len(trainDataGroups)):
				if(trainDataGroups[i] == 1):
					X_train_class_1.append(trainData[i])
				else:
					X_train_class_2.append(trainData[i])

			# Test best sigma on test set
			# accuracyOnTest = {}
			for kmax_values in k_max:
				predictedGroups_testSet = PNN_(bestSigmaAndAccuracyForDifferentKMax[beta_values][alpha_values][kmax_values][0], X_train_class_1, X_train_class_2, testData_, number_of_features, number_of_classes)
				accuracy_testSet = accuracy_score(testGroup_, np.asarray(predictedGroups_testSet))
				accuracyOnTest[beta_values][alpha_values][kmax_values] = [bestSigmaAndAccuracyForDifferentKMax[beta_values][alpha_values][kmax_values][0], accuracy_testSet]

	# print(bestSigmaAndAccuracyForDifferentKMax)
	# print(accuracyOnTest)
	# print(uppoints)
	# Write results in files
	# print("Up points", 100 * up_points/kmax)

	path = "results/simulated_annealing//kfold_" + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt"
	file = open(path, '+w')
	file.write("K_max\tbeta\talpha\tBest Sigma\tAccuracy\n")
	for it in bestSigmaAndAccuracyForDifferentKMax[1][1]:
		for bb in beta:
			for aa in alpha:
				file.write(str(it) + "\t" + 
					str(bb) + "\t" + str(aa) + "\t" + str((((bestSigmaAndAccuracyForDifferentKMax[bb])[aa]))[it][0]) + "\t" + str((((bestSigmaAndAccuracyForDifferentKMax[bb])[aa]))[it][1]) + "\n")
				file.flush()
	file.write("---------\n")

	for it in bestSigmaAndAccuracyForDifferentKMax[1][1]:
		for bb in beta:
			for aa in alpha:
				file.write(str(it) + "\t" + str(bb) + "\t" + str(aa) + "\t" + str((((accuracyOnTest[bb])[aa]))[it][0]) + "\t" + str((((accuracyOnTest[bb])[aa]))[it][1]) + "\n")
				file.flush()
	file.close()