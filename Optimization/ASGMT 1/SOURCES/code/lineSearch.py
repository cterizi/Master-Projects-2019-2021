from objectiveF import objectiveF
from gradient import gradient
from hessian import *
from zoom import zoom
import random


def lineSearch(x_0, p, a_max, x, y):
	step = 0
	selected_step = float(a_max / 2)
	iterations = 1

	c_1 = 10**(-4)
	c_2 = 0.9

	while(True):
		# Calculate new coordinations for x_0, that is, x_0 + selected_step * p
		x_new = x_0 + (selected_step * p)

		# Calculate first part of Armijo condition, φ(x_new)
		armijo_condintion_a = objectiveF(x_new, x, y)

		# Calculate second part of first Armijo condition, φ(x_0) + c1 * a_j * φ'(x_0)
		armijo_condintion_b = objectiveF(x_0, x, y) + c_1 * selected_step * gradient(x_0, x, y).dot(p)

		# Calculate second part of Armijo condition, φ(a_j) >= φ(a_i)
		armijo_condintion_c = objectiveF(x_0 + (step * p), x, y)

		# Check Armijo conditions
		if((armijo_condintion_a > armijo_condintion_b) or ((iterations > 1) and (armijo_condintion_a >= armijo_condintion_c))):
			# Armijo condiiton is not valid. Select new step value.
			return(zoom(x_0, step, selected_step, p, x, y))


		# Check the condition of curvature, |φ'(a_i)| > - c2 * |φ'(0)|
		curvature_condition = gradient(x_new, x, y).dot(p)
		if(abs(curvature_condition) > (-1) * c_2 * abs(gradient(x_0, x, y).dot(p))):
			# Wolfe conditions are valid. Return the selected step
			return(selected_step)

		# The condition of curvature is not valid
		if(curvature_condition >= 0):
			return(zoom(x_0, selected_step, step, p, x, y))

		# Update variables
		step = selected_step

		while(True):
			selected_step = random.uniform(step, a_max)
			if(not(selected_step == step or selected_step == a_max)):
				break
		iterations = iterations + 1
