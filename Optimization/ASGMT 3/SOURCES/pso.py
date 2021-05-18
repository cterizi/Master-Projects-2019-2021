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


def initializeVelocity(sizeOfPopulation, numberOfpoints, typeOf):
	points = []
	for sp in range(0, sizeOfPopulation):
		coordinates = []
		for i in range(0, numberOfpoints):
			# Initialize 3 coordinates for each point
			coor = []
			for j in range(0, 3):
				coor.append(float(decimal.Decimal(random.randrange(-250, 251))/100)) # Random generate is a semi-open range
			coordinates.append(coor)
		points.append(coordinates)
	return(np.asarray(points))


def selectBestNeighbor(a, b, c):
	bestEnergy = c[a[0]]
	bestC = b[a[0]]
	for i in a:
		if(c[i] < bestEnergy):
			bestEnergy = c[i]
			bestC = b[i]
	return(bestC)


def updateVelocities(velocitiesPrevious, coordinates, bestPositionCluster, neighbors, energy_, X, C1, C2):
	newVelocities = []
	v_max = 0.1 * 5

	for i in range(0, len(velocitiesPrevious)):
		vel = []
		for j in range(0, len(velocitiesPrevious[i])):
			coor = []
			bestNeig = selectBestNeighbor(neighbors[i], coordinates, energy_)
			for k in range(0, 3):
				p_ij = bestPositionCluster[i][0][j][k]
				p_gi = bestNeig[j][k]
				
				v_ij = X * (velocitiesPrevious[i][j][k] + float(decimal.Decimal(random.randrange(0, 101))/100) * C1 * (p_ij - coordinates[i][j][k]) + 
					float(decimal.Decimal(random.randrange(0, 101))/100) * C2 * (p_gi - coordinates[i][j][k]) )

				if(v_ij > v_max):
					v_ij = v_max
				elif(v_ij < -v_max):
					v_ij = -v_max

				coor.append(v_ij)
			
			vel.append(coor)
		newVelocities.append(vel)
	newVelocities = np.asarray(newVelocities)
	return(newVelocities)


def updatePoints(coordinates, velocities_):
	coordinates_ = []
	for i in range(0, len(coordinates)):
		coord_ = []
		for j in range(0, len(coordinates[i])):
			c_ = []
			for k in range(0, 3):
				# coordinates[i][j][k] = coordinates[i][j][k] + velocities_[i][j][k]
				tmp = coordinates[i][j][k] + velocities_[i][j][k]

				# if(coordinates[i][j][k] > 2.5):
				if(tmp > 2.5):
					tmp = 2.5
				elif(tmp < -2.5):
					tmp = -2.5
				c_.append(tmp)
			coord_.append(c_)
		coordinates_.append(coord_)
	coordinates_ = np.asarray(coordinates_)
	return(coordinates_)


def initializeNeighbors(coordinates, topology):
	neig = {}
	if(topology == 'lbest'):
		p = 1
		for i in range(0, len(coordinates)):
			if(i == 0):
				neig[i] = [len(coordinates) - 1, i, i + 1]
			elif(i == len(coordinates) - 1):
				neig[i] = [i - 1, i, 0]
			else:
				neig[i] = [i - 1, i, i + 1]
	elif(topology == "gbest"):
		for i in range(0, len(coordinates)):
			neig[i] = [j for j in range(0, len(coordinates))]
	return(neig)


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
def pso(points, solutionQuality, experimentID):
	T_max = len(points[0]) * (10**5)
	totalCases = 10
	T_max = int(T_max / totalCases)
	# print("T_max", T_max)

	restart = int(0.10 * T_max) # Restart after 10% of total iterations without improvement 
	restart_iterations = 0
	numberOfRestarts = 0

	iter_ = 0
	bestIteration = -1

	X = 0.729
	C1 = 2.05
	C2 = 2.05

	upper = 2.5
	lower = -2.5

	# topology = "gbest"
	topology = "lbest"

	velocities = initializeVelocity(len(points), len(points[0]), "real")
	energy = evaluateEnergy(points)

	# Best point (coordinates, energy)
	x_best = updateBest(points, energy)
	x_best_clusters = {}
	for i in range(0, len(points)):
		x_best_clusters[i] = [points[i], energy[i]]
	
	neighbors = initializeNeighbors(points, topology)


	# Main loop
	while(iter_ < T_max):
		# Update parameter for total iterations
		iter_ += 1
		# if(iter_ % 1000 == 0):
			# print("iter_", iter_)

		
		# Update velocities
		velocities = updateVelocities(velocities, points, x_best_clusters, neighbors, energy, X, C1, C2)

		# Update population
		points = updatePoints(points, velocities)

		# Calculate energies
		energyNew = evaluateEnergy(points)
		
		# Update best positions for each cluster
		for i in range(0, len(points)):
			if(energyNew[i] < energy[i]):
				x_best_clusters[i] = [points[i], energyNew[i]]
		energy = energyNew

		x_best_new = updateBest(points, energy)
		# print(x_best_new[1])
		if(solutionQuality == x_best_new[1]): #or abs(x_best_new[1] - solutionQuality)<10**(-3)):
			break
		if(x_best_new[1] >= x_best[1]):
			# Check for restart
			restart_iterations += 1
			if(restart_iterations == restart):
				points = restartNewCoordinates(len(points), len(points[0]), 'real')
				restart_iterations = 0
				numberOfRestarts += 1
		else:
			restart_iterations = 0
			bestIteration = iter_
		x_best = x_best_new
	
	path = "results/pso/" + str(len(points[0])) + "/" + topology + ".txt"
	file = open(path, "a")
	file.write("Experiment\t" + str(experimentID) + "\t" + str(x_best[1]) + "\t" + str(abs(x_best[1] - solutionQuality)) + "\t" + str(bestIteration) + "\t" + str(numberOfRestarts) + "\t" + str(x_best[0]) + "\n")
	file.close()
