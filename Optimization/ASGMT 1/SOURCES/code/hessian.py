import numpy as np

def hessian(x_i):
	df_da0_a0 = 60
	df_da0_a1 = 2 * sum(x_i)
	df_da0_a2 = 2 * sum([x**2 for x in x_i])
	df_da0_a3 = 2 * sum([x**3 for x in x_i])
	df_da0_a4 = 2 * sum([x**4 for x in x_i])
	df_da1_a4 = 2 * sum([x**5 for x in x_i])
	df_da2_a4 = 2 * sum([x**6 for x in x_i])
	df_da3_a4 = 2 * sum([x**7 for x in x_i])
	df_da4_a4 = 2 * sum([x**8 for x in x_i])

	hessian = [[df_da0_a0, df_da0_a1, df_da0_a2, df_da0_a3, df_da0_a4],
			[df_da0_a1, df_da0_a2, df_da0_a3, df_da0_a4, df_da1_a4],
			[df_da0_a2, df_da0_a3, df_da0_a4, df_da1_a4, df_da2_a4],
			[df_da0_a3, df_da0_a4, df_da1_a4, df_da2_a4, df_da3_a4],
			[df_da0_a4, df_da1_a4, df_da2_a4, df_da3_a4, df_da4_a4]]
	hessian = np.array(hessian)
	return(hessian)


def checkHessianPositive(matrix):
	return(np.all(np.linalg.eigvals(matrix) > 0))


def convertHessianIntoPositiveMatrix(matrix, b_value):
	# Steps 1-5 (page. 138)
	diagonalElements = matrix.diagonal()
	minDiagonalElement = min(diagonalElements)
	if(minDiagonalElement <= 0):
		t = (-1 * minDiagonalElement) + b_value
	else:
		t = 0
	# Steps 6-13 (page. 138)
	while(True):
		new_matrix = matrix + t * np.eye(len(matrix), dtype = float)
		try:
			L = np.linalg.cholesky(new_matrix)
			return(new_matrix)
		except:
			t = max([b_value, 2 * t])