'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Import libraries
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
from numpy import linalg as LA
import numpy as np
import math


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
Main function
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
def PNN_(sigma, trainData_class_1, trainData_class_2, testData, number_of_features, number_of_classes):
	sumOfGaussians = {}
	sigma = sigma
	classes = []

	dataInGroup = {1:np.asarray(trainData_class_1), 
					2:np.asarray(trainData_class_2)}

	for point_want_to_classify in testData:
		# INPUT LAYER of PNN
		for k in range(1, number_of_classes + 1):
			# PATTERN LAYER of PNN
			product = 0

			for trainElement in dataInGroup[k]:
				norm = (LA.norm([(point_want_to_classify[i] - trainElement[i]) for i in range(0, len(point_want_to_classify))]))**2
				exp = math.exp((-1 * (norm)) / (2 * (sigma**2)))
				gaussian = (1 / ((2 * math.pi * (sigma**2))**(number_of_features/2))) * exp
				product = product + gaussian
			
			# SUMMATION LAYER of PNN
			sumOfGaussians[k] = (1/number_of_classes) * product
		
		# OUTPUT LAYER of PNN
		classified_class = str(max(sumOfGaussians, key = sumOfGaussians.get))
		classes.append(int(classified_class))
	return(classes)