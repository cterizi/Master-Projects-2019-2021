import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os


'''
#############################################
#############################################
Return folders, files
#############################################
#############################################
'''
def returnSubreddits(dir):
	return(['politics'])
	return(os.listdir(dir))

def returnEdgesFiles(dir):
	files = os.listdir(dir)
	filesDict = {'reply':{'hot':'', 'top':'', 'controversial':''}, 'share':{'hot':'', 'top':'', 'controversial':''}}
	for i in files:
		if('share' in i):
			if('hot' in i):
				filesDict['share']['hot'] = i
			elif('top' in i):
				filesDict['share']['top'] = i
			else:
				filesDict['share']['controversial'] = i
		else:
			if('hot' in i):
				filesDict['reply']['hot'] = i
			elif('top' in i):
				filesDict['reply']['top'] = i
			else:
				filesDict['reply']['controversial'] = i
	return(filesDict)


'''
#############################################
#############################################
Load graphs, partition, suspended users
#############################################
#############################################
'''
def loadGraph(path):
	file = open(path, 'r')
	G = nx.Graph()
	for line in file:
		tmp_line = line.replace("\n", "").split(" ")
		if(tmp_line[0] == 'None' or tmp_line[1] == 'None'):
			continue
		G.add_edge(tmp_line[0], tmp_line[1])
	file.close()
	H = G.subgraph(list(max(nx.connected_components(G), key=len)))
	return(H)

def loadPartition(path):
	file = open(path, 'r')
	A = []
	B = []
	for line in file:
		tmp_line = line.split(":")
		if(tmp_line[0].replace("\n", "") == 'A'):
			for usr in tmp_line[1].replace("\n", "").split(","):
				A.append(usr)
		elif(tmp_line[0].replace("\n", "") == 'B'):
			for usr in tmp_line[1].replace("\n", "").split(","):
				B.append(usr)
	file.close()
	return(A[:-1], B[:-1])

def loadSSUsers(path):
	file = open(path, 'r')
	susUsers = []
	for line in file:
		susUsers.append(line.replace("\n", ""))
	file.close()
	return(list(set(susUsers)))


'''
#############################################
#############################################
Show partitioning graph
#############################################
#############################################
'''
def showPartitionGraph(G, partitionA, partitionB, ssUsr, path):
	color_map = []
	susUsr_color_map = []
	for node in G:
		if(node in set(ssUsr)):
			susUsr_color_map.append('orange')
		else:
			if (node in set(partitionA)):
				susUsr_color_map.append('red')
			elif(node in set(partitionB)):
				susUsr_color_map.append('blue')
		if (node in set(partitionA)):
			color_map.append('red')
		elif(node in set(partitionB)):
			color_map.append('blue')

	pos = nx.spring_layout(G)
	nx.draw(G, node_color=color_map, node_size=4, pos=pos, width=0.05)
	plt.savefig(path + "allUsers.png")
	plt.show()
	nx.draw(G, node_color=susUsr_color_map, node_size=4, pos=pos, width=0.1)
	plt.savefig(path + "ssUsers.png")
	plt.show()


'''
#############################################
#############################################
CDF for degree distribution
#############################################
#############################################
'''
def returnDegreeValues(G, d):
	l = []
	for n in d:
		try:
			l.append(G.degree[n])
		except:
			X = 0
	return(l, np.sort(l))

def cdfDegree(G, partitionA, partitionB, ssUsers, path):
	[allGraphDegrees, allGraphDegrees_sorted] = returnDegreeValues(G, list(G.nodes))
	[partitionA_Degree, partitionA_Degree_sorted] = returnDegreeValues(G, partitionA)
	[partitionB_Degree, partitionB_Degree_sorted] = returnDegreeValues(G, partitionB)
	
	[ssUsers_Degree, ssUsers_Degree_sorted] = returnDegreeValues(G, ssUsers)
	[ssUsersA, ssUsersA_sorted] = returnDegreeValues(G, (set(partitionA)).intersection(set(ssUsers)))
	[ssUsersB, ssUsersB_sorted] = returnDegreeValues(G, (set(partitionB)).intersection(set(ssUsers)))

	x_values = np.sort(np.asarray(list(set(allGraphDegrees + partitionA_Degree + partitionB_Degree + ssUsers_Degree))))
	y_all = []
	y_A = []
	y_B = []
	y_SS = []
	y_SS_A = []
	y_SS_B = []
	if(len(ssUsers_Degree) == 0):
			print("There aren't suspended users")
			print(path)
	for i in x_values:
		y_all.append(float((allGraphDegrees_sorted<=i).sum()) / len(allGraphDegrees))
		y_A.append(float((partitionA_Degree_sorted<=i).sum()) / len(partitionA_Degree))
		y_B.append(float((partitionB_Degree_sorted<=i).sum()) / len(partitionB_Degree))
		if(not(len(ssUsers_Degree) == 0)):
			y_SS.append(float((ssUsers_Degree_sorted<=i).sum()) / len(ssUsers_Degree))
			if(not(len(ssUsersA) == 0)):
				y_SS_A.append(float((ssUsersA_sorted<=i).sum()) / len(ssUsersA))
			if(not(len(ssUsersB) == 0)):
				y_SS_B.append(float((ssUsersB_sorted<=i).sum()) / len(ssUsersB))
	showCDF(x_values, y_all, y_A, y_B, path, "")
	#showCDF(x_values, y_SS, y_SS_A, y_SS_B, path, "SS")

