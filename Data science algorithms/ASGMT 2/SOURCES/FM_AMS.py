import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import statistics
import operator
import random
import math
import sys
import csv

class FM:
	def __init__(self, filename, N):
		self.filename = filename
		self.N = N
		self.hashFunctions = [10, 50, 100, 150, 200, 250, 300]

	def fm_algorithm(self):
		with open(self.filename) as read_file:
			reader = csv.reader(read_file, delimiter=',')

			result = {}
			for hf in self.hashFunctions:
				approximateList = []

				for seed in range(0, hf):
					#if(seed % 50 == 0):
					#	print("Seed: " + str(seed))

					p = 2**64-355
					m = 2**63-1
					a = random.randint(1,p-1)
					b = random.randint(0,p-1)
					max_R = -1
					tmp_N = 0
					for row in reader:
						if(not(self.N == -1)):
							tmp_N = tmp_N + 1
							if(tmp_N > self.N):
								break
						
						aa_ = (bin(((a * int(row[0]) + b) % p) % m)[2:])
						if(len(aa_) <= 64):
							aa_ = '0'*(64-len(aa_)) + aa_
						else:
							">64 bits"
						if(aa_ == '0'*64):
							tmp_r = 0
						else:
							tmp_r = len(aa_)-len(aa_.rstrip('0'))
						if(tmp_r > max_R):
							max_R = tmp_r
					read_file.seek(0)
					approximateList.append(2**max_R)
					#print("SEED " + str(seed) + ", max R = " + str(max_R) + ", " + str(2**max_R))
			
				averageForMedian = []
				for elementsPerGroup in range(1, hf + 1):
					#numberOfGroups = math.ceil(float(len(approximateList)) / elementsPerGroup)
					startIndex = 0
					tmp_medianList = []
					while(True):
						'''
						1. Calculate median per group
						2. Calculate average of medians
						'''
						if(not(startIndex + elementsPerGroup >= len(approximateList))):
							tmp_medianList.append(statistics.median(approximateList[startIndex:startIndex + elementsPerGroup]))
						else:
							tmp_medianList.append(statistics.median(approximateList[startIndex:len(approximateList)]))
							break
						startIndex = startIndex + elementsPerGroup
						
					averageForMedian.append(math.ceil(sum(tmp_medianList) / len(tmp_medianList)))
				
				result[hf] = self.differenceBtwApproxGT(averageForMedian, hf)
				
			return(result)
		
	def differenceBtwApproxGT(self, approx, hf):
		if(self.N == -1):
			with open(self.filename) as read_file:
				reader = csv.reader(read_file, delimiter=',')

				distinctElements = []
				for row in reader:
					distinctElements.append(row[0])
				read_file.seek(0)
			distinctElements = len(set(distinctElements))
		else:
			with open(self.filename) as read_file:
				reader = csv.reader(read_file, delimiter=',')
				distinctElements = []
				tmp_N = 0
				for row in reader:
					tmp_N = tmp_N + 1
					if(tmp_N > self.N):
						break
					distinctElements.append(row[0])
				read_file.seek(0)
			distinctElements = len(set(distinctElements))

		best_a = hf + 1
		tmp_value = 10000000000000
		approx_ = -1
		for i in range(0, len(approx)):
			if(abs(distinctElements - approx[i]) < tmp_value):
				tmp_value = abs(distinctElements - approx[i])
				best_a = i + 1
				approx_ = approx[i]
		return([distinctElements, approx_, best_a])

	def generate_fm_plot(self, approx):
		numberOfDistinctElements_real = approx[list(approx.keys())[0]][0]
		
		x_values = sorted(list(approx.keys()))
		approx_Y = []
		for i in x_values:
			 approx_Y.append(approx[i][1])
		x_values_min = min(x_values)
		x_values_max = max(x_values)
		X = []
		for i in range(x_values_min, x_values_max + 1):
			X.append(i)
		
		gt_Y = [numberOfDistinctElements_real] * len(X)
		Y = []
		c = []
		min_Y = 10000000000000
		max_Y = -1
		n = []
		for i in range(x_values_min, x_values_max + 1):
			if(i in x_values):
				Y.append(approx[i][1])
				c.append('red')
				n.append(approx[i][-1])
				if(approx[i][1] > max_Y):
					max_Y = approx[i][1]
				if(approx[i][1] < min_Y):
					min_Y = approx[i][1]
			else:
				Y.append(0)
				c.append('white')
				n.append(0)
		if(numberOfDistinctElements_real > max_Y):
			max_Y = numberOfDistinctElements_real
		if(numberOfDistinctElements_real < min_Y):
			min_Y = numberOfDistinctElements_real

		'''Plot code'''
		fig, ax1 = plt.subplots()
		ax1.plot(X, gt_Y, 'green')
		ax1.scatter(X, Y, c=c)

		for i, txt in enumerate(n):
			if(txt > 0):
				ax1.annotate(txt, (X[i]+0.1, Y[i]+0.1))

		ax1.tick_params(axis='y', labelcolor = "black", labelsize=12)
		ax1.tick_params(axis='x', labelcolor = "black", labelsize=14)
		ax1.set_ylabel("number of distinct elements", fontsize=14)
		ax1.set_xlabel("number of hash functions", fontsize=14)
		plt.ylim([min_Y - 10000, max_Y + 10000])
		plt.xlim([min(x_values) - 10, max(x_values) + 10])
		
		gt = mpatches.Patch(color='green', label='real #distinct Tweet IDs')
		ap = mpatches.Patch(color='red', label='approximated #distinct Tweet IDs')
		leg = plt.legend(handles=[ap, gt], frameon = True, loc = 0, fontsize = "medium")
		
		plt.grid()
		plt.tight_layout()

		if('sample' in self.filename):
			if(self.N == -1):
				plt.savefig("sample_fm.png")
			else:
				plt.savefig("sample_fm_" + str(self.N) + ".png")
		else:
			if(self.N == -1):
				plt.savefig("fm.png")
			else:
				plt.savefig("fm_" + str(self.N) + ".png")
		plt.show()

