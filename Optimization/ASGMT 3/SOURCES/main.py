'''
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
Libraries and modules
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
from geneticBinary import geneticBinary, in_U
from geneticReal import geneticReal
from pso import pso

from os import path
import numpy as np
import os.path
import decimal
import random
import sys
import ast
import os


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
Functions: 
(Initialize & Write) & Read coordinates of points
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
def readPoints(numberOfPoints, sizeOfPopulation, methodName, experimentID):
	points = []
	path = "points/" + methodName + "/" + str(sizeOfPopulation) + "/" + str(numberOfPoints) + "/" + str(experimentID) + ".txt"
	file = open(path, 'r')
	for line in file:
		coor = []
		for element in line.replace("\n", "").split("\t"):
			coor.append(ast.literal_eval(element))
		points.append(coor)
	file.close()
	return(np.asarray(points))


def pointsInitialization(sizeOfPopulation, numberOfpoints, typeOf, experimentID):
	path_ = "points/" + typeOf + "/" + str(sizeOfPopulation) + "/"
	if(not(path.exists(path_))):
		os.mkdir(path_)
	path_ = path_ + str(numberOfpoints) + "/"
	if(not(path.exists(path_))):
		os.mkdir(path_)
	path_ = path_ + str(experimentID) + ".txt"
	file = open(path_, "+w")

	if(typeOf == "real" or typeOf == "pso"):
		for sp in range(1, sizeOfPopulation + 1):
			coordinates = []
			for i in range(0, numberOfpoints):
				# Initialize 3 coordinates for each point
				coor = []
				for j in range(0, 3):
					coor.append(float(decimal.Decimal(random.randrange(-250, 251))/100)) # Random generate is a semi-open range
				if(i == numberOfpoints - 1):
					file.write(str(coor) + "\n")
				else:
					file.write(str(coor) + "\t")
	file.close()


def init_population(sizeOfPopulation, numberOfpoints):
    population = []
    for i in range(sizeOfPopulation):
        p = []
        for j in range(numberOfpoints):
            atom = []
            for k in range(3):
                while True:
                    b = []
                    for l in range(13):
                        a = random.randint(0, 1)
                        b.append(a)
                    if in_U(b):
                        break
                atom.extend(b)
            p.extend(atom)
        population.append(p)
    return population


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
Main code
python3 main.py method_name N_parameter
e.g. python3 main.py {binary, real, pso} {4, 5, 6, 7, 8, 9, 10, 15, 20}
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
if __name__ == '__main__':

	method = sys.argv[1]
	N = int(sys.argv[2])
	experiments = 30
	populationSize = 10

	solutionQuality = {4: -6.000000,
						5: -9.103852,
						6: -12.712062, 
						7: -16.505384, 
						8: -19.821489, 
						9: -24.113360, 
						10: -28.422532, 
						15: -52.322627, 
						20: -77.177043, 
						30: -128.286571, 
						40: -185.249839, 
						50: -244.549926}


	# Initialize and write coordinates of each point for defferent size of population and for 30 total experiments
	# for populationSize_ in populationSize:
	'''
	for exp in range(1, experiments + 1):
		if(method == "real" or method == "pso"):	
			pointsInitialization(populationSize, N, method, exp)
		elif(method == binary):
			init_population(populationSize, N)
	'''
	
	# Main loop for the 30 total experiments
	for exp in range(1, experiments + 1):
		print("experiment", exp, "method", method, "populationSize", populationSize)

		# Read coordinates
		points = readPoints(N, populationSize, method, exp)

		# Call function for each method
		if(method == "binary"):
			binaryPoints = [0]*len(points)
			for i in range(len(points)):
				binaryPoints[i] = list(points[i][0][:])
			geneticBinary(binaryPoints, solutionQuality[N], N, exp)
		elif(method == "real"):
			geneticReal(points, solutionQuality[N], exp)
		elif(method == "pso"):
			pso(points, solutionQuality[N], exp)

		# break
	