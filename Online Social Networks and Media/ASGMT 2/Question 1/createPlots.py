import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import operator

def createPlot(x, y, xLabel, yLabel, saveName):
	fig, ax1 = plt.subplots()
	ax1.tick_params(axis='y', labelcolor = "black", labelsize=14)
	ax1.tick_params(axis='x', labelcolor = "black", labelsize=14)
	ax1.set_ylabel(yLabel, fontsize=14)
	ax1.set_xlabel(xLabel, fontsize=14)

	plt.scatter(x, y, s = 10, alpha = 0.6, s = 0.4)
	plt.grid()
	plt.tight_layout()

	plt.savefig(saveName + ".png")
	plt.show()


def returnData(fileName, tp):
	file = open(fileName, 'r')
	d = {}
	for line in file:
		tmp_line = line.replace("\n", "").split("\t")
		cluster_id = int(tmp_line[0])
		if("size" in tp):
			value = int(tmp_line[1])
		else:
			value = float(tmp_line[1])
		d[cluster_id] = value
	file.close()
	return(d)

def sortXYaxisValues(a, b):
	sorted_x = sorted(a.items(), key=operator.itemgetter(1))
	sorted_x.reverse()
	x_axis = []
	y_axis_size = []
	y_axis_modularity = []
	for i in sorted_x:
		x_axis.append(i[0])
		y_axis_size.append(i[1])
		y_axis_modularity.append(b[i[0]])
	return(x_axis, y_axis_size, y_axis_modularity)

def main():
	sizeData = returnData("clusterSize.txt", "size")
	modularityData = returnData("clusterModularity.txt", "modularity")

	[x_axis, y_axis_size, y_axis_modularity] = sortXYaxisValues(sizeData, modularityData)
	createPlot(x_axis, y_axis_size, "community ID", "community size", "clusterSize")
	createPlot(x_axis, y_axis_modularity, "community ID", "community modularity", "clusterModularity")

main()