class AMS:
	def __init__(self, filename, k, N):
		self.filename = filename
		self.k = k
		self.N = N
		if(self.N < 500):
			self.n = self.N
		else:
			self.n = 500
		self.numberOfVariables = self.n
		self.info = {}
		for i in range(0, self.numberOfVariables):
			self.info['X' + str(i+1)] = {'element':'', 'value':0, 'n':-1}
		self.positiions = []
		for i in range(0, self.n):
			self.positiions.append(i)
		self.randomPositions = self.positiions[0:self.numberOfVariables]

	def ams_algorithm(self):
		initialPosition = self.randomPositions[0]
		tmp_X_number = 1
		tmp_X_name = 'X' + str(tmp_X_number)

		with open(self.filename) as read_file:
			reader = csv.reader(read_file, delimiter=',')

			tmp_line = -1
			for row in reader:
				tmp_line = tmp_line + 1
				'''Mono edw yparxei to self.N'''
				if(tmp_line == self.N):
					break
				if(tmp_line < initialPosition):
					continue
				tmp_ss = 0
				for ii in self.info:
					if(self.info[ii]['element'] == ''):
						tmp_ss = tmp_ss + 1
				if(tmp_ss > 0):
				#if(tmp_line < self.n):
					if(tmp_line == initialPosition):
						self.info[tmp_X_name]['element'] = row[0]
						self.info[tmp_X_name]['value'] = self.info[tmp_X_name]['value'] + 1
						self.info[tmp_X_name]['n'] = tmp_line + 1
						tmp_X_number = tmp_X_number + 1
						tmp_X_name = 'X' + str(tmp_X_number)
					else:
						if(not(tmp_line in self.randomPositions[1:])):
							variableName = self.checkCurrentElements(row[0], self.info)
							if(not(variableName == 'None')):
								self.info[variableName]['value'] = self.info[variableName]['value'] + 1
								self.info[variableName]['n'] = tmp_line + 1
						else:
							variableName = self.checkCurrentElements(row[0], self.info)
							if(variableName == 'None'):
								'''New variable'''
								self.info[tmp_X_name]['element'] = row[0]
								self.info[tmp_X_name]['value'] = self.info[tmp_X_name]['value'] + 1
								self.info[tmp_X_name]['n'] = tmp_line + 1
								tmp_X_number = tmp_X_number + 1
								tmp_X_name = 'X' + str(tmp_X_number)
							else:
								self.info[variableName]['value'] = self.info[variableName]['value'] + 1	
								self.info[variableName]['n'] = tmp_line + 1
				else:
					'''Reservoir Sampling'''
					variableName = self.checkCurrentElements(row[0], self.info)
					if(not(variableName == 'None')):
						self.info[variableName]['value'] = self.info[variableName]['value'] + 1
						self.info[variableName]['n'] = tmp_line + 1
					else:
						threshold = len(self.info) / (tmp_line + 1)
						randomProbability = random.random()
						if(randomProbability <= threshold):
							'''Replace variable'''
							choosenVariableName = self.chooseVariableToDelete()
							self.info[choosenVariableName]['element'] = row[0]
							self.info[choosenVariableName]['value'] = 1
							self.info[choosenVariableName]['n'] = tmp_line + 1
			print(self.N, self.calculateReal(), self.calculateApprox())

	def calculateReal(self):
		with open(self.filename) as read_file:
			reader = csv.reader(read_file, delimiter=',')

			tmp_N = -1
			tmp_dt = {}
			for row in reader:
				tmp_N = tmp_N + 1
				if(tmp_N == self.N):
					break
				tmp_dt[row[0]] = int(row[-1])
			read_file.seek(0)
		tmp_sum = 0
		for i in tmp_dt:
			tmp_sum = tmp_sum + tmp_dt[i]**self.k
		return(tmp_sum)

	def calculateApprox(self):
		max_n = self.returnMaxN()
		self.updateInfoDictionary()
		total_approx = []
		for elementsPerGroup in range(1, len(self.info) + 1):
			numberOfGroups = math.ceil(len(self.info) / elementsPerGroup)
			medianList = []
			for group in range(0, numberOfGroups):
				tmp_medianList = []
				selectedArray = list(self.info.keys())[group * elementsPerGroup:group * elementsPerGroup + elementsPerGroup]
				for i in selectedArray:
					tmp_medianList.append(max_n * (self.info[i]['value']**self.k - (self.info[i]['value'] - 1)**self.k))
				medianList.append(statistics.median(tmp_medianList))
			total_approx.append(math.ceil(sum(medianList) / len(medianList)))
		'''
		total_approx[0] = 1 element per group
		total_approx[2] = 3 elements per group
		'''
		return(total_approx[2])

	def returnMaxN(self):
		max_n = -1
		for i in self.info:
			if(self.info[i]['n'] > max_n):
				max_n = self.info[i]['n']
		return(max_n)

	def updateInfoDictionary(self):
		variablesToDalete = []
		for i in self.info:
			if(self.info[i]['element'] == ''):
				variablesToDalete.append(i)
		for i in variablesToDalete:
			del self.info[i]

	def chooseVariableToDelete(self):
		l = sorted(list(self.info.keys()))
		for i in l:
			if(self.info[i]['element'] == ''):
				return(i)
		'''Choose one from self.numberOfVariables variables'''
		return(random.choice(l))

	def checkCurrentElements(self, element, dict):
		for x_variable, element_value in dict.items():
			if(element_value['element'] == element):
				return(x_variable)
		return('None')


