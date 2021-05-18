from objectiveF import objectiveF
from gradient import gradient
from hessian import *


from scipy.optimize import fsolve
from numpy import linalg as LA
import numpy as np


def get_direction(radius, hessian_, x_0, x, y):
	inverse_hessian = np.linalg.inv(hessian_)

	# Newton point
	p_B = (-1) * inverse_hessian.dot(gradient(x_0, x, y))

	if(LA.norm(p_B) <= radius):
		p_star = p_B
		type_ = 'Newton'
	else:
		# Cauchy point
		g = gradient(x_0, x, y)
		p_U = (-1) * (np.inner(g, g) / (g.dot(hessian_)).dot(g)) * g

		if(LA.norm(p_U) >= radius):
			p_star = (-1) * (radius / LA.norm(g)) * g
			type_ = 'Cauchy'
		else:
			f = lambda t: (LA.norm(p_U + (t - 1) * (p_B - p_U))**2) - radius**2
			t_star = fsolve(f, 2)[0]
			p_star = p_U + (t_star - 1) * (p_B - p_U)
			type_ = 'Dogleg'
	return(p_star, type_)	


def trustRegion(x_0, x, y, errorFile):
	epsilon = 10**(-6)
	iterations = 0
	max_radius = 1
	eta = 0.2
	D_0 = float(max_radius / 2)
	errorList = []

	# Counters for selected points in Newton trust region method
	pointCounter = {'newton':0, 'cauchy':0, 'dogleg':0}
	radiusSelections = {'shrink':0, 'increase':0}

	# Check if Hessian matrix is positive defined.
	# If it is not positive defined then update Hessian 
	# matrix with a positive one
	hessian_ = hessian(x)
	if(not(checkHessianPositive(hessian_))):
		print("Hessian is not positive defined.")
		hessian_ = convertHessianIntoPositiveMatrix(hessian_, 1)

	errorFile.write("Initial error: " + str(objectiveF(x_0, x, y)) + "\n")
	errorList.append(objectiveF(x_0, x, y))
	print("Initial error: " + str(objectiveF(x_0, x, y)))


	while(LA.norm(gradient(x_0, x, y)) > epsilon):
		if(iterations == 1000):
			break

		# Select direction and return type of selected point
		[p, pointType] = get_direction(D_0, hessian_, x_0, x, y)
		
		if(pointType =='Newton'):
			pointCounter['newton'] = pointCounter['newton'] + 1
		elif(pointType == 'Cauchy'):
			pointCounter['cauchy'] = pointCounter['cauchy'] + 1
		elif(pointType == 'Dogleg'):
			pointCounter['dogleg'] = pointCounter['dogleg'] + 1

		m = objectiveF(x_0, x, y) + (gradient(x_0, x, y).dot(p)) + (1/2) * (p.dot(hessian_)).dot(p)
		r = (objectiveF(x_0, x, y) - objectiveF(x_0 + p, x, y)) / (objectiveF(x_0, x, y) - m)

		if(r < 0.25):
			D_0 = 0.25 * D_0
			radiusSelections['shrink'] = radiusSelections['shrink'] + 1
		elif(r > 0.75 and LA.norm(p) == D_0):
			D_0 = min(2*D_0, max_radius)
			radiusSelections['increase'] = radiusSelections['increase'] + 1

		if(r > eta):
			x_0 = x_0 + p

		iterations = iterations + 1

		# Update error file
		errorFile.write("Iteration " + str(iterations) + ": " + str(objectiveF(x_0, x, y)) + "\n")
		errorFile.flush()
		errorList.append(objectiveF(x_0, x, y))
		print("Error: " + str(objectiveF(x_0, x, y)))


	print("Optimizer: " + str(x_0))
	print("Total iteraions: " + str(iterations))
	print("||Gradient f (x_k)|| = " + str(LA.norm(gradient(x_0, x, y))))
	print(pointCounter)
	return(x_0, errorList)