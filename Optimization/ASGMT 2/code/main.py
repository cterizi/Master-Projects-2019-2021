'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Import libraries
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
from simulated_annealing import simulated_annealing
from random_search_step import random_search_step
from random_search import random_search
from nelder_mead import nelder_mead
from loadData import loadData
from PNN import PNN_

from sklearn.model_selection import KFold
from sklearn.metrics import * 
from os import path
import numpy as np
import os.path
import sys


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Functions
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
def printMinMaxvalueForFeatures(data):
	for featureIndex in range(0, len(data[0])):
		featureValues = data[:, featureIndex]
		print(f'Feature {featureIndex}: min: {np.amin(featureValues)}, max:{np.amax(featureValues)}, mean: {np.mean(featureValues)}, variance: {np.var(featureValues)}, std: {np.std(featureValues)}')


def writeRandomSearch(results_train, results_test, trainTest_id, experiment_id):
	path = "results/" + sys.argv[1]  + "/kfold_" + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt"
	file = open(path, '+w')
	file.write("K_max\tBest Sigma\tAccuracy\n")
	for result in results_train:
		file.write(str(result) + "\t" + str(abs(results_train[result][0])) + "\t" + str(results_train[result][1]) + "\n")
		file.flush()
	file.write("---------\n")
	for result in results_test:
		file.write(str(result) + "\t" + str(abs(results_test[result][0])) + "\t" + str(results_test[result][1]) + "\n")
		file.flush()
	file.close()


# def writeRandomSearchStep(results, trainTest_id, experiment_id):
# 	path = "results/" + sys.argv[1]  + "/kfold_" + str(trainTest_id) + "/exp_" + str(experiment_id) + ".txt"
# 	file = open(path, '+w')
# 	file.write("K_max\ta\tb\tStep_size\tBest Sigma\tAccuracy\n")
# 	for it in results:
# 		for a_v in results[it]:
# 			for b_v in results[it][a_v]:
# 				for ss in results[it][a_v][b_v]:
# 					file.write(str(it) + "\t" + str(a_v) + "\t" + str(b_v) + "\t" + str(ss) + "\t" + str(results[it][a_v][b_v][ss][0]) + "\t" + str(results[it][a_v][b_v][ss][1]) + "\n")
# 					file.flush()
# 	file.close()

'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Main code
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
if __name__ == '__main__':
	# Load dataset
	[ids, features, groups] = loadData()
	
	# Print maximum and minimum values for each feature
	# printMinMaxvalueForFeatures(features)

	# Apply k-fold cross validation
	kfold_number = 10
	cv = KFold(n_splits = kfold_number, random_state = 1, shuffle = True)
	train_test = 1

	for train_index, test_index in cv.split(features):
		# Split train and test sets
		X_train, X_test = features[train_index], features[test_index]
		y_train, y_test = groups[train_index], groups[test_index]


		experimentIds = [i for i in range(1, 11)]
		for exid in experimentIds:
			if(sys.argv[1] == "random_search"):
				# print("kfold", train_test, "Experiment", int(sys.argv[2]))
				# [results_random_search_train, results_random_search_test] = random_search(X_train, y_train, X_test, y_test, trainTest_id = train_test, experiment_id = int(sys.argv[2]))
				# writeRandomSearch(results_random_search_train, results_random_search_test, train_test, int(sys.argv[2]))

				print("kfold", train_test, "Experiment", exid)
				[results_random_search_train, results_random_search_test] = random_search(X_train, y_train, X_test, y_test, trainTest_id = train_test, experiment_id = exid)
				writeRandomSearch(results_random_search_train, results_random_search_test, train_test, exid)

			elif(sys.argv[1] == "random_search_step"):
				# print("kfold", train_test, "experiment", int(sys.argv[2]))
				# random_search_step(X_train, y_train, X_test, y_test, trainTest_id = train_test, experiment_id = int(sys.argv[2]))

				print("kfold", train_test, "Experiment", exid)
				random_search_step(X_train, y_train, X_test, y_test, trainTest_id = train_test, experiment_id = exid)

			elif(sys.argv[1] == "nelder_mead"):
				# print("kfold", train_test, "experiment", int(sys.argv[2]))
				# nelder_mead(X_train, y_train, X_test, y_test, trainTest_id = train_test, experiment_id = int(sys.argv[2]))

				print("kfold", train_test, "Experiment", exid)
				nelder_mead(X_train, y_train, X_test, y_test, trainTest_id = train_test, experiment_id = exid)

			elif(sys.argv[1] == "simulated_annealing"):
				# print("kfold", train_test, "experiment", int(sys.argv[2]))
				# simulated_annealing(X_train, y_train, X_test, y_test, trainTest_id = train_test, experiment_id = int(sys.argv[2]))

				print("kfold", train_test, "Experiment", exid)
				simulated_annealing(X_train, y_train, X_test, y_test, trainTest_id = train_test, experiment_id = exid)
		
		train_test += 1
		print("-----------------------")