import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from operator import add
import numpy as np
import math
import os

def MSEandStatistics(filePath):
	file = open(filePath, 'r')
	tmpList = []
	mseList = []
	highPredictedPairs = 0
	for line in file:
		tmpLine = line.replace("\n", "").split("\t")
		user_i = tmpLine[0]
		user_j = tmpLine[1]
		realJS = float(tmpLine[2])
		predictedJS = float(tmpLine[3])

		mseList.append((abs(predictedJS - realJS)))
		if(predictedJS > 0.85):
			highPredictedPairs = highPredictedPairs + 1
			tmpList.append((user_i, user_j))

	file.close()
	return({'mseList':mseList, 'totalNumberOfHighPredictedPairs':highPredictedPairs, 'pairsList':tmpList})

def loadGroundTruth(numberOfusers):
	path = "groundTruth/articles_" + str(numberOfusers) + ".truth.txt"
	file = open(path, 'r')
	listOfPairs = []
	for line in file:
		tmpLine = line.replace("\n", "").split(" ")
		tmpPair = (tmpLine[0], tmpLine[1])
		listOfPairs.append(tmpPair)

	file.close()
	return(listOfPairs)


'''
#########################
#########################
PLOTS
'mseList':mseList
'totalNumberOfHighPredictedPairs':highPredictedPairs
'pairsList':tmpList
#########################
#########################
'''
def cdf(y, x):
	data_ = y
	totalSize_ = len(data_)
	tmp_data_ = np.sort(np.asarray(list(set(data_))))
	sortedData_ = np.sort(np.asarray(data_))
	y_values_ = []
	print(len(x))
	tmpa = 0
	for i in x:
		tmpa = tmpa + 1
		if(tmpa == 10000 or tmpa == 50000 or tmpa == 80000 or tmpa == 110000):
			print(tmpa)
		y_values_.append(float((sortedData_<=i).sum()) / totalSize_)
	return(y_values_)

def cdfMSE(x, xlabel, ylabel, title, savePath):
	axisX = []
	p = {}

	for nohashes in x:
		axisX = axisX + x[nohashes]['mseList']
	axisX = np.sort(list(set(axisX)))
	for nohashes in x:
		p[nohashes] = cdf(x[nohashes]['mseList'], axisX)
		

	fig, ax1 = plt.subplots()
	
	colorMpatches = {2:"yellow", 10:"orange", 20:"red", 50:"brown", 100:"blue", 200:"black"}
	for nohashes in x:
		ax1.plot(axisX, p[nohashes], colorMpatches[nohashes])

	hashes_2 = mpatches.Patch(color='yellow', label='2 signatures')
	hashes_10 = mpatches.Patch(color='orange', label='10 signatures')
	hashes_20 = mpatches.Patch(color='red', label='20 signatures')
	hashes_50 = mpatches.Patch(color='brown', label='50 signatures')
	hashes_100 = mpatches.Patch(color='blue', label='100 signatures')
	hashes_200 = mpatches.Patch(color='black', label='200 signatures')

	leg = plt.legend(handles=[hashes_2, hashes_10, hashes_20, hashes_50, hashes_100, hashes_200], frameon = True, loc = 0, ncol = 1, fontsize = "large")

	ax1.tick_params(axis='y', labelcolor = "black", labelsize=14)
	ax1.tick_params(axis='x', labelcolor = "black", labelsize=14)
	ax1.set_ylabel(ylabel, fontsize=14)
	ax1.set_xlabel(xlabel, fontsize=14)
	plt.title(title, loc = 'center', fontsize = 15, color = 'orange')
	plt.ylim([-0.01, 1.01])
	plt.xlim([-0.01, 1.01])


	plt.grid()
	plt.tight_layout()

	plt.savefig(savePath)
	plt.show()

