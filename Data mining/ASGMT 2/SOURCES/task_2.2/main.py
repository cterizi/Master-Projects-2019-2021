from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import SpectralClustering
import matplotlib.patches as mpatches
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os

import sklearn 
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm

def plotSilhouetteScore(x, y, file):
	fig, ax = plt.subplots()
	ax.plot(x, y, linewidth=3)

	ax.tick_params(axis='y', labelcolor = "black", labelsize = 15)
	ax.tick_params(axis='x', labelcolor = "black", labelsize = 15, rotation = 50)

	ax.set_ylabel("Silhouette score", fontsize = 25)
	ax.set_xlabel("Number of clusters", fontsize=25)
	plt.xticks(x)

	plt.grid()
	plt.tight_layout()
	plt.savefig("graphVisualization_yesGroups/silhouette_score/" + file.replace(".txt", ".png"))
	plt.show()

def visualizationDtasetForSilhouetteAnalysis(points, cluster_labels, centers, file, n_clusters):
	fig, ax = plt.subplots()
	ax.scatter(points[:, 0], points[:, 1], marker='.', lw=0, alpha=0.7,c=mapColorPerGroup(cluster_labels), edgecolor='k')
	ax.scatter(centers[:, 0], centers[:, 1], marker='+',color='black', s=150)

	ax.set_ylabel("y-coordinates", fontsize = 25)
	ax.set_xlabel("x-coordinates", fontsize=25)

	plt.xticks([])
	plt.yticks([])

	plt.savefig("graphVisualization_yesGroups/silhouette_score/" + file.replace(".txt", "") + "_" + str(n_clusters) + "_clusters.png")
	plt.show()


def visualizationDatasetWithGroups(x, y, c, x_centers, y_centers, clusteringModel, saveName):
	fig, ax = plt.subplots()
	ax.scatter(x, y, marker='.', color=c)

	ax.scatter(x_centers, y_centers, marker='+', color='black', s=150)

	ax.set_ylabel("y-coordinates", fontsize = 25)
	ax.set_xlabel("x-coordinates", fontsize=25)

	plt.xticks([])
	plt.yticks([])

	plt.grid()
	plt.tight_layout()
	# plt.savefig("graphVisualization_yesGroups/" + clusteringModel + "_" + saveName + ".png")
	#plt.savefig("graphVisualization_yesGroups/gaussian_ring_best_sigma/" + clusteringModel + "_" + saveName + ".png")
	plt.show()

def applyKMeans(points, n_clusters):
	kmeans = KMeans(n_clusters = n_clusters).fit(points)
	return(kmeans.labels_, kmeans.cluster_centers_, kmeans.inertia_, kmeans.n_iter_)

def applyAgglomerative(points, n_clusters, linkageType):
	clustering = AgglomerativeClustering(n_clusters = n_clusters, linkage=linkageType).fit(points)
	return(clustering.labels_)

def applySpectral(points, n_clusters, sigma):
	clustering = SpectralClustering(n_clusters=n_clusters, assign_labels="kmeans", affinity='rbf', gamma=sigma).fit(points)
	return(clustering.labels_)

def mapColorPerGroup(labels):
	colors = {0:'red' , 1:'orange', 2:'yellow', 3:'powderblue', 4:'sandybrown', 5:'pink', 6:'lightgreen', 7:'purple', 8:'black'}
	c = []
	for l in labels:
		c.append(colors[l])
	return(c)

def returnCentersCoordinates(centers):
	x = []
	y = []
	for c in centers:
		x.append(c[0])
		y.append(c[1])
	return(x, y)

if __name__ == '__main__':
	actualNumberOfClusters = {'7clusters':7, 
							'3wings':3,
							'5Gaussians':5,
							'3rings':3,
							'4rectangles':4,
							'5gauss_ring':5,
							'6gauss_ring':6,
							'7gauss_ring':7}

	fileNames = os.listdir("files/")

	for file in fileNames:
		f = open("files/" + file, 'r')
		points = []
		for row in f:
			try:
				points.append([float(row.strip().replace("\n", "").split(" ")[0]), float(row.strip().replace("\n", "").split(" ")[-1])])
			except:
				continue
		f.close()

		points = np.array(points)
		x = []
		y = []
		for p in points:
			x.append(p[0])
			y.append(p[1])

		#K-Means
		# [kmeansLabels, kmeans_centers, sumOfSquaredDistances, iterations] = applyKMeans(points, actualNumberOfClusters[file.replace(".txt", "")])
		# kmeans_c = mapColorPerGroup(kmeansLabels)
		# [x_centers, y_centers] = returnCentersCoordinates(kmeans_centers)

		#print(file.replace(".txt", ""), 'kmeans', sumOfSquaredDistances, iterations)
		#visualizationDatasetWithGroups(x, y, kmeans_c, x_centers, y_centers, 'kmeans', file.replace(".txt", ""))
		
		#Agglomerative Clustering, linkage = {single, average}
		# linkage = ['ward', 'average', 'complete', 'single']
		# for la in linkage:
		# 	aggLabels = applyAgglomerative(points, actualNumberOfClusters[file.replace(".txt", "")], la)
			#print(file.replace(".txt", ""), 'agglomerative', la)
			#visualizationDatasetWithGroups(x, y, mapColorPerGroup(aggLabels), [], [], 'aggl_' + la, file.replace(".txt", ""))
		
		#Spectral clustering
		#Notice that delta is proportional to the inverse of the gamma parameter of the 
		#RBF kernel, mentioned earlier in the doc link you give: both are free parameters 
		#which can be used to tune the clustering results.
		# sigmaValues = [0.10, 0.50, 1]
		# for sigma in sigmaValues:
		# 	spectralLabels = applySpectral(points, actualNumberOfClusters[file.replace(".txt", "")], sigma)
			# print(file.replace(".txt", ""), 'spectral', sigma)
			# visualizationDatasetWithGroups(x, y, mapColorPerGroup(spectralLabels), [], [], 'spectral_' + str(sigma), file.replace(".txt", ""))


		#Find the best sigma parameter for gaussian_ring datset
		# if("gauss_ring" in file):
		# 	#gaussian_ring_best_sigma
		# 	sigma_candidate_values = []
		# 	currentValue = 1
		# 	step = 0.50
		# 	finalValue = 20
		# 	while(True):
		# 		if(currentValue + step > finalValue):
		# 			break
		# 		currentValue = currentValue + step
		# 		sigma_candidate_values.append(currentValue)

		# 	for sigma in sigma_candidate_values:
		# 		spectralLabels = applySpectral(points, actualNumberOfClusters[file.replace(".txt", "")], sigma)
		# 		visualizationDatasetWithGroups(x, y, mapColorPerGroup(spectralLabels), [], [], 'spectral_' + str(sigma), file.replace(".txt", ""))


		#Estimate  the number of KMeans cluster using the silhouette criterion
		candidate_n_clusters = []
		for i in range(2, 21):
			candidate_n_clusters.append(i)

		if(not("ring" in file)):
			print(file)
			silhouette_list = []
			for n_clusters in candidate_n_clusters:
				clusterer = KMeans(n_clusters = n_clusters)
				cluster_labels = clusterer.fit_predict(points)
				silhouette_list.append(silhouette_score(points, cluster_labels))
				# if(n_clusters == 5):
				# 	visualizationDtasetForSilhouetteAnalysis(points, cluster_labels, clusterer.cluster_centers_, file, n_clusters)
			# plotSilhouetteScore(candidate_n_clusters, silhouette_list, file)
			for i, j in zip(candidate_n_clusters, silhouette_list):
				print(i, j)

			print("-----------------------")