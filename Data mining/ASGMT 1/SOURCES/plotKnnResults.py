import matplotlib.pyplot as plt
import matplotlib

if __name__=='__main__':
	x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	y = [0.5760000000000001, 0.5469999999999999, 0.5589999999999999,
	0.5509999999999999, 0.5599999999999999, 0.563, 0.575, 0.564,
	0.6020000000000001]

	fig, ax = plt.subplots()
	ax.plot(x, y, linewidth=2)
	ax.tick_params(axis='y', labelcolor = "black", labelsize = 20)
	ax.tick_params(axis='x', labelcolor = "black", labelsize = 20)
	ax.set_ylabel("accuracy", fontsize = 20)
	ax.set_xlabel("k number of neighbors", fontsize=20)	
	plt.xticks(x)
	plt.title("K-Nearest Neighbor", loc = 'center', fontsize = 20, color = 'orange')
	plt.grid()
	plt.tight_layout()
	plt.savefig("knn.png")
	plt.show()