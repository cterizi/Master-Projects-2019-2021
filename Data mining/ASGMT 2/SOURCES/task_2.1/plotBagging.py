import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import matplotlib


def crossValidationColors(k):
	if(k == 5):
		return("yellow")
	elif(k == 10):
		return("pink")
	elif(k == 15):
		return("orange")
	elif(k == 20):
		return("red")
	elif(k == 25):
		return("olive")
	elif(k == 30):
		return("green")
	elif(k == 35):
		return("brown")
	elif(k == 40):
		return("grey")
	elif(k == 45):
		return("blue")
	elif(k == 50):
		return("black")

def plot(x, y, saveName):
	fig, ax = plt.subplots()

	for k in y:
		ax.plot(x, y[k], crossValidationColors(k), linewidth=3)

	ax.tick_params(axis='y', labelcolor = "black", labelsize = 20)
	ax.tick_params(axis='x', labelcolor = "black", labelsize = 20)
	ax.set_ylabel("accuracy", fontsize = 25)
	ax.set_xlabel("number of estimators", fontsize=25)

	ax.set_ylim(top=0.90)
	ax.set_ylim(bottom=0.74)
	cross5 = mpatches.Patch(color='yellow', label='5')
	cross10 = mpatches.Patch(color='pink', label='10')
	cross15 = mpatches.Patch(color='orange', label='15')
	cross20 = mpatches.Patch(color='red', label='20')
	cross25 = mpatches.Patch(color='olive', label='25')
	cross30 = mpatches.Patch(color='green', label='30')
	cross35 = mpatches.Patch(color='brown', label='35')
	cross40 = mpatches.Patch(color='grey', label='40')
	cross45 = mpatches.Patch(color='blue', label='45')
	cross50 = mpatches.Patch(color='black', label='50')
	leg = plt.legend(handles=[cross5, cross10, cross15, cross20, cross25, cross30, cross35, cross40, cross45, cross50], frameon = True, loc = 0, fontsize='xx-large', ncol=3)

	plt.yticks(np.arange(0.74, 0.85, 0.02))
	plt.xticks(x)

	plt.grid()
	plt.tight_layout()
	plt.savefig(saveName + "_plot_bagging.png")
	plt.show()

if __name__ == '__main__':
	#fileNames = ['nonnormalizedData_bagging.csv', 'normalizedData_bagging.csv']
	fileNames = ['normalizedData_bagging.csv']
	
	for file in fileNames:
		accuracyScores = {}
		f = open(file, 'r')
		for row in f:
			if("accuracy" in row):
				continue
			if (int(row.replace("\n", "").split("\t")[0]) in accuracyScores):
				accuracyScores[int(row.replace("\n", "").split("\t")[0])].append(float(row.replace("\n", "").split("\t")[2]))
			else:
				accuracyScores[int(row.replace("\n", "").split("\t")[0])] = [(float(row.replace("\n", "").split("\t")[2]))]
		f.close()

		plot([25, 50, 75, 100], accuracyScores, file.replace(".csv", ""))