def plotCT(xaxis, TruePositivesList, FalseNegativesList, title):
	fig, ax1 = plt.subplots()

	# for i in range(0, len(xaxis)):
	# 	xaxis[i] = str(xaxis[i])
	# xaxis = np.array(xaxis)
	#xaxis = np.array(['2', '10', "20", "50", "100", "200"])
	#plt.xticks(range(len(xaxis)), xaxis)
	

	color = 'tab:green'
	ax1.scatter(xaxis, TruePositivesList, color = color)
	ax1.set_xlabel('number of signatures per user', fontsize=14)
	ax1.set_ylabel('True Positives Ratio', color=color, fontsize=14)
	plt.ylim([-0.05, 1.1])
	ax1.tick_params(axis='y', labelcolor = color, labelsize=14)

	#second axis 
	ax2 = ax1.twinx()
	color = 'tab:red'
	ax2.scatter(xaxis, FalseNegativesList, color = color)
	ax2.set_ylabel('False Negatives Ratio', color=color, fontsize=14)
	plt.ylim([-0.05, 1.1])
	ax2.tick_params(axis='y', labelcolor = color, labelsize=14)

	ax1.tick_params(axis='x', labelsize=14)

	#plt.title("", loc = 'center', fontsize = 15, color = 'orange')
	goalForTP = mpatches.Patch(color='green', label='Αpproaching one')
	goalForFN = mpatches.Patch(color='red', label='Αpproaching zero')
	leg = plt.legend(handles=[goalForTP, goalForFN], frameon = True, loc = 5, ncol = 1, fontsize = "x-large")


	plt.grid()
	plt.tight_layout()

	plt.savefig(title)
	plt.show()

def plotFP(xaxis, data, savePath):
	fig, ax1 = plt.subplots()
	# for i in range(0, len(xaxis)):
	# 	xaxis[i] = str(xaxis[i])
	# xaxis = np.array(xaxis)
	#xaxis = np.array(["2", "10", "20", "50", "100", "200"])
	#plt.xticks(range(len(xaxis)), xaxis) 

	color = 'tab:orange'
	ax1.scatter(xaxis, data, color = color)
	ax1.set_xlabel('number of signatures per user', fontsize=14)
	ax1.set_ylabel('False Positives', color=color, fontsize=14)
	plt.ylim([-5, 200])
	ax1.tick_params(axis='y', labelcolor = color, labelsize=14)
	ax1.tick_params(axis='x', labelsize=14)

	goalForFP = mpatches.Patch(color='orange', label='Αpproaching zero')
	leg = plt.legend(handles=[goalForFP], frameon = True, loc = 0, ncol = 1, fontsize = "x-large")

	plt.grid()
	plt.tight_layout()

	plt.savefig(savePath)
	plt.show()


def confusionTable(real, predicted, an):
	numberOfMinhashes = [2, 10, 20, 50, 100, 200]
	realNumber = len(real)

	TruePositivesList = []
	FalseNegativesList = []
	FalsePositivesList = []

	for i in numberOfMinhashes:

		print(str(i) + " signatures")

		TruePositives = 0
		FalseNegatives = 0
		FalsePositives = 0

		if(realNumber > len(predicted[i]['pairsList'])):
			FalseNegatives = realNumber - len(predicted[i]['pairsList'])
		if(realNumber < len(predicted[i]['pairsList'])):
			FalsePositives = len(predicted[i]['pairsList']) - realNumber

		for p in predicted[i]['pairsList']:
			if(p in real or (p[1], p[0]) in real):
				TruePositives = TruePositives + 1
		
		TruePositives = float(TruePositives) / realNumber
		TruePositivesList.append(TruePositives)

		FalseNegatives = float(FalseNegatives) / realNumber
		FalseNegativesList.append(FalseNegatives)
	
		FalsePositivesList.append(FalsePositives)

	print(TruePositivesList)
	print(FalseNegativesList)
	plotCT(numberOfMinhashes, TruePositivesList, FalseNegativesList, "plots/tpfn_error_" + str(an) + ".png")
	plotFP(numberOfMinhashes, FalsePositivesList, "plots/fp_error_" + str(an) + ".png")

def timePlot(readT, singT, xValues, savePath):
	fig, ax1 = plt.subplots()

	ax1.xaxis.set_ticks(xValues)
	ax1.xaxis.set_ticklabels(xValues)
	
	#read
	color = 'tab:red'
	ax1.plot(xValues, readT, color = color)
	ax1.set_xlabel('number of users/articles', fontsize=14)
	ax1.set_ylabel('time (seconds)', color=color, fontsize=14)
	ax1.tick_params(axis='y', labelcolor = color, labelsize=14)

	#signatures
	ax2 = ax1.twinx()
	color = 'tab:green'
	ax2.plot(xValues[:-1], singT, color = color)
	ax2.set_ylabel('time (seconds)', color=color, fontsize=14)
	ax2.tick_params(axis='y', labelcolor = color, labelsize=14)
	ax2.scatter(10000, singT[-1], color = color)
	ax1.tick_params(axis='x', labelsize=14, rotation = 45)

	readM = mpatches.Patch(color='red', label='terms to hash values')
	signaturesM = mpatches.Patch(color='green', label='generate signatures\n + calculate JS')
	largeNumberOfTIme = mpatches.Patch(color='green', label='infinity')
	leg = plt.legend(handles=[readM, signaturesM, largeNumberOfTIme], frameon = True, loc = 0, ncol = 1, fontsize = "x-large")

	plt.grid()
	plt.tight_layout()

	plt.savefig(savePath)
	plt.show()

