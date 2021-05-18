import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os

def visualizeDatasetWithoutGroups(x, y, saveName):
	fig, ax = plt.subplots()
	ax.scatter(x, y, marker='.')

	ax.set_ylabel("y-coordinates", fontsize = 25)
	ax.set_xlabel("x-coordinates", fontsize=25)

	plt.xticks([])
	plt.yticks([])

	plt.grid()
	plt.tight_layout()
	plt.savefig("graphVisualization_noGroups/" + saveName + ".png")
	plt.show()

if __name__ == '__main__':
	fileNames = os.listdir("files/")

	for file in fileNames:
		print(file)
		f = open("files/" + file, 'r')
		points = []
		x = []
		y = []
		for row in f:
			try:
				x.append(float(row.strip().replace("\n", "").split(" ")[0]))
				y.append(float(row.strip().replace("\n", "").split(" ")[-1]))
				points.append((float(row.strip().replace("\n", "").split(" ")[0]), float(row.strip().replace("\n", "").split(" ")[-1])))
			except:
				continue
		f.close()

		visualizeDatasetWithoutGroups(x, y, file.replace(".txt", ""))