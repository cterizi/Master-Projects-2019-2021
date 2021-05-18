'''
##############################################################################
##############################################################################
Import the libraries
##############################################################################
##############################################################################
'''
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import numpy as np
import csv
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib


'''
##############################################################################
##############################################################################
Functions
1. load data
##############################################################################
##############################################################################
'''
def loadData():
	data = []
	labels = []
	with open("Terizi.csv") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			data.append([float(i) for i in row[:-1]])
			'''
			Due to the fact that SVM uses as labels the values {0, 1},
			I convert the labels as follows,
			label 1 -> becomes 0
			label 2 -> becomes 1
			'''
			if(int(row[-1]) == 1):
				labels.append(0)
			elif(int(row[-1]) == 2):
				labels.append(1)
	data = np.asarray(data)
	labels = np.asarray(labels)
	return(data, labels)


def normalizeData(data, borderLeft, borderRight):
	numberOFFeatures = len(data[0])
	minMax = {}
	for i in range(0, numberOFFeatures):
		valuesPerFeature = []
		for dataRow in data:
			valuesPerFeature.append(dataRow[i])

		minMax[i] = [min(valuesPerFeature), max(valuesPerFeature)] #min, max

	newData = []
	for dataRow in data:
		tmpDataRow = [] #new ranges [-1, +1]
		for i in range(0, numberOFFeatures):
			a = minMax[i][0]
			b = minMax[i][1]
			c = borderLeft
			d = borderRight
			x = dataRow[i]
			newValue = (((d - c) * (x - a)) / (b - a)) + c

			'''
				For the 1 and 2 features (index 0 and 1), 
				I will change the range of values. The initial 
				range is [-2.5, +2.5]. The new range is [2, 3].
			'''
			# if(i == 0 or i == 1):
			# 	c = 2
			# 	d = 3
			# 	newValue = (((d - c) * (dataRow[i] - minMax[i][0])) / (minMax[i][1] - minMax[i][0])) + c
			
			tmpDataRow.append(newValue)

		newData.append(tmpDataRow)
	newData = np.asarray(newData)
	return(newData)

	
def detectNoise(data, saveName):
	numberOFFeatures = len(data[0])
	for i in range(0, numberOFFeatures): #i is the index for each feature
		dataFeature = []
		for dataRow in data:
			dataFeature.append(dataRow[i])

		#Histogram
		n_bins = 900
		fig, ax = plt.subplots()
		ax.hist(dataFeature, bins = n_bins)

		ax.set_ylim(top = 10)
		ax.set_ylim(bottom = -0.10)
		ax.set_xlim(left = -0.50)
		ax.set_xlim(right = 1.5)


		plt.title("Feature " + str(i + 1) + ", n_bins = " + str(n_bins), loc = 'center', fontsize = 14, color = 'orange')
		plt.grid()
		plt.tight_layout()
		plt.savefig("histogram/" + saveName + "_" + str(i) + ".png")
		plt.show()

		# if(i == 1):
		# 	break


def specificData(data, labels, labelValue):
	tmpData = []
	for i in range(0, len(labels)):
		if(labels[i] == labelValue):
			tmpData.append(list(data[i]))
	tmpData = np.asarray(tmpData)
	labels = [labelValue]*len(tmpData)
	labels = np.asarray(labels)
	return(tmpData, labels)


def dt(X_train, y_train, X_test, y_test, criterion, splitter):
	if(criterion == "" and splitter == ""):
		clf = DecisionTreeClassifier()
	else:
		clf = DecisionTreeClassifier(criterion=criterion, splitter=splitter)
	clf = clf.fit(X_train, y_train)
	y_pred = clf.predict(X_test)
	return(metrics.accuracy_score(y_test, y_pred))


