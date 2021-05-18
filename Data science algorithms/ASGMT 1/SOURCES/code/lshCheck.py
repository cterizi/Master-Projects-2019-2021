import matplotlib.patches as mpatches
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import binascii
import sys
import re

'''
###################################
###################################
global variables
###################################
###################################
'''
global dataCollection


'''
###################################
###################################
Text representation as a set of 
integers
###################################
###################################
'''
def preprocessArticle(path, candidateUsers):
	file = open(path, 'r')
	dataDictionary = {}

	stop_words = set(stopwords.words('english'))

	for line in file:
		tmpLine = line.split(" ")
		articleID = tmpLine[0]
		if(not(articleID in candidateUsers)):
			continue
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
Ground Truth &
Candidate similar pairs of users
###################################
###################################
'''
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

def returnCandidateUsers():
	articleNumber = [100, 1000, 2500, 10000]
	candidatePairs = {}
	candidateUsers = []
	for i in articleNumber:
		candidatePairs[i] = []
		path = "lsh_similarity_files/" + str(i) + ".txt"
		file = open(path, 'r')
		for line in file:
			tmpLine = line.replace("\n", "").split("\t")
			userI = tmpLine[0].replace("\'", "")
			userJ = tmpLine[1].replace("\'", "")
			candidatePairs[i].append((userI, userJ))
			candidateUsers.append(userI)
			candidateUsers.append(userJ)
		file.close()
	return(set(candidateUsers), candidatePairs)


'''
###################################
###################################
Calculate JS, fp, fn, tp, tn
###################################
###################################
'''
def calculateStatistics(groundTruth, candidatePairs):
	global dataCollection

	similarityThreshold = 0.85
	counterForHighSimilarity = 0
	truePositives = 0
	for cp in candidatePairs:
		cpI = cp[0]
		cpJ = cp[1]

		js = (len(dataCollection[cpI].intersection(dataCollection[cpJ])) / len(dataCollection[cpI].union(dataCollection[cpJ])))
		if(js > similarityThreshold):
			counterForHighSimilarity = counterForHighSimilarity + 1
		if(cp in set(groundTruth) or (cpJ, cpJ) in set(groundTruth)):
			truePositives = truePositives + 1
	truePositivesRatio = truePositives / len(groundTruth)
	return(truePositivesRatio)

def plotLSHStatistics(xValues, truePositivesRatio, falseNegativesRatio, savePath):
	fig, ax1 = plt.subplots()

	ax1.xaxis.set_ticks(xValues)
	ax1.xaxis.set_ticklabels(xValues)

	ax1.plot(xValues, truePositivesRatio, color = 'green')
	ax1.plot(xValues, falseNegativesRatio, color = 'red')
	ax1.set_xlabel('number of users per file', fontsize=14)
	ax1.set_ylabel('ratio', color="black", fontsize=14)
	ax1.tick_params(axis='y', labelcolor = "black", labelsize=14)
	ax1.tick_params(axis='x', labelcolor = "black", labelsize=14, rotation = 45)

	truePosRatio = mpatches.Patch(color='green', label='True Positive Ratio')
	falseNegRatio = mpatches.Patch(color='red', label='False Negative Ratio')
	leg = plt.legend(handles=[truePosRatio, falseNegRatio], frameon = True, loc = 0, ncol = 1, fontsize = "x-large")


	plt.grid()
	plt.tight_layout()

	plt.savefig(savePath)
	plt.show()

'''
###################################
###################################
MAIN
###################################
###################################
'''
if __name__=='__main__':
	global dataCollection

	#read the articles (and convert them in a set of hash values) from the candidate pairs/users
	[candidateUsers, candidatePairsPerFile] = returnCandidateUsers()
	dataCollection = preprocessArticle("data/articles_10000.txt", candidateUsers)
	
	articleNumber = [100, 1000, 2500, 10000]
	groundTruthPairs = {}

	truePositivesRatio = []
	for an in articleNumber:
		groundTruthPairs[an] = loadGroundTruth(an)
		truePositivesRatio.append(calculateStatistics(groundTruthPairs[an], candidatePairsPerFile[an]))
		print(len(candidatePairsPerFile[an]))
	#plot true positives ratio, false positives and false negatives
	#falsePositivesList = [0, 8, 2, 40]
	falseNegativesRatio = [0, 0, 0, 0.5]
	plotLSHStatistics(articleNumber, truePositivesRatio, falseNegativesRatio, "plots/lsh_statistics.png")
