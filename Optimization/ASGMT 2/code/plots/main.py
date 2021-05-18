'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Import libraries
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
import matplotlib.pyplot as plt
import numpy as np
import statistics
import sys
import scipy.stats
import scipy.stats as st
from itertools import combinations
from scipy.stats import ttest_ind
from scipy.stats import f_oneway
import itertools
# from scipy.stats import ttest_ind
# from scipy import stats
# from scipy.stats import wilcoxon


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Read results from files
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
def readResultsRandomSearch():
	kfolds = [i for i in range(1, 11)]
	experiments = [i for i in range(1, 11)]
	k_max = [10]
	while(True):
		k_max.append(k_max[-1] + k_max[0])
		if(k_max[-1] == 100):
			break
	results = {}

	for kfold_value in kfolds:
		# results[kfold_value] = {}
		for experiment in experiments:
			# print("kfold_value", kfold_value, "experiment", experiment)
			path = "../results/" + sys.argv[1] + "/kfold_" + str(kfold_value) + "/exp_" + str(experiment) + ".txt"
			file = open(path, 'r')
			skipTrainResults = False
			for line in file:
				if("---" in line):
					skipTrainResults = True
				if(skipTrainResults and not("---" in line)):
					line = line.replace("\n", "").split("\t")
					k_max_value = int(line[0])
					accuracy = float(line[-1])
					if(k_max_value in results):
						# results[kfold_value][k_max_value] = np.append(results[kfold_value][k_max_value], [accuracy])
						results[k_max_value] = np.append(results[k_max_value], [accuracy])
					else:
						# results[kfold_value][k_max_value] = np.asarray([accuracy])
						results[k_max_value] = np.asarray([accuracy])
			file.close()
	return(results)


def readResultsSimulatedAnnealing():
	kfolds = [i for i in range(1, 11)]
	experiments = [i for i in range(1, 11)]
	k_max = [10]
	while(True):
		k_max.append(k_max[-1] + k_max[0])
		if(k_max[-1] == 100):
			break
	alpha = [1, 2]
	beta = [1, 5, 10]
	combinations = list(itertools.product(beta, alpha))

	results = {}
	for com in combinations:
		results[com] = {10:[], 20:[], 30:[], 40:[], 50:[], 60:[], 70:[], 80:[], 90:[], 100:[]}

	for kfold_value in kfolds:
		for experiment in experiments:
			path = "../results/" + sys.argv[1] + "/kfold_" + str(kfold_value) + "/exp_" + str(experiment) + ".txt"
			file = open(path, 'r')
			skipTrainResults = False
			for line in file:
				if("---" in line):
					skipTrainResults = True
				if(skipTrainResults and not("---" in line)):
					line = line.replace("\n", "").split("\t")
					results[(int(line[1]), int(line[2]))][int(line[0])].append(float(line[-1]))
			file.close()
	return(results)