if __name__ == "__main__":
	if(not(len(sys.argv) == 4)):
		print("====================================================================")
		print("====================================================================")
		print("Wrong input parameters!\nCommand format: python3 \"PYTHON FILE NAME.py\" \"CSV FILE NAME.csv\" k-parameter N-parameter")
		print("e.g. python3 GroundTruth.csv 0 1000")
		print("e.g. python3 originalTweetsPerTweet.csv 0 1000")
		print("e.g. python3 GroundTruth.csv 0 -1 (for all records)")
		print("e.g. python3 originalTweetsPerTweet.csv 0 -1 (for all records)")

		print("e.g. python3 originalTweetsPerTweet.csv 2 500")
		print("====================================================================")
		print("====================================================================")
		exit()

	if(int(sys.argv[2]) == 0):
		'''Flajolet-Martin'''
		if(int(sys.argv[3]) == -1 or int(sys.argv[3]) > 0):
			fmObject = FM(sys.argv[1], int(sys.argv[3]))
			approximations = fmObject.fm_algorithm()
			fmObject.generate_fm_plot(approximations)
		else:
			print("====================================================================")
			print("====================================================================")
			print("Wrong N-parameter!\nN = -1 (all records) or N∈ ℤ")
			print("====================================================================")
			print("====================================================================")
			exit()
	elif(int(sys.argv[2]) >= 2):
		'''Alon-Matias-Szegedy'''
		if(int(sys.argv[3]) > 0):
			amsObject = AMS(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
			amsObject.ams_algorithm()
		else:
			print("====================================================================")
			print("====================================================================")
			print("Wrong N-parameter!\nN∈ ℤ")
			print("====================================================================")
			print("====================================================================")
			exit()
	else:
		print("====================================================================")
		print("====================================================================")
		print("Wrong k-parameter!\nk∈ ℤ* - {1} < N")
		print("====================================================================")
		print("====================================================================")
		exit()
