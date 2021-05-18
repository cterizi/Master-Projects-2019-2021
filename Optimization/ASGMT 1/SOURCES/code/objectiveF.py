def objectiveF(point, x, y):
	sum_ = 0
	for i in range(0, len(x)):
		sum_ = sum_ + (point[0] + point[1]*x[i] + point[2]*(x[i]**2) + point[3]*(x[i]**3) + point[4]*(x[i]**4) - y[i])**2
	return(sum_)