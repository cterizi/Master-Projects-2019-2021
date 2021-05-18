from nltk.corpus import stopwords
import scipy.sparse as sp_sparse
#nltk.download('stopwords')
from random import randint
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import collections
import binascii
import operator
import random
import nltk
import time
import math
import sys
import os
import re

'''
###################################
###################################
global parameters
###################################
###################################
'''
global inputParameterForFileName

'''
###################################
###################################
Step 1: Text representation as a 
set of integers
###################################
###################################
'''
def preprocessArticle(path):
	file = open(path, 'r')
	dataDictionary = {}

	stop_words = set(stopwords.words('english'))

	for line in file:
		tmpLine = line.split(" ")
		articleID = tmpLine[0]

		filtered_sentence = [w for w in tmpLine[1:] if not w in stop_words]

		for word in range(0, len(filtered_sentence)):
			filtered_sentence[word] = re.sub(r'[^\w]', ' ', filtered_sentence[word])
			filtered_sentence[word] = filtered_sentence[word].lower()
		
		dataDictionary[articleID] = createSetsFromStrings(filtered_sentence)
	file.close()
	return(dataDictionary)

def createSetsFromStrings(article):
	shinglesInDoc = set()
	for index in range(0, len(article) - 2):
		shingle = article[index] + " " + article[index + 1] + " " + article[index + 2]
		hashValue = binascii.crc32(shingle.encode('utf-8')) & 0xffffffff
		shinglesInDoc.add(hashValue)
	return(shinglesInDoc)


'''
###################################
###################################
Write files with real and predicted 
similarity and pairs of users
###################################
###################################
'''


'''
###################################
###################################
Step 2: MinHash Implementation
###################################
###################################
'''
def make_random_hash_function(totalDiscreteHashValues):
	l = []
	p = 2**33 - 355
	m = len(totalDiscreteHashValues)
	a = randint(1, p - 1) 
	b = randint(0, p - 1)

	for i in range(0, len(totalDiscreteHashValues)):
		pp = ((a * i + b) % p) % m
		l.append(pp)

	return(l)

def createTableForHashes(numberOfRows, numberOfColumns):
	signaturesTable = []
	for i in range(0, numberOfRows):
		number = math.pow(2,50)
		tmpList = [number] * numberOfColumns
		signaturesTable.append(tmpList)
	signaturesTable = np.array(signaturesTable)
	return (signaturesTable)

def minhash(d, mapIDsWithIntegers):
	global inputParameterForFileName

	#numberOfMinhashes = [2, 10, 20, 50, 100, 200]
	numberOfMinhashes = [200]
	percentageCutDictionary = {100:1 , 1000:0.1 , 2500:0.1 , 10000:0.0001}

	totalDiscreteHashValues = []
	totalDiscreteHashValues_ = []
	for i in d:
		for j in d[i]:
			totalDiscreteHashValues_.append(j)
	counter = collections.Counter(totalDiscreteHashValues_)
	sortedWords = sorted(counter.items(), key=operator.itemgetter(1))[::-1]

	if(inputParameterForFileName == 100):
		xxx = int(percentageCutDictionary[inputParameterForFileName] * len(set(totalDiscreteHashValues_)))
		top = sortedWords[0:xxx]
		for i in top:
			totalDiscreteHashValues.append(i[0])
	elif(inputParameterForFileName == 10000):
		counter_ = 0
		for ii in sortedWords:
			if(ii[1] >= 2):
				totalDiscreteHashValues.append(ii[0])
		#shuffle
		#random.shuffle(totalDiscreteHashValues)
		#totalDiscreteHashValues = totalDiscreteHashValues[0:350000]
		#print(len(totalDiscreteHashValues))
	else:
		counter_ = 0
		for ii in sortedWords:
			if(ii[1] >= 2):
				totalDiscreteHashValues.append(ii[0])
	
	dictionaryHashValuesColumnsEqualsOne = {}

	for userID in mapIDsWithIntegers:
		if(userID == 1000 or userID == 2000 or userID == 5000 or userID == 7000 or userID == 9000):
			print(userID)
		for w in range(0, len(totalDiscreteHashValues)):
			if(totalDiscreteHashValues[w] in set(d[mapIDsWithIntegers[userID]])):
				if(w in set(list(dictionaryHashValuesColumnsEqualsOne.keys()))):
					dictionaryHashValuesColumnsEqualsOne[w].append(userID)
				else:
					dictionaryHashValuesColumnsEqualsOne[w] = [userID]
		
	#create hash vectors
	#gia kathe user ftiaxe dictionary me to signatures gia kathe periptwsh plhthous functions
	for i in numberOfMinhashes:
		print("#hash vectors: " + str(i))
		hashVector = []
		for j in range(0, i):
			hashVector.append(make_random_hash_function(totalDiscreteHashValues))
		hashVector = np.array(hashVector)
	
		table = createTableForHashes(i, len(set(list(mapIDsWithIntegers.keys()))))

		#gia thn prwth hash value pare tis times 
		for j in range(0, len(totalDiscreteHashValues)):
			wordIdRow = j
			tmpHashVector = []
			for jj in hashVector:
				tmpHashVector.append(jj[wordIdRow])
			
			columnsToEdit = set(dictionaryHashValuesColumnsEqualsOne[j])
			for kk in range(0, len(tmpHashVector)):
				for jjj in columnsToEdit:
					if(table[kk][jjj] > tmpHashVector[kk]):
						table[kk][jjj] = tmpHashVector[kk]
		
		if(i == 200):
			totalSignatureTable = table

		#calculate JS for signatures
		#gia kathe user ftiaxe dictionary me to signatures
		signaturesDictionary = {}
		for userID in mapIDsWithIntegers:
			tmpLL = []
			for j in range(0, len(table)):
				tmpLL.append(table[j][userID])
			signaturesDictionary[userID] = set(tmpLL)
		
		
		#calculate real and approximate Jaccard similarity
		[predictedPairsAbove085, predictedPairs] = calculateJaccardSimilarity(d, mapIDsWithIntegers, signaturesDictionary, i, inputParameterForFileName)
		#writeFiles(predictedPairsAbove085, predictedPairs)
	return(totalSignatureTable, totalDiscreteHashValues)