def readResultsRandomSearchStep():
	kfolds = [i for i in range(1, 11)]
	experiments = [i for i in range(1, 11)]
	k_max = [10]
	while(True):
		k_max.append(k_max[-1] + k_max[0])
		if(k_max[-1] == 100):
			break
	alpha = [1.5, 2]
	beta = [0.7, 0.5]
	step = [0.1, 0.5]
	combinations = list(itertools.product(alpha, beta, step))
	
	results = {}
	for com in combinations:
		results[com] = {10:[], 20:[], 30:[], 40:[], 50:[], 60:[], 70:[], 80:[], 90:[], 100:[]}

	for kfold_value in kfolds:
		for experiment in experiments:
			path = "../results/" + sys.argv[1] + "/kfold_" + str(kfold_value) + "/exp_" + str(experiment) + ".txt"
			file = open(path, 'r')
			skipTrainResults = False
			for line in file:
				if("---" in line):
					skipTrainResults = True
				if(skipTrainResults and not("---" in line)):
					line = line.replace("\n", "").split("\t")
					results[(float(line[1]), float(line[2]), float(line[3]))][int(line[0])].append(float(line[-1]))
			file.close
	return(results)


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Functions for plots
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
def boxplot_1(data, savePath):
	d = []
	xaxis = []
	fig1, ax1 = plt.subplots()
	green_diamond = dict(markerfacecolor='g', marker='D')
	for i in data:
		d.append(data[i])
		xaxis.append(i)
	ax1.boxplot(d, flierprops = green_diamond, notch = True)
	plt.xlabel("Computational budget, k_max", fontsize=17)
	plt.ylabel("Accuracy", fontsize=17)
	plt.tick_params(axis='x', labelsize=18)
	plt.xticks(np.arange(1, 11), xaxis)
	plt.tick_params(axis='y', labelsize=18)
	if(sys.argv[1] == "random_search"):
		plt.ylim(bottom=0.90)
	elif(sys.argv[1] == "nelder_mead" or sys.argv[1] == "random_search_step"):
		plt.ylim(bottom=0.88)
	elif(sys.argv[1] == "simulated_annealing"):
		plt.ylim(bottom=0.60)
	plt.tight_layout()
	plt.grid()
	plt.savefig(savePath)
	plt.close()
	plt.show()


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Main code
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
if __name__ == '__main__':
	kmaxs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

	if(sys.argv[1] == "random_search" or sys.argv[1] == "nelder_mead"):
		results = readResultsRandomSearch()

		# Boxplot for each k_max thershold. Call boxplot_1 function
		# boxplot_1(results, sys.argv[1] + ".png")

		# Calculate table min, max, mean, variance, std
		#file = open("../statistics/" + sys.argv[1] + ".txt", "+w")
		#file.write("K_max\tMean\tMedian\tSt.Dev.\tMin.\tMax.\tCI low\tCI up\n")
		#for i in kmaxs:
		#	ci = st.t.interval(0.95, len(results[i])-1, loc=np.mean(results[i]), scale=st.sem(results[i]))
		#	file.write(f'{i}\t{statistics.mean(results[i])}\t{statistics.median(results[i])}\t{statistics.stdev(results[i])}\t{min(results[i])}\t{max(results[i])}\t{ci[0]}\t{ci[1]}\n')
		#file.close()

		# p_value
		file = open("../p_values/095/" + sys.argv[1] + ".txt", "+w")
		for list1, list2 in combinations(results.keys(), 2):
			t, p = ttest_ind(results[list1], results[list2])
			if(p > 0.95):
				file.write(f'{list1}\t{list2}\t{p}\n')
			# file.write(f'{list1}\t{list2}\t{p}\n')
		file.close()

	elif(sys.argv[1] == 'random_search_step'):
		results = readResultsRandomSearchStep()

		for com in results:
			# Boxplot for each k_max thershold. Call boxplot_1 function
			# boxplot_1(results[com], "random_search_step/" + str(com) + ".png")

			# Calculate table min, max, mean, variance, std
			# file = open("../statistics/random_search_step/" + str(com) + ".txt", "+w")
			# file.write("K_max\tMean\tMedian\tSt.Dev.\tMin.\tMax.\tCI low\tCI up\n")
			# for i in kmaxs:
			# 	ci = st.t.interval(0.95, len(results[com][i])-1, loc=np.mean(results[com][i]), scale=st.sem(results[com][i]))
			# 	file.write(f'{i}\t{statistics.mean(results[com][i])}\t{statistics.median(results[com][i])}\t{statistics.stdev(results[com][i])}\t{min(results[com][i])}\t{max(results[com][i])}\t{ci[0]}\t{ci[1]}\n')
			# file.close()

			# p_value
			file = open("../p_values/095/random_search_step/" + str(com) + ".txt", "+w")
			for list1, list2 in combinations(results[com].keys(), 2):
				t, p = ttest_ind(results[com][list1], results[com][list2])
				if(p > 0.95):
					file.write(f'{list1}\t{list2}\t{p}\n')
				# file.write(f'{list1}\t{list2}\t{p}\n')
			file.close()

	elif(sys.argv[1] == "simulated_annealing"):
		results = readResultsSimulatedAnnealing()

		for com in results:
			# Boxplot for each k_max thershold. Call boxplot_1 function
			# boxplot_1(results[com], "simulated_annealing/" + str(com) + ".png")

			# Calculate table min, max, mean, variance, std
			# file = open("../statistics/simulated_annealing/" + str(com) + ".txt", "+w")
			# file.write("K_max\tMean\tMedian\tSt.Dev.\tMin.\tMax.\tCI low\tCI up\n")
			# for i in kmaxs:
			# 	ci = st.t.interval(0.95, len(results[com][i])-1, loc=np.mean(results[com][i]), scale=st.sem(results[com][i]))
			# 	file.write(f'{i}\t{statistics.mean(results[com][i])}\t{statistics.median(results[com][i])}\t{statistics.stdev(results[com][i])}\t{min(results[com][i])}\t{max(results[com][i])}\t{ci[0]}\t{ci[1]}\n')
			# file.close()

			# p_value
			file = open("../p_values/095/simulated_annealing/" + str(com) + ".txt", "+w")
			for list1, list2 in combinations(results[com].keys(), 2):
				t, p = ttest_ind(results[com][list1], results[com][list2])
				if(p > 0.95):
					file.write(f'{list1}\t{list2}\t{p}\n')
				# file.write(f'{list1}\t{list2}\t{p}\n')
			file.close()
