from lineSearch import lineSearch
from objectiveF import objectiveF
from gradient import gradient
from hessian import *

from numpy import linalg as LA
import numpy as np

def newton(x_0, x, y, method, errorFile):
	if(method == 'newton'):
		a_max = 2
	elif(method == 'steepestDescent'):
		a_max = 1
	epsilon = 10**(-6)
	iterations = 0
	errorList = []

	# Check if Hessian matrix is positive defined.
	# If it is not positive defined then update Hessian 
	# matrix with a positive one
	hessian_ = hessian(x)
	if(not(checkHessianPositive(hessian_))):
            print("Hessian is not positive defined.")
            hessian_ = convertHessianIntoPositiveMatrix(hessian_, 1)
	inverse_hessian = np.linalg.inv(hessian_)

	errorFile.write("Initial error: " + str(objectiveF(x_0, x, y)) + "\n")
	errorList.append(objectiveF(x_0, x, y))
	print("Initial error: " + str(objectiveF(x_0, x, y)))


	while(LA.norm(gradient(x_0, x, y)) > epsilon):
		if(iterations == 1000):
			break

		# Select direction
		if(method == 'newton'):
			p = np.asarray((-1) * inverse_hessian.dot(gradient(x_0, x, y)))
		elif(method == 'steepestDescent'):
			p = np.asarray((-1) * gradient(x_0, x, y))

		# Select next optimal step
		a_star = lineSearch(x_0, p, a_max, x, y)

		# Update point x_0
		x_0 = x_0 + (a_star * p)

		iterations += 1

		# Update error file
		errorFile.write("Iteration " + str(iterations) + ": " + str(objectiveF(x_0, x, y)) + "\n")
		errorFile.flush()
		errorList.append(objectiveF(x_0, x, y))
		print("Error: " + str(objectiveF(x_0, x, y)))
	

	print("Optimizer: " + str(x_0))
	print("Total iteraions: " + str(iterations))
	print("||Gradient f (x_k)|| = " + str(LA.norm(gradient(x_0, x, y))))
	return(x_0, errorList)