def calculateJaccardSimilarity(d, mapIDsWithIntegers, predicted, numberOfHashes, numberOfArticlesFileName):
	totalPairsSimilarityAbove085 = 0
	realPairs = []
	predictedPairsAbove085 = 0
	predictedPairs = []
	
	fileForError = open("similarityFiles/" + str(numberOfArticlesFileName) + "_real_predicted_JS_" + str(numberOfHashes) + ".txt", 'w')

	for i in range(0, len(d.keys())):
		print(i)
		for j in range(i + 1, len(d.keys())): #for each pair of users calculate jaccard similarity in real set of hash(words)
			js = (len(d[mapIDsWithIntegers[i]].intersection(d[mapIDsWithIntegers[j]])) / len(d[mapIDsWithIntegers[i]].union(d[mapIDsWithIntegers[j]])))
			jsPredicted = (len(predicted[i].intersection(predicted[j])) / len(predicted[i].union(predicted[j])))

			fileForError.write(str(mapIDsWithIntegers[i]) + "\t" + str(mapIDsWithIntegers[j]) + "\t" + str(js) + "\t" + str(jsPredicted) + "\n")

			if(js > 0.85):
				realPairs.append((mapIDsWithIntegers[i], mapIDsWithIntegers[j]))
				totalPairsSimilarityAbove085 = totalPairsSimilarityAbove085 + 1
			if(jsPredicted > 0.85):
				predictedPairsAbove085 = predictedPairsAbove085 + 1
				predictedPairs.append((mapIDsWithIntegers[i], mapIDsWithIntegers[j]))
	
	fileForError.close()
	print("#pairs JS > 0.85: " + str(totalPairsSimilarityAbove085))
	print("#pairs JS (predicted) > 0.85: " + str(predictedPairsAbove085))
	print("-------------------------------")
	return(predictedPairsAbove085, predictedPairs)


'''
###################################
###################################
Locality Sensitive Hashing
###################################
###################################
'''
def plotBestParameter(r, b):
	actualY = []

	y = []
	x = []
	startT = 0.0
	step = 0.01
	finishT = 1.0
	while(True):
		if(startT > finishT):
			break
		x.append(startT)
		A = 1 - math.pow(1 - math.pow(startT, r), b)
		y.append(A)
		
		if(startT < 0.85):
			actualY.append(0)
		elif(startT >= 0.85):
			actualY.append(1)
		startT = startT + step

	fig, ax1 = plt.subplots()
	ax1.plot(x, y, 'green')
	ax1.plot(x, actualY, 'red')
	ax1.set_xlabel('similarity', fontsize=14)
	ax1.set_ylabel('probability of candidacy', fontsize=14)
	ax1.tick_params(axis='y', labelsize=14)
	ax1.tick_params(axis='x', labelsize=14)
	plt.title("r = " + str(r) + ", b = " + str(b), loc = 'center', fontsize = 15, color = 'orange') 
	
	redLine = mpatches.Patch(color='red', label='desired approach\nsimilarity threshold 0.80')
	greenLine = mpatches.Patch(color='green', label='approach of s ~ (1/b)^(1/r)')
	leg = plt.legend(handles=[redLine, greenLine], frameon = True, loc = 0, ncol = 1, fontsize = "large")

	plt.grid()
	plt.tight_layout()

	plt.savefig("plots/r" + str(r) + "b" + str(b) +"_.png")
	plt.show()