'''
##############################################################################
##############################################################################
Main code
##############################################################################
##############################################################################
'''
if __name__=='__main__':
	#Load data and labels per record
	[data, labels] = loadData()

	data = normalizeData(data, 0, 1) #range [-1, +1] or [0, +1]

	# [data_zero, labels_zero] = specificData(data, labels, 0)
	# [data_one, labels_one] = specificData(data, labels, 1)
	#detectNoise(data, "all")
	#detectNoise(data_zero, "zero")
	#detectNoise(data_one, "one")
	
	
	#Apply k-fold cross validation, where k=10
	k = 10
	shuffleType = True
	kf = KFold(n_splits = k, shuffle = shuffleType)




	'''	
	#check more than one values for n_neighbors parameter of kNN algorithm
	n_neighbors_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	for n_neighbors_value in n_neighbors_values:
		accuracySum = 0
		for train_index, test_index in kf.split(data): 
			#Train data and labels
			X_train = data[train_index]
			y_train = labels[train_index]

			#Test data and real labels
			X_test = data[test_index]
			y_test = labels[test_index]

			#Apply kNN
			knn = KNeighborsClassifier(n_neighbors = n_neighbors_value) #Create KNN Classifier
			knn.fit(X_train, y_train) #Train the model using the training sets
			y_pred = knn.predict(X_test) #Predict the response for test dataset

			accuracy = metrics.accuracy_score(y_test, y_pred) #how often is the classifier correct?
			accuracySum = accuracySum + accuracy
			
		finalAccuracy = accuracySum / k

		knnFile = open("results/knn.txt", 'a')
		knnFile.write("kNN, " + str(n_neighbors_value) + " neighbors, " + str(finalAccuracy) + "\n")
		knnFile.close()
	
	
	#Apply k-fold cross validation
	accuracySum = 0
	for train_index, test_index in kf.split(data):
		#Train data and labels
		X_train = data[train_index]
		y_train = labels[train_index]

		#Test data and real labels
		X_test = data[test_index]
		y_test = labels[test_index]

		#Apply Naïve Bayes
		gnb = GaussianNB()
		y_pred = gnb.fit(X_train, y_train).predict(X_test)

		accuracy = metrics.accuracy_score(y_test, y_pred) #how often is the classifier correct?
		accuracySum = accuracySum + accuracy
	finalAccuracy = accuracySum / k

	gnbFile = open("results/GaussianNB.txt", 'a')
	gnbFile.write("Naïve Bayes, " + str(finalAccuracy) + "\n")
	gnbFile.close()

	
	#Apply k-fold cross validation
	accuracySum = 0
	for train_index, test_index in kf.split(data):
		#Train data and labels
		X_train = data[train_index]
		y_train = labels[train_index]

		#Test data and real labels
		X_test = data[test_index]
		y_test = labels[test_index]

		#Apply SVM - linear kernel
		svclassifier = SVC(kernel='linear')
		svclassifier.fit(X_train, y_train)
		y_pred = svclassifier.predict(X_test)

		accuracy = metrics.accuracy_score(y_test, y_pred) #how often is the classifier correct?
		accuracySum = accuracySum + accuracy
	finalAccuracy = accuracySum / k

	linearSVMFile = open("results/svm_linear.txt", 'a')
	linearSVMFile.write("SVM - Linear kernel, " + str(finalAccuracy) + "\n")
	linearSVMFile.close()
	'''

	'''
	gamma = [] #spread
	step = 0.01
	initialValue = 0.01
	finalValue = 0.10
	tmpStop = initialValue
	while(True):
		if(initialValue > finalValue):
			break
		gamma.append(initialValue)
		initialValue = initialValue + step
	
	C = [] #penalty
	step = 10
	initialValue = 1000
	finalValue = 1000000
	tmpStop = initialValue
	while(True):
		if(initialValue > finalValue):
			break
		C.append(initialValue)
		initialValue = initialValue * step


	# gamma = [0.00000001]
	# C = [10000000]
	for c_value in C:
		for gamma_value in gamma:
			#print("C: " + str(c_value) + ", gamma: " + str(gamma_value))
			accuracySum = 0
			for train_index, test_index in kf.split(data):
				#Train data and labels
				X_train = data[train_index]
				y_train = labels[train_index]

				#Test data and real labels
				X_test = data[test_index]
				y_test = labels[test_index]

				#Apply SVM - RBF
				svm = SVC(kernel='rbf', random_state = 0, gamma=gamma_value, C=c_value)
				svm.fit(X_train, y_train)
				y_pred = svm.predict(X_test)

				accuracy = metrics.accuracy_score(y_test, y_pred) #how often is the classifier correct?
				accuracySum = accuracySum + accuracy
			finalAccuracy = accuracySum / k
			if(finalAccuracy > 0.80):
				print("SVM - RBF kernel, C: " + str(c_value) + ", Gamma: " + str(gamma_value) + ", " + str(finalAccuracy))
				svmRBFFile = open("results/svm_rbf_new.txt", 'a')
				svmRBFFile.write("SVM - RBF kernel, C: " + str(c_value) + ", Gamma: " + str(gamma_value) + ", " + str(finalAccuracy) + "\n")
				svmRBFFile.close()
	(for example, 𝐶=2−5,2−3,…,215;𝛾=2−15,2−13,…,23).
	'''		
	
	#Apply k-fold cross validation
	accuracySum_simple = 0
	accuracySum_entropy_best = 0
	accuracySum_entropy_random = 0
	accuracySum_gini_best = 0
	accuracySum_gini_random = 0
	for train_index, test_index in kf.split(data):
		#Train data and labels
		X_train = data[train_index]
		y_train = labels[train_index]

		#Test data and real labels
		X_test = data[test_index]
		y_test = labels[test_index]

		accuracySum_simple = accuracySum_simple + dt(X_train, y_train, X_test, y_test, "", "")
		accuracySum_entropy_best = accuracySum_entropy_best + dt(X_train, y_train, X_test, y_test, "entropy", "best")
		accuracySum_entropy_random = accuracySum_entropy_random + dt(X_train, y_train, X_test, y_test, "entropy", "random")
		accuracySum_gini_best = accuracySum_gini_best + dt(X_train, y_train, X_test, y_test, "gini", "best")
		accuracySum_gini_random = accuracySum_gini_random + dt(X_train, y_train, X_test, y_test, "gini", "random")

	finalAccuracy_simple = accuracySum_simple / k
	finalAccuracy_entropy_best = accuracySum_entropy_best / k
	finalAccuracy_entropy_random = accuracySum_entropy_random / k
	finalAccuracy_gini_best = accuracySum_gini_best / k
	finalAccuracy_gini_random = accuracySum_gini_random / k

	print("Decision Tree - Default, " + str(finalAccuracy_simple))
	print("Decision Tree - Entropy-Best, " + str(finalAccuracy_entropy_best))
	print("Decision Tree - Entropy-Random, " + str(finalAccuracy_entropy_random))
	print("Decision Tree - Gini-Best, " + str(finalAccuracy_gini_best))
	print("Decision Tree - Gini-Random, " + str(finalAccuracy_gini_random))



	maxDepth = []
	for i in range(1, 1000):
		maxDepth.append(i)

	minSamplesLeaf = []
	for i in range(1, 501):
		minSamplesLeaf.append(i)

	for minSamplesLeaf_value in minSamplesLeaf:
		for maxDepth_value in maxDepth:
			accuracySum = 0
			for train_index, test_index in kf.split(data):
				#Train data and labels
				X_train = data[train_index]
				y_train = labels[train_index]

				#Test data and real labels
				X_test = data[test_index]
				y_test = labels[test_index]

				clf = DecisionTreeClassifier(max_depth=maxDepth_value, min_samples_leaf=minSamplesLeaf_value)
				clf = clf.fit(X_train, y_train)
				y_pred = clf.predict(X_test)
				accuracySum = accuracySum + metrics.accuracy_score(y_test, y_pred)
			finalAccuracy = accuracySum / k
			#print(minSamplesLeaf_value, maxDepth_value, finalAccuracy)
			if(finalAccuracy > 0.70):
				print("Decision Tree, max_depth: " + str(maxDepth_value) + ", leaf_size: " + str(minSamplesLeaf_value) + "\t" + str(finalAccuracy))
				dtFile = open("results/decisionTree.txt", 'a')
				dtFile.write("Leaf size: " + str(minSamplesLeaf_value) + ", max depth " + str(maxDepth_value) + ", " + str(finalAccuracy) + "\n")
				dtFile.close()
