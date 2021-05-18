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
def random_search_step(trainData, trainDataGroups, testData_, testGroup_, trainTest_id, experiment_id):
	number_of_features = 9
	number_of_classes = 2
	std = 1
	kmax = 100 # 10 per step

	a = [1.5, 2] 	# increase 
	b = [0.7, 0.5]	# shrink
	step = [0.1, 0.5]	# initial step

	# Generate 100 random values for p vector (random direction). Write data in file.
	# file = open('seeds/random_search_step/kfold_' + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt", '+w')
	# initial_x_step = np.random.uniform(0, std)
	# file.write("initial_step:" + str(initial_x_step) + "\n")
	# for i in range(0, kmax + 1):
	# 	p = np.random.uniform(-1, 1)
	# 	file.write("p_" + str(i) + ":" + str(p) + "\n")
	# 	file.flush()
	# file.close()

	# Load from file the initial x step and p random directions
	file = open('seeds/random_search_step/kfold_' + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt", 'r')
	p_directions = []
	for line in file:
		line = line.replace("\n", "").split(":")
		if("initial_step" == line[0]):
			initial_x = float(line[1])
		elif("p_" in line[0]):
			p_directions.append(float(line[1]))
	file.close()

	# Generate a list of values for k_max factor. Initial k_max = 100
	k_max = [10]
	while(True):
		k_max.append(k_max[-1] + k_max[0])
		if(k_max[-1] == kmax):
			break

	bestSigmaAndAccuracyForDifferentKMax = {}
	accuracyOnTest = {}

	for a_value in a:
		bestSigmaAndAccuracyForDifferentKMax[a_value] = {}
		accuracyOnTest[a_value] = {}
		for b_value in b:
			bestSigmaAndAccuracyForDifferentKMax[a_value][b_value] = {}
			accuracyOnTest[a_value][b_value] = {}
			for step_value in step:
				bestSigmaAndAccuracyForDifferentKMax[a_value][b_value][step_value] = {}
				accuracyOnTest[a_value][b_value][step_value] = {}

				step_value_ = step_value
				print("a_value", a_value, "b_value", b_value, "step_value", step_value)
				mapSigmaAccuracy = []

				# Main loop
				k = 0
				x_best = initial_x
				while(k < kmax):
					print("Iteration", k)
					p = p_directions[k]
					# p = p / abs(p) 							# ||p|| = p if p is 1-d, so p/||p|| = 1
					x_t = initial_x + step_value * p
					k += 1

					f_x_t = train(trainData, trainDataGroups, x_t)
					f_x_x = train(trainData, trainDataGroups, initial_x)
					
					if(k == 1):
						mapSigmaAccuracy.append([initial_x, f_x_x])
					mapSigmaAccuracy.append([x_t, f_x_t])
					
					'''
						If accuracy with the new sigma (x_t) value is higher than the previous (initial_x),
						then increase step.
					'''
					if(f_x_t > f_x_x):
						# mapSigmaAccuracy.append([x_t, f_x_t])

						s_1 = a_value * step_value
						x_1 = initial_x + s_1 * p
						k += 1

						f_x_1 = train(trainData, trainDataGroups, x_1)
						mapSigmaAccuracy.append([x_1, f_x_1])

						if(f_x_1 > f_x_t):
							initial_x = x_1
							step_value = s_1
						else:
							initial_x = x_t
					else:
						'''
						If accuracy with the new sigma (x_t) value is lower than the previous (initial_x),
						then shrink step.
						'''
						s_m = b_value * step_value
						x_m = initial_x + s_m * p
						k += 1

						f_x_m = train(trainData, trainDataGroups, x_m)

						mapSigmaAccuracy.append([x_m, f_x_m])
						if(f_x_m > f_x_x):
							initial_x = x_m
							step_value = s_m

					f_x_best = train(trainData, trainDataGroups, x_best)
					f_x_new = train(trainData, trainDataGroups, initial_x)

					if(f_x_new > f_x_best):
						x_best = initial_x

				
				# Find sigma with best accuracy score
				for kmax_values in k_max:
					bestSigma = -1
					bestAccuracy = -1
					for element in mapSigmaAccuracy[0:kmax_values]:
						if(element[1] >= bestAccuracy):
							bestAccuracy = element[1]
							bestSigma = element[0]
					bestSigmaAndAccuracyForDifferentKMax[a_value][b_value][step_value_][kmax_values] = [bestSigma, bestAccuracy]

				# Split X_train into two sublists for PNN on test set
				X_train_class_1 = []
				X_train_class_2 = []
				for i in range(0, len(trainDataGroups)):
					if(trainDataGroups[i] == 1):
						X_train_class_1.append(trainData[i])
					else:
						X_train_class_2.append(trainData[i])

				# Test best sigma on test set
				for kmax_values in k_max:
					predictedGroups_testSet = PNN_(bestSigmaAndAccuracyForDifferentKMax[a_value][b_value][step_value_][kmax_values][0], X_train_class_1, X_train_class_2, testData_, number_of_features, number_of_classes)
					accuracy_testSet = accuracy_score(testGroup_, np.asarray(predictedGroups_testSet))
					accuracyOnTest[a_value][b_value][step_value_][kmax_values] = [bestSigmaAndAccuracyForDifferentKMax[a_value][b_value][step_value_][kmax_values][0], accuracy_testSet]
					
	# print(accuracyOnTest)
	# print(bestSigmaAndAccuracyForDifferentKMax)
	# Write results
	path = "results/random_search_step/kfold_" + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt"
	file = open(path, '+w')
	file.write("K_max\ta\tb\tStep_size\tBest Sigma\tAccuracy\n")
	for it in bestSigmaAndAccuracyForDifferentKMax[1.5][0.7][0.1]:
		for aa in a:
			for bb in b:
				for ss in step:
					file.write(str(it) + "\t" + 
						str(aa) + "\t" + str(bb) + "\t" + str(ss) + "\t" + str((((bestSigmaAndAccuracyForDifferentKMax[aa])[bb])[ss])[it][0]) + "\t" + str((((bestSigmaAndAccuracyForDifferentKMax[aa])[bb])[ss])[it][1]) + "\n")
					file.flush()
	file.write("---------\n")

	for it in bestSigmaAndAccuracyForDifferentKMax[1.5][0.7][0.1]:
		for aa in a:
			for bb in b:
				for ss in step:
					file.write(str(it) + "\t" + str(aa) + "\t" + str(bb) + "\t" + str(ss) + "\t" + str((((accuracyOnTest[aa])[bb])[ss])[it][0]) + "\t" + str((((accuracyOnTest[aa])[bb])[ss])[it][1]) + "\n")
					file.flush()
	file.close()