def selectParameters():
	similarityValues = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
	#maxRows/Signatures = 200
	maxRows = 200
	totalT = []
	stepR = [5, 6, 7, 8, 9, 10, 11, 12]
	for r in stepR: 
		t = []
		for s in similarityValues:
			b = round(float(maxRows) / r)
			q1 = 1 - math.pow(1 - math.pow(s, r), b)
			t.append(q1)
		totalT.append(t)	
	bestParameter(similarityValues, totalT)

def bestParameter(x, y):
	fig, ax1 = plt.subplots()
	colors = ['yellow', 'pink', 'orange', 'red', 'purple', 'brown', 'blue', 'black']
	for i in range(0,  len(y)):
		ax1.plot(x, y[i], color = colors[i])
	
	ax1.set_xlabel('similarity', fontsize=14)
	ax1.set_ylabel('probability of candidacy', fontsize=14)
	ax1.tick_params(axis='y', labelsize=14)
	ax1.tick_params(axis='x', labelsize=14)

	rows5 = mpatches.Patch(color='yellow', label='5 rows per band')
	rows6 = mpatches.Patch(color='pink', label='6 rows per band')
	rows7 = mpatches.Patch(color='orange', label='7 rows per band')
	rows8 = mpatches.Patch(color='red', label='8 rows per band')
	rows9 = mpatches.Patch(color='purple', label='9 rows per band')
	rows10 = mpatches.Patch(color='brown', label='10 rows per band')
	rows11 = mpatches.Patch(color='blue', label='11 rows per band')
	rows12 = mpatches.Patch(color='black', label='12 rows per band')
	
	leg = plt.legend(handles=[rows5, rows6, rows7, rows8, rows9, rows10, rows11, rows12], frameon = True, loc = 0, ncol = 1, fontsize = "large")

	plt.grid()
	plt.tight_layout()

	plt.savefig("plots/selectParameter_best.png")
	plt.show()

def LSH(M, rows, band, mapID):
	bucketDictionary = {}
	falsePosotivesCounter = 0
	falseNegativesCounter = 0

	initialStep = 0
	step = rows
	finalStep = len(M)

	allPossiblePairs = []

	while(True):
		bucketDictionary = {}

		if(initialStep >= finalStep):
			break
		if(initialStep + step > finalStep):
			tmpM = M[initialStep : finalStep]
		else:
			tmpM = M[initialStep : initialStep + step]

		#put every columns in a bucket
		for i in range(0, len(M[0])):
			tmpShortSignature = []
			for j in range(0, step):
				try:
					tmpShortSignature.append(tmpM[j][i])
				except:
					break
			tmpShortSignature.sort()
			tmpShortSignature = str(tmpShortSignature)

			if(tmpShortSignature in set(bucketDictionary.keys())):
				bucketDictionary[tmpShortSignature].append(i)
			else:
				bucketDictionary[tmpShortSignature] = [i]
		
		for i in bucketDictionary:
			if(len(bucketDictionary[i]) >= 2):
				tmpListOfIDs = []
				for j in bucketDictionary[i]:
					tmpListOfIDs.append(mapID[j])
				tmpListOfIDs = tuple(tmpListOfIDs)
				allPossiblePairs.append(tmpListOfIDs)
		
		#update parameters
		initialStep = initialStep + step

	return(set(allPossiblePairs))

def writeLSHpairs(data, path):
	file = open(path, 'w')
	for i in data:
		userI = i[0].replace("\'", "")
		userJ = i[1]
		file.write(userI + "\t" + userJ + "\n")
	file.close()

'''
###################################
###################################
MAIN
###################################
###################################
'''
if __name__=='__main__':
	#STEP 1
	global inputParameterForFileName

	inputParameterForFileName = int(sys.argv[1])
	fileName = "articles_" + sys.argv[1] + ".txt"
	readTimeStart = time.time()
	dataCollection = preprocessArticle("data/" + fileName)
	readTimeEnd = time.time()
	print("Read time: " + str(readTimeEnd - readTimeStart) + " seconds")


	#STEP 2
	totalIDs = dataCollection.keys()
	mapIDsWithIntegers = {}
	tmpID = 0
	for t in totalIDs:
		mapIDsWithIntegers[tmpID] = t
		tmpID = tmpID + 1

	minhashJSStart = time.time()
	[signatureTable, totalDiscreteHashValues]= minhash(dataCollection, mapIDsWithIntegers)
	minhashJSEnd = time.time()
	print("Minhash JS time: " + str(minhashJSEnd - minhashJSStart) + " seconds")

	#STEP 3
	#selectParameters()
	totalSignatures = 200
	bestR = 12
	bestB = round(float(totalSignatures) / bestR)
	#plotBestParameter(bestR, bestB)
	lshStart = time.time()
	possiblePairs = LSH(signatureTable, bestR, bestB, mapIDsWithIntegers)
	lshEnd = time.time()
	print("LSH time: " + str(lshEnd - lshStart) + " seconds")
	writeLSHpairs(possiblePairs, "lsh_similarity_files/" + str(inputParameterForFileName) + ".txt")
	print("possible pairs: " + str(len(possiblePairs)))
	
