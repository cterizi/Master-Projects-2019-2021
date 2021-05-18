from objectiveF import objectiveF
from gradient import gradient

def zoom(x_0, a_l, a_h, p, x, y):
	c_1 = 10**(-4)
	c_2 = 0.9

	while(True):
		step_j = (a_l + a_h) / 2
		x_new = x_0 + (step_j * p)

		# Calculate first part of Armijo condition, φ(x_new)
		armijo_condintion_a = objectiveF(x_new, x, y)

		# Calculate second part of first Armijo condition, φ(x_0) + c1 * a_j * φ'(x_0)
		armijo_condintion_b = objectiveF(x_0, x, y) + c_1 * step_j * gradient(x_0, x, y).dot(p)

		# Calculate second part of Armijo condition, φ(a_j) >= φ(a_l)
		armijo_condintion_c = objectiveF(x_0 + (a_l * p), x, y)

		# Check Armijo condition
		if((armijo_condintion_a > armijo_condintion_b) or (armijo_condintion_a >= armijo_condintion_c)):
			a_h = step_j
		else:
			# Check the condition of curvature, |φ'(a_j)| > - c2 * |φ'(0)|
			curvature_condition = gradient(x_new, x, y).dot(p)
			if(abs(curvature_condition) > (-1) * c_2 * abs(gradient(x_0, x, y).dot(p))): 
				# Wolfe conditions are valid. Return the step j
				return(step_j)

			if(curvature_condition * (a_h - a_l) >= 0):
				a_h = a_l

			a_l = step_j