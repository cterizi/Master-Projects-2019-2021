from trustRegion import trustRegion
from gradient import gradient
from newton import newton
from hessian import *
from bfgs import bfgs
from load import load


import matplotlib.pyplot as plt
from numpy import linalg as LA
import time
import sys


def functionP(a, x_values):
	pred = []
	for x in x_values:
		pred.append((a[0] + a[1]*x + a[2]*(x**2) + a[3]*(x**3) + a[4]*(x**4)) * 10000)
	return(pred)


if __name__ == '__main__':
	# Read covid-19 data from file and initial points
	[days, cases, days_divided, cases_divided, points] = load("covid_data_30_GR.dat", "initial_points.dat")


	# python3 main.py (1 2 3 4 5) (newton/trustRegion/bfgs/steepestDescent)
	mapMethods = {'newton':1, 'trustRegion':2, 'bfgs':3, 'steepestDescent':4}
	inputs = sys.argv
	selected_point = np.array(points[int(inputs[1]) - 1])
	print("Selected initial point: " + str(selected_point))
	selected_method = mapMethods[inputs[2]]
	

	error_file = open('error' + inputs[1] + "_" + inputs[2] + ".txt", 'a')

	# Main scheme
	start_time = time.time()

	if(selected_method == 1):
		# Newton Line Search
		[optimizer, error] = newton(selected_point, days_divided, cases_divided, 'newton', error_file)
	elif(selected_method == 4):
		# Steepest Descent
		[optimizer, error] = newton(selected_point, days_divided, cases_divided, 'steepestDescent', error_file)
	elif(selected_method == 3):
		# BFGS
		[optimizer, error] = bfgs(selected_point, days_divided, cases_divided, error_file)
	elif(selected_method == 2):
		# Newton Trust Region
		[optimizer, error] = trustRegion(selected_point, days_divided, cases_divided, error_file)

	error_file.close()

	end_time = time.time()
	print("Run time: " + str(end_time - start_time) + " seconds")

	# Calculate total COVID-19 cases
	days_divided = list(days_divided) + [(i/10) for i in [31, 32, 33, 34, 35]]
	pred = functionP(optimizer, days_divided)
	cases = list(cases) + [66637, 69675, 72510, 74205, 76403]
	days = list(days) + [31, 32, 33, 34, 35]

	# Plot Optimal solution
	mapMathodTitle = {'newton':"Newton Ευθύγραμμης Αναζήτησης", 'bfgs':"BFGS Ευθύγραμμης Αναζήτησης", 'trustRegion':"Newton Ασφαλούς Περιοχής",
					'steepestDescent':"Steepest Descent Ευθύγραμμης Αναζήτησης"}
	fig, ax = plt.subplots()
	actual = ax.scatter(days, cases, c='r', marker='*', label='Actual data')
	prediction = ax.plot(days, pred, c='b', label='Prediction data')

	plt.title(mapMathodTitle[inputs[2]], loc='center', fontsize=12, fontweight=0, color='orange')
	plt.ylabel("Covid19 Cases", fontsize=20)
	plt.xlabel("Days", fontsize=20)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=13)

	plt.legend(prop={'size': 15})
	plt.grid(b = True)
	plt.tight_layout()
	plt.savefig("cases_" + inputs[1] + ".png")
	plt.show()

	# Plot objective function values
	fig, ax = plt.subplots()
	x = [i for i in range(1, len(error) + 1)]
	ax.plot(x, error)
	plt.ylabel("Error", fontsize=20)
	plt.xlabel("Iterations", fontsize=20)
	plt.xticks(fontsize=13)
	plt.yticks(fontsize=13)
	if(not(len(error) > 50)):
		plt.xticks(x, rotation=30)
	plt.grid(b = True)
	plt.tight_layout()
	plt.savefig("error_" + inputs[1] + ".png")
	plt.show()
	