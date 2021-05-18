import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib import cm as cm
import seaborn as sns
import numpy as np

def readSimilarityFile():
	file = open("similarityFileForAllPairOfClusters.txt", 'r')
	data = {}
	similarityDict = {}
	for line in file:
		tmp_line = line.replace("\n", "").split(" ")
		cluster_i = int(tmp_line[0])
		cluster_j = int(tmp_line[1])
		similarity = float(tmp_line[2])

		if(not(cluster_i in set(list(data.keys())))):
			data[cluster_i] = [cluster_j]
			similarityDict[cluster_i] = [similarity]

			if(cluster_i > 1):
				if(cluster_i == cluster_j):
					for t in range(0, cluster_i - 1):
						similarityDict[cluster_i] = [-1] + similarityDict[cluster_i]
		else:
			data[cluster_i].append(cluster_j)
			similarityDict[cluster_i].append(similarity)

	heatData = []
	for i  in similarityDict:
		heatData.append(similarityDict[i])
	heatData = np.array(heatData)

	#heatmap code
	mask = np.tril(heatData)
	xticklabels = []
	yticklabels = []
	for i in range (1, 1954):
		xticklabels.append(i)
		yticklabels.append(i)
	
	fig, ax = plt.subplots()
	ax.set_xticks(xticklabels)
	ax.set_yticks(yticklabels)
	ax.tick_params(axis='y', labelcolor = "black", labelsize=12, rotation = 90)
	ax.tick_params(axis='x', labelcolor = "black", labelsize=12, rotation = 90)
	ax = sns.heatmap(heatData, mask=mask)
	ax.set_ylabel("community ID", fontsize=14)
	ax.set_xlabel("community ID", fontsize=14)
	plt.title("Homogeneity of the clusters", loc = 'center', fontsize = 15, color = 'orange')
	plt.grid()
	plt.tight_layout()

	plt.savefig('heatmapClusterSimilarity_bestPoints.png')
	plt.show()
	
	file.close()

def main():
	readSimilarityFile()

main()