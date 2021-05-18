import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import sys

def generate_plot(x, real, approx):
	fig, ax1 = plt.subplots()
	ax1.plot(x, real, 'green')
	ax1.plot(x, approx, 'red')

	ax1.tick_params(axis='y', labelcolor = "black", labelsize=12)
	ax1.tick_params(axis='x', labelcolor = "black", labelsize=12, rotation = 20)
	ax1.set_ylabel("surprise number", fontsize=14)
	ax1.set_xlabel("N", fontsize=14)

	real_mp = mpatches.Patch(color='green', label='real value')
	appr_mp = mpatches.Patch(color='red', label='approximate value')
	leg = plt.legend(handles=[real_mp, appr_mp], frameon = True, loc = 0, fontsize = "x-large")

	plt.grid()
	plt.tight_layout()

	plt.savefig("ams_" + sys.argv[1].replace(".txt", "") + ".png")

	plt.show()

if __name__ == "__main__":
	filename = open(sys.argv[1], 'r')

	N = []
	R = []
	A = []
	for line in filename:
		tmp_line = line.replace("\n", "").split(" ")
		N.append(int(tmp_line[0]))
		R.append(int(tmp_line[1]))
		A.append(int(tmp_line[2]))
	
	generate_plot(N, R, A)

	filename.close()
