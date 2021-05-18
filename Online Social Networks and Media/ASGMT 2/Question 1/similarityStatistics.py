'''
clusterModularity.txt
clusterSize.txt
communities.txt
similarityFileForAllPairOfClusters.txt
'''

'''
{'WWW (Companion Volume)': 1, 
'KDD': 2, 
'ICDE': 3, 
'KDD Cup': 4, 
'SDM': 5, 
'CIKM': 6, 
'WWW': 7, 
'ICDM': 8, 
'SIGMOD Conference': 9, 
'SIGIR': 10, 
'EDBT': 11, 
'VLDB': 12}
'''
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from collections import Counter
import networkx as nx
import numpy as np
import statistics
import operator

def loadGraph():
	G = nx.Graph()
	file = open("graph/dblp_graph", 'r')
	for line in file:
		tmp_line = line.replace("\n", "").split("\t")
		source = int(tmp_line[0])
		target = int(tmp_line[1])
		G.add_edge(source, target)
	file.close()
	return(G)

def loadModularity():
	file = open("clusterModularity.txt", 'r')
	modularityDict = {}
	for line in file:
		tmp_line = line.replace("\n", "").split("\t")
		community = int(tmp_line[0])
		modularity = float(tmp_line[1])
		modularityDict[community] = modularity
	file.close()
	return(modularityDict)

def loadSize():
	file = open("clusterSize.txt", 'r')
	sizeDict = {}
	for line in file:
		tmp_line = line.replace("\n", "").split("\t")
		community = int(tmp_line[0])
		size = float(tmp_line[1])
		sizeDict[community] = size
	file.close()
	return(sizeDict)

def loadCommunities():
	file = open("communities.txt", 'r')
	data = {}
	tmp_community_id = 0
	for line in file:
		tmp_line = line.replace("\n", "")
		if("Community:" in tmp_line):
			tmp_community_id = tmp_community_id + 1
			data[tmp_community_id] = []
		elif("The modularity of the network is" in tmp_line):
			break
		else:
			data[tmp_community_id].append(int(tmp_line))
	file.close()
	return(data)

def loadLabels():
	mapConferenceID = {"WWW (Companion Volume)": 1, "KDD": 2, "ICDE": 3, 
					"KDD Cup": 4, "SDM": 5, "CIKM": 6, "WWW": 7, 
					"ICDM": 8, "SIGMOD Conference": 9, "SIGIR": 10, 
					"EDBT": 11, "VLDB": 12}
	file = open("graph/dblp_authors_conf.txt", 'r')
	data = {}
	for line in file:
		tmp_line = line.replace("\n", "").split("\t")
		user = int(tmp_line[0])
		conference = mapConferenceID[tmp_line[1]]
		if(not(user in set(list(data.keys())))):
			data[user] = [conference]
		else:
			data[user].append(conference)
	file.close()
	return(data)

def loadClusterModularity():
	file = open("similarityFileForAllPairOfClusters.txt", 'r')
	similarityTuple = []
	#how many pairs of clusters have average similarity equals 1.0
	#print size of these clusters
	#labels of these clusters
	for line in file:
		tmp_line = line.replace("\n", "").split(" ")
		cluster_i = int(tmp_line[0])
		cluster_j = int(tmp_line[1])
		similarity = float(tmp_line[2])
		similarityTuple.append((cluster_i, cluster_j, similarity))
	file.close()
	return(similarityTuple)

def cdfModularitySize(data, tp):
	A = np.sort(data)
	p = 1. * np.arange(len(A)) / (len(A) - 1)
	fig, ax1 = plt.subplots()
	
	if(tp == "modularity"):
		ax1.set_xlabel("modularity of clusters", fontsize=15)
		plt.title("Cumulative distribution of modularity of clusters", loc = 'center', fontsize = 15, color = 'orange')
	elif(tp == "Homogeneity"):
		ax1.set_xlabel("homogeneity of clusters", fontsize=15)
		plt.title("Cumulative distribution of homogeneity of clusters", loc = 'center', fontsize = 15, color = 'orange')
	else:
		ax1.set_xlabel("size of clusters", fontsize=15)
		plt.title("Cumulative distribution of size of clusters", loc = 'center', fontsize = 15, color = 'orange')
	ax1.set_ylabel("probability", fontsize=15)
	ax1.tick_params(axis='y', labelcolor = "black", labelsize=15)
	ax1.tick_params(axis='x', labelcolor = "black", labelsize=15)
	plt.grid()
	plt.tight_layout()

	plt.plot(A, p)
	if(tp == "modularity"):
		plt.savefig("modularity_cdf.png")
	elif(tp == "Homogeneity"):
		plt.savefig("homogeinity_cdf.png")
	else:
		plt.savefig("size_cdf.png")

	plt.show()

def numberOfHigherClusters(x):
	higherPairs = []
	totalNumber = 0
	for i in x:
		if(i[2] > 0.85):
			totalNumber = totalNumber + 1
			higherPairs.append((i[0], i[1]))
	print("Number of higher pairs: " + str(totalNumber))
	return(higherPairs)

def calculateStatistics(modularity, size, communities, labels, clusterModularity):
	#cdfModularitySize(list(modularity.values()), "modularity")
	#cdfModularitySize(list(size.values()), "size")
	#higerPairs = numberOfHigherClusters(clusterModularity)
	# cdfModularityList = []
	# for i in clusterModularity:
	# 	cdfModularityList.append(i[2])
	# cdfModularitySize(cdfModularityList, "Homogeneity")
	whichClusterHasBestSimilarity = []
	for i in clusterModularity:
		if(i[2] > 0.85):
			whichClusterHasBestSimilarity.append(i[0])
			whichClusterHasBestSimilarity.append(i[1])
	counter_ = Counter(whichClusterHasBestSimilarity)
	sorted_x = sorted(counter_.items(), key=operator.itemgetter(1))[::-1]
	maxNumber = 243
	bestCommunityIDs = []
	for i in sorted_x:
		if(i[1] == maxNumber):
			bestCommunityIDs.append(i[0])
	bestModularityIDs = []
	bestSizeIDs = []
	for i in bestCommunityIDs:
		bestModularityIDs.append(modularity[i])
		bestSizeIDs.append(size[i])
	cdfModularitySize(bestModularityIDs, "modularity")
	cdfModularitySize(bestSizeIDs, "size")
	CCC = 0
	
def modularityEdgesInCommunities(graph, modularity, communities, size):
	A = graph.degree()
	sumAllDegrees = 0
	totalNodes = graph.number_of_nodes()
	degreeList = []
	for i in A:
		sumAllDegrees = sumAllDegrees + i[1]
		degreeList.append(i[1])
	averageDegree = int(float(sumAllDegrees) / totalNodes)
	
	expectedNumberOfEdges = {}
	realNumberOfEdgesInCommunities = {}
	for i in communities:
		expectedNumberOfEdges[i] = averageDegree * size[i]
		realNumberOfEdgesInCommunities[i] = 0

	for e in graph.edges():
		for com in communities:
			allNodesInCommunity = set(communities[com])
			if(e[0] in allNodesInCommunity and e[1] in allNodesInCommunity):
				realNumberOfEdgesInCommunities[com] = realNumberOfEdgesInCommunities[com] + 1
				break
	
	
	

def main():
	#g = loadGraph()
	m = loadModularity()
	s = loadSize()
	#c = loadCommunities()
	#l = loadLabels()
	clmd = loadClusterModularity()
	calculateStatistics(m, s, 0, 0, clmd)
	#calculateStatistics(m, s, c, l, clmd)
	#modularityEdgesInCommunities(g, m, c, s)

main()