def timePlot_all(readTime, minhashTime, xValues, onlyMinhashTime, lshTime, minhashAndLSH, savePath):
	fig, ax1 = plt.subplots()
	ax1.xaxis.set_ticks(xValues)
	ax1.xaxis.set_ticklabels(xValues)

	color = 'tab:red'
	ax1.plot(xValues, readTime, color = color)
	color = 'tab:orange'
	ax1.plot(xValues, onlyMinhashTime, color = color)
	color = 'tab:green'
	ax1.plot(xValues[:-1], minhashTime, color = color)
	ax1.scatter([10000], minhashTime[-1], color = color)
	color = 'tab:blue'
	ax1.plot(xValues, minhashAndLSH, color = color)

	ax1.set_xlabel('number of users/articles', fontsize=14)
	ax1.set_ylabel('time (seconds)', fontsize=14)
	ax1.tick_params(axis='y', labelsize=14)
	ax1.tick_params(axis='x', labelsize=14, rotation = 45)

	readM = mpatches.Patch(color='red', label='terms to hash values')
	generateSignatures = mpatches.Patch(color='orange', label='generate signatures')
	signatureJS = mpatches.Patch(color='green', label='generate signatures \n + JS all combinations \n 10k users -> infinity')
	lshSignatures = mpatches.Patch(color='blue', label='generate signatures \n + LSH')
	leg = plt.legend(handles=[readM, generateSignatures, signatureJS, lshSignatures], frameon = True, loc = 0, ncol = 1, fontsize = "large")

	plt.grid()
	plt.tight_layout()

	plt.savefig(savePath)
	plt.show()
'''
#########################
#########################
MAIN
#########################
#########################
'''
if __name__=='__main__':
	numberOfMinhashes = [2, 10, 20, 50, 100, 200]
	articleNumber = [100, 1000, 2500, 10000]
	#articleNumber = [100, 1000, 2500]
	trueFalseDictionary = {}
	groundTruthPairs = {}

	'''
	for an in articleNumber:
		tmpName = "similarityFiles/"
		tmpName = tmpName + str(an) + "_real_predicted_JS_"

		groundTruthPairs[an] = loadGroundTruth(an)
	
		trueFalseDictionary[an] = {}

		for nom in numberOfMinhashes:
			tmpName_ = tmpName
			tmpName_ = tmpName_ + str(nom) + ".txt"
			print(str(an) + " users - " + str(nom) + " hash functions")
			trueFalseDictionary[an][nom] = MSEandStatistics(tmpName_)
		
		#plots code
		#CDF for ERROR JS
		#cdfMSE(trueFalseDictionary[an], 'error', 'probability', 'CDF of error', "plots/cdf_error_" + str(an) + ".png")
		
		#truePositives-FalseNegatives Plot
		#confusionTable(groundTruthPairs[an], trueFalseDictionary[an], an)
	'''
	#time plots
	xValues = [100, 1000, 2500, 10000]
	#in seconds
	readTime = [0.04007411003112793, 0.3978688716888428, 0.9985969066619873, 3.7036917209625244]
	minhashTime = [20.150715827941895, 93.07991170883179, 538.9515526294708]
	onlyMinhashTime = [10.152915000915527, 34.87178444862366, 273.0862033367157, 13125.667533397675]
	lshTime = [0.022039175033569336, 0.447934627532959, 2.755995512008667, 41.555468797683716]
	minhashAndLSH = [sum(x) for x in zip(onlyMinhashTime, lshTime)]
	timePlot_all(readTime, minhashTime, xValues, onlyMinhashTime, lshTime, minhashAndLSH, "plots/time_all.png")
		