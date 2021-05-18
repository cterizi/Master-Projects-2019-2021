import numpy as np

def gradient(x0, x_i, y_i):
	s0 = 0
	s1 = 0
	s2 = 0
	s3 = 0
	s4 = 0

	for i in range(0, len(x_i)):
		s0 = s0 + (x0[0] + x0[1]*x_i[i] + x0[2]*(x_i[i]**2) + x0[3]*(x_i[i]**3) + x0[4]*(x_i[i]**4) - y_i[i])
		s1 = s1 + (x0[0] + x0[1]*x_i[i] + x0[2]*(x_i[i]**2) + x0[3]*(x_i[i]**3) + x0[4]*(x_i[i]**4) - y_i[i])*x_i[i]
		s2 = s2 + (x0[0] + x0[1]*x_i[i] + x0[2]*(x_i[i]**2) + x0[3]*(x_i[i]**3) + x0[4]*(x_i[i]**4) - y_i[i])*(x_i[i]**2)
		s3 = s3 + (x0[0] + x0[1]*x_i[i] + x0[2]*(x_i[i]**2) + x0[3]*(x_i[i]**3) + x0[4]*(x_i[i]**4) - y_i[i])*(x_i[i]**3)
		s4 = s4 + (x0[0] + x0[1]*x_i[i] + x0[2]*(x_i[i]**2) + x0[3]*(x_i[i]**3) + x0[4]*(x_i[i]**4) - y_i[i])*(x_i[i]**4)

	# Calculate final df_dai
	df_da0 = 2 * s0		
	df_da1 = 2 * s1
	df_da2 = 2 * s2
	df_da3 = 2 * s3
	df_da4 = 2 * s4
	
	gradient = np.asarray([df_da0, df_da1, df_da2, df_da3, df_da4])
	return(gradient)