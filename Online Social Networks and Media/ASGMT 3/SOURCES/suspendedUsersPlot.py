import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

if __name__=='__main__':
	hot_list = [0.24271844660194175, 0.45045045045045046, 0.6734006734006734]
	top_list = [3.4183673469387754, 3.185004571776897, 1.439697899457163]
	controversial_list = [4.705882352941177, 9.789702683103698, 48.35164835164835]

	x_labels = ['politics', 'worldnews', 'sports']

	fig, ax = plt.subplots()
	x = np.arange(len(x_labels))
	width = 0.40

	rects1 = ax.bar(x - width/2, hot_list, width/2, label='hot', color='orange', align='center')
	rects2 = ax.bar(x, top_list, width/2, label='top', color='red', align='center')
	rects3 = ax.bar(x + width/2, controversial_list, width/2, label='controversial', color='blue', align='center')

	ax.tick_params(axis='y', labelcolor = "black", labelsize=20)
	ax.tick_params(axis='x', labelcolor = "black", labelsize=20)
	ax.set_ylabel("percent of suspended users", fontsize=20)
	ax.set_xticks(range(3))
	ax.set_xticklabels(x_labels)
	ax.set_ylim(top=50)

	hot_mp = mpatches.Patch(color='orange', label='hot')
	top_mp = mpatches.Patch(color='red', label='top')
	contr_mp = mpatches.Patch(color='blue', label='controversial')
	leg = plt.legend(handles=[hot_mp, top_mp, contr_mp], frameon = True, loc = 2, fontsize='xx-large', ncol=1)

	plt.grid()
	plt.tight_layout()
	plt.savefig('share_suspendedUsers.png')
	plt.show()