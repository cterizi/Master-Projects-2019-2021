from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import KFold
from sklearn import metrics
import numpy as np
import csv

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
			tmpDataRow.append(newValue)
		newData.append(tmpDataRow)
	newData = np.asarray(newData)
	return(newData)

if __name__ == '__main__':
	#Load data and labels per record
	[data, labels] = loadData()

	data = normalizeData(data, 0, 1) #range [-1, +1] or [0, +1]

	#Number of classifiers
	n_estimators_list = [25, 50, 75, 100]

	#Values for k-cross validation
	k_list = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

	'''
	with open("nonnormalizedData_bagging.csv", mode='w') as file:
		writer = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['k-crossValidation', 'n_estimators', 'accuracy'])
		file.flush()

		#Apply Bagging classifier
		for k_values in k_list:
			for n_estimators_value in n_estimators_list:
				accuracy_score = 0
				#Apply k-fold cross validation, where k = k_values
				shuffleType = True
				kf = KFold(n_splits = k_values, shuffle = shuffleType)
				for train_index, test_index in kf.split(data): 
					#Train data and labels
					X_train = data[train_index]
					y_train = labels[train_index]

					#Test data and real labels
					X_test = data[test_index]
					y_test = labels[test_index]

					dtc = DecisionTreeClassifier()
					bag_model = BaggingClassifier(base_estimator = dtc, n_estimators = n_estimators_value, bootstrap = True)
					bag_model = bag_model.fit(X_train, y_train)
					y_pred = bag_model.predict(X_test)

					accuracy_score = accuracy_score + metrics.accuracy_score(y_test, y_pred)

				# print(str(k_values) + " - cross validation")
				# print("Total accuracy using " + str(n_estimators_value) + " classifiers: " + str(accuracy_score/k_values))
				writer.writerow([k_values, n_estimators_value, accuracy_score/k_values])
				file.flush()
	'''

	#X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.368)

	#Apply Random Forest classifier
	for n_estimators_value in n_estimators_list:
		rfc = RandomForestClassifier(n_estimators = n_estimators_value, min_samples_leaf = 5, oob_score = True, bootstrap = True)
		rfc.fit(data, labels)
		#rfc = RandomForestClassifier(n_estimators = n_estimators_value, min_samples_leaf = 5)
		#rfc.fit(X_train, y_train)
		#y_pred = rfc.predict(X_test)

		#And lastly, the OOB score is computed as the number of correctly predicted rows from the out of bag sample.
		#In an ideal case, about 36.8 % of the total training data forms the OOB sample.
		#Therefore, about 36.8 % of total training data are available as OOB sample for each DT and 
		#hence it can be used for evaluating or validating the random forest model.
		# raise ValueError("Out of bag estimation only available"
		#ValueError: Out of bag estimation only available if bootstrap=True

		print("Number of estimators: " + str(n_estimators_value))
		#print("Score: " + str(metrics.accuracy_score(y_test, y_pred)))
		print(rfc.oob_score_)

'''
Number of estimators: 25
0.642
Number of estimators: 50
0.663
Number of estimators: 75
0.652
Number of estimators: 100
0.699
'''
		