'''
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
Libraries and modules
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
import numpy as np
import decimal
import random


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
Functions
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
def evaluateEnergy(data):
	energyL = []
	for coords in data:
		sum_ = 0
		for element_index_i in range(0, len(coords)-1):
			for element_index_j in range(element_index_i + 1, len(coords)):
				r_ij = np.linalg.norm(coords[element_index_i] - coords[element_index_j])
				v_ij = (1/r_ij)**12 - (1/r_ij)**6
				sum_ = sum_ + v_ij
		E_LJ = 4 * sum_
		energyL.append(E_LJ)
	return(np.asarray(energyL))


def updateBest(dataOfPoints, dataOfEnergy):
	minimumEnergy = min(dataOfEnergy)
	minimumIndex = np.where(dataOfEnergy == minimumEnergy)
	return((dataOfPoints[minimumIndex], minimumEnergy))
	

def selection(data, typeOfSelection):
	selectedPointsIndex = []
	selectedPoints = []

	if(typeOfSelection == 'rouletteCompareWorst'):
		energyOfPopulation = evaluateEnergy(data)
		energy_worst = max(energyOfPopulation)
		
		# Calculate fitness
		fitness_tmp = []
		for energy_tmp in energyOfPopulation:
			fitness_tmp.append(abs(energy_worst - energy_tmp))
		fitness_cap = sum(fitness_tmp)

		# Set probabilities
		ps = []
		for energy_tmp in energyOfPopulation:
			ps.append(abs(energy_worst - energy_tmp) / fitness_cap)
		
		probabilitiesInterval = [ps[0]]
		for i in range(1, len(ps)):
			probabilitiesInterval.append(probabilitiesInterval[-1] + ps[i])
		probabilitiesInterval[-1] = 1

		# Select points
		Ns = len(data) # Or 2 * len(data)
		randomNumbers = np.random.uniform(low = 0.0, high = 1.0, size = Ns)
		for rn in randomNumbers:
			for pi in range(0, len(probabilitiesInterval)):
				if(rn <= probabilitiesInterval[pi]):
					selectedPointsIndex.append(pi)
					selectedPoints.append(data[pi])
					break

	elif(typeOfSelection == 'rouletteLinearFitness'):
		# Sort elements based on energy
		energyOfPopulation = evaluateEnergy(data)
		energyOfPopulationDictionary = {}
		for i in range(0, len(energyOfPopulation)):
			energyOfPopulationDictionary[i] = energyOfPopulation[i]
		
		energyOfPopulationDictionary_sorted = sorted(energyOfPopulationDictionary.items(), key=lambda item: item[1])[::-1]
		energyOfPopulationDictionary_sorted_final = {}
		for i in range(0, len(energyOfPopulationDictionary_sorted)):
			energyOfPopulationDictionary_sorted_final[energyOfPopulationDictionary_sorted[i][0]] = i

		# Calculate fitness
		fitness_tmp = []
		for i in range(0, len(energyOfPopulation)):
			# 2 - s + 2(s - 1)(P_i - 1 / N - 1), s = 2
			fitness_tmp.append(2 * ( (energyOfPopulationDictionary_sorted_final[i] + 1 - 1) / (len(data) - 1) )) 
		fitness_cap = sum(fitness_tmp)	

		# Set probabilities
		ps = []
		for ps_tmp in fitness_tmp:
			ps.append(ps_tmp / fitness_cap)
		
		probabilitiesInterval = [ps[0]]
		for i in range(1, len(ps)):
			probabilitiesInterval.append(probabilitiesInterval[-1] + ps[i])
		probabilitiesInterval[-1] = 1
		
		# Select points
		Ns = len(data) # Or 2 * len(data)
		randomNumbers = np.random.uniform(low = 0.0, high = 1.0, size = Ns)
		for rn in randomNumbers:
			for pi in range(0, len(probabilitiesInterval)):
				if(rn <= probabilitiesInterval[pi]):
					selectedPointsIndex.append(pi)
					selectedPoints.append(data[pi])
					break

	elif(typeOfSelection == 'tournament'):
		N_tour = int(len(data)/2)
		Ns = len(data) # Or 2 * len(data)
		energyOfPopulationAll = evaluateEnergy(data)

		for i in range(0, Ns):
			# Select N_tour random elements from N points without replacement 
			randomNTourElements = data[np.random.choice(len(data), size = N_tour, replace=False)]
			energyOfPopulation = evaluateEnergy(randomNTourElements)

			# Select the best point from these N_tour selected points
			minimumEnergy = min(energyOfPopulation)
			minimumIndex = np.where(energyOfPopulation == minimumEnergy)

			selectedPointsIndex.append(np.where(energyOfPopulationAll == minimumEnergy)[0][0])
			selectedPoints.append(randomNTourElements[minimumIndex][0])

	return(selectedPoints)


def crossover(data, typeOfCrossover, delta):
	# Generate pairs of parents
	pairs = []
	if(typeOfCrossover == 'random'):
		indexes = [i for i in range(0, len(data))]
		while(len(indexes) > 0):
			p1 = random.choice(indexes)
			indexes.remove(p1)
			p2 = random.choice(indexes)
			indexes.remove(p2)
			pairs.append([data[p1], data[p2]])
	elif(typeOfCrossover == "order"):
		i_start = 0
		i_end = len(data) - 1
		while(i_start < i_end):
			pairs.append([data[i_start], data[i_start + 1]])
			i_start = i_start + 2
	
	# Generate child from parents
	childs = []
	for elements in pairs:
		child = []
		for coord in range(0, len(elements[0])):
			new_child = []
			for index in range(0, 3):
				r = np.random.uniform((-1)*delta, 1 + delta)
				o = r * elements[0][coord][index] + (1 - r) * elements[1][coord][index]

				# Keep new coordinates into the range [-2.5, 2.5]
				if(o > 2.5):
					o = 2.5
				elif(o < -2.5):
					o = -2.5

				new_child.append(o)
			child.append(new_child)
		childs.append(child)
		# break
	childs = np.asarray(childs)
	return(childs)


def mutation(data, typeOfMutation, sigma_alpha):
	for element in range(0, len(data)):
		for coord in range(0, len(data[element])):
			for index  in range(0, 3):
				if(typeOfMutation == "normal"):
					o = data[element][coord][index] + np.random.normal(0, sigma_alpha)
				elif(typeOfMutation == "uniform"):
					o = data[element][coord][index] + np.random.uniform((-1)*sigma_alpha, sigma_alpha)

				# Keep new coordinates into the range [-2.5, 2.5]
				if(o > 2.5):
					o = 2.5
				elif(o < -2.5):
					o = -2.5

				data[element][coord][index] = o
	return(data)


def updatePopulations(a, b):
	p = []
	for i in a:
		p.append(i)
	for i in b:
		p.append(i)
	p = np.asarray(p)
	return(p)


def updateNewPopulation(previous, new, typeOfNewPopulation):
	if(typeOfNewPopulation == "replace"):
		return(new)
	elif(typeOfNewPopulation == "merge"):
		N = len(previous)
		allTogether = updatePopulations(previous, new)
		energy_allTogether = evaluateEnergy(allTogether)
		Z = [x for _,x in sorted(zip(energy_allTogether, allTogether))]
		return(np.asarray(Z[0:N]))


def restartNewCoordinates(sizeOfPopulation, numberOfpoints, typeOf):
	points = []
	for sp in range(0, sizeOfPopulation):
		coordinates = []
		for i in range(0, numberOfpoints):
			# Initialize 3 coordinates for each point
			coor = []
			for j in range(0, 3):
				if(typeOf == "binary"):
					coor.append(random.choice([0, 1]))
				elif(typeOf == "real"):
					coor.append(float(decimal.Decimal(random.randrange(-250, 251))/100)) # Random generate is a semi-open range
			coordinates.append(coor)
		points.append(coordinates)
	return(np.asarray(points))


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
Main code
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
def geneticReal(points, solutionQuality, experimentID):
	T_max = len(points[0]) * (10**5)
	totalCases = 10
	T_max = int(T_max / totalCases)
	# print("T_max", T_max)

	restart = int(0.10 * T_max) # Restart after 10% of total iterations without improvement 
	restart_iterations = 0
	numberOfRestarts = 0

	iter_ = 0
	bestIteration = -1

	selectionMethod = 'rouletteCompareWorst'
	# selectionMethod = 'rouletteLinearFitness'
	# selectionMethod = 'tournament'

	# crossoverMethod = 'random'
	crossoverMethod = 'order'

	crossoverProbability = 0.5

	delta = 0.50

	# mutationMethod = 'normal'
	# sigma_alpha = 0.50

	mutationMethod = 'uniform'
	sigma_alpha = 0.50

	# newPopulationMethod = "replace"
	newPopulationMethod = "merge"


	# Evaluate initial population of points
	energy = evaluateEnergy(points)
	
	# Best point (coordinates, energy)
	x_best = updateBest(points, energy)


	# Main loop
	while(iter_ < T_max):
		# Update parameter for total iterations
		iter_ += 1
		# if(iter_ % 100 == 0):
			# print("iter_", iter_)

		# Selection process
		selectedPopulation = selection(points, selectionMethod)

		'''
			Check number of final selected points.
			If it is an odd number then add a random member from selectedPopulation.
			Pairs are created either random or based on the order that appeared.
		'''
		finalselectedPoints = []
		notSelectedPoints = []
		for el in selectedPopulation:
			prob = np.random.uniform(0, 1)
			if(prob <= crossoverProbability):
				finalselectedPoints.append(el)
			else:
				notSelectedPoints.append(el)
		finalselectedPoints = finalselectedPoints
		if(not(len(finalselectedPoints) % 2 == 0)):
			selectRandomElementIndex = random.choice([ind for ind in range(0, len(finalselectedPoints))])
			finalselectedPoints.append(finalselectedPoints[selectRandomElementIndex])
		finalselectedPoints = np.asarray(finalselectedPoints)

		# Crossover process
		crossoverPopulation = crossover(finalselectedPoints, crossoverMethod, delta)
		C_population = updatePopulations(notSelectedPoints, crossoverPopulation)

		# Mutation process
		mutationPopulation = mutation(C_population, mutationMethod, sigma_alpha)

		# New population
		points = updateNewPopulation(points, mutationPopulation, newPopulationMethod)

		# Update best point (coordinates, energy)
		x_best_newPopulation = updateBest(points, evaluateEnergy(points))
		if(x_best_newPopulation[1] < x_best[1]):
			x_best = x_best_newPopulation
			restart_iterations = 0
			bestIteration = iter_
		else:
			# Check for restart
			restart_iterations += 1
			if(restart_iterations == restart):
				points = restartNewCoordinates(len(points), len(points[0]), 'real')
				restart_iterations = 0
				numberOfRestarts += 1

	path = "results/real/" + str(len(points[0])) + "/" + selectionMethod + "_N_" + crossoverMethod + "_" + str(delta) + "_" + mutationMethod + "_" + str(sigma_alpha) + "_" + newPopulationMethod + ".txt"	
	file = open(path, "a")
	file.write("Experiment\t" + str(experimentID) + "\t" + str(x_best[1]) + "\t" + str(abs(x_best[1] - solutionQuality)) + "\t" + str(bestIteration) + "\t" + str(numberOfRestarts) + "\t" + str(x_best[0]) + "\n")
	file.close()