def showCDF(x, y_all, y_a, y_b, path, ss):
	fig, ax = plt.subplots()
	if(not(len(y_all) == 0)):
		ax.plot(x, y_all, 'red', linewidth=3)
	if(not(len(y_a) == 0)):
		ax.plot(x, y_a, 'blue', linewidth=3)
	if(not(len(y_b) == 0)):
		ax.plot(x, y_b, 'green', linewidth=3)
	ax.tick_params(axis='y', labelcolor = "black", labelsize=20)
	ax.tick_params(axis='x', labelcolor = "black", labelsize=20)
	ax.set_ylabel("CDF", fontsize=20)
	ax.set_xlabel("degree", fontsize=20)

	if(not(ss == "SS")):
		all_ = mpatches.Patch(color='red', label='total graph')
		A_ = mpatches.Patch(color='blue', label='partition A')
		B_ = mpatches.Patch(color='green', label='partition B')
	else:
		all_ = mpatches.Patch(color='red', label='total suspended users')
		A_ = mpatches.Patch(color='blue', label='partition A')
		B_ = mpatches.Patch(color='green', label='partition B')
	leg = plt.legend(handles=[all_, A_, B_], frameon = True, loc = 0, fontsize='xx-large')

	#plt.title("Degree Cumulative Distribution Function ", loc = 'center', fontsize = 18, color = 'orange')
	plt.grid()
	plt.tight_layout()
	if(not(ss == "SS")):
		plt.savefig(path + "all.png")
	else:
		plt.savefig(path + "ss.png")
	plt.show()


'''
#############################################
#############################################
Calculate statistics
#############################################
#############################################
'''
def statistics(G, partA, partB, ssUsers, path, orderType):
	file = open(path, 'a')
	file.write("--- " + orderType + " ---\n")
	file.write("Number of nodes: " + str(G.number_of_nodes()) + "\n")
	file.write("Number of edges: " + str(G.number_of_edges()) + "\n")
	file.write("Number of suspended users: " + str(len(set(ssUsers))) + ", " + str(len(set(ssUsers)) * 100 / G.number_of_nodes()) + "%\n")	
	file.write("Partinion A: " + str(len(partA)) + ", " + str(len(partA)/G.number_of_nodes()*100) + "%\n")
	file.write("Partinion B: " + str(len(partB)) + ", " + str(len(partB)/G.number_of_nodes()*100) + "%\n")	
	ssUsr_A = set(partA).intersection(set(ssUsers))
	ssUsr_B = set(partB).intersection(set(ssUsers))
	file.write("Suspended users(partition A): " + str(len(ssUsr_A)) + ", " + str(len(ssUsr_A)*100/len(partA)) + "% (in partition), " + str(len(ssUsr_A)*100/G.number_of_nodes()) + "% (in total)\n")
	file.write("Suspended users(partition B): " + str(len(ssUsr_B)) + ", " + str(len(ssUsr_B)*100/len(partB)) + "% (in partition), " + str(len(ssUsr_B)*100/G.number_of_nodes()) + "% (in total)\n")
	file.close()

if __name__=='__main__':
	subreddits = returnSubreddits("data/")
	for sf in subreddits:
		fileNames = returnEdgesFiles("data/" + sf + "/edges/")
		
		for graphType in fileNames:
			if(graphType == 'share'):
				for submissionOrder in fileNames[graphType]:
					if(submissionOrder == 'controversial'):
						print(sf + ", " + graphType + ", " + submissionOrder)
						G = loadGraph("data/" + sf + "/edges/" + fileNames[graphType][submissionOrder])
						[A, B] = loadPartition("data/" + sf + "/partition/" + submissionOrder + "_" + graphType + ".txt")
						ssUsers = loadSSUsers("data/" + sf + "/suspendedUsers/" + submissionOrder + "_" + graphType + ".txt")
						
						#showPartitionGraph(G, A, B, ssUsers, "data/" + sf + "/plots/" + graphType + "/" + submissionOrder + "_")
						cdfDegree(G, A, B, ssUsers, "data/" + sf + "/plots/" + graphType + "/" + submissionOrder + "_cdf_")
						#statistics(G, A, B, ssUsers, "data/" + sf + "/plots/" + graphType + "/statistics.txt", submissionOrder)
						