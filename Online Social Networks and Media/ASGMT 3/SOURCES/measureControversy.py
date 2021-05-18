import networkx as nx
import random,numpy,sys,os
from operator import itemgetter

# percent = float(sys.argv[3])/100;
#percent = 0.10

'''
#############################################
#############################################
Return folders, files
#############################################
#############################################
'''
def returnSubreddits(dir):
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
Load graphs, partition
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
		G.add_edge(tmp_line[0], tmp_line[1], weight=1)
	file.close()
	H = G.subgraph(list(max(nx.connected_components(G), key=len)))
	return(H)

def loadPartition(path):
	file = open(path, 'r')
	A = [] #left
	dict_left = {}

	B = [] #right
	dict_right = {}

	for line in file:
		tmp_line = line.split(":")
		if(tmp_line[0].replace("\n", "") == 'A'):
			for usr in tmp_line[1].replace("\n", "").split(","):
				A.append(usr)
				dict_left[usr] = 1
		elif(tmp_line[0].replace("\n", "") == 'B'):
			for usr in tmp_line[1].replace("\n", "").split(","):
				B.append(usr)
				dict_right[usr] = 1

	file.close()
	return(A[:-1], dict_left, B[:-1], dict_right)


'''
#############################################
#############################################
Functions for Random Walks score
#############################################
#############################################
'''
def getRandomNodes(G,k): # parameter k = number of random nodes to generate
	nodes = G.nodes()
	random_nodes = {}
	for i in range(k):
		random_num = random.randint(0,len(nodes)-1)
		random_nodes[nodes[random_num]] = 1
	return(random_nodes)

def getRandomNodesFromLabels(G,k,flag): # parameter k = no. of random nodes to generate, flag could be "left", "right" or "both". If both, k/2 from one side and k/2 from the other side are generated.
	random_nodes = []
	random_nodes1 = {}
	if(flag=="left"):
		for i in range(k):
			random_num = random.randint(0,len(left)-1)
			random_nodes.append(left[random_num])
	elif(flag=="right"):
		for i in range(k):
			random_num = random.randint(0,len(right)-1)
			random_nodes.append(right[random_num])
	else:
		for i in range(k/2):
			random_num = random.randint(0,len(left)-1)
			random_nodes.append(left[random_num])
		for i in range(k/2):
			random_num = random.randint(0,len(right)-1)
			random_nodes.append(right[random_num])
	for ele in random_nodes:
		random_nodes1[ele] = 1
	return(random_nodes1)

def getNodesFromLabelsWithHighestDegree(G,k,flag): # first take the nodes with the highest degree according to the "flag" and then take the top $k$
	random_nodes = {}
	dict_degrees = {}
	for node in G.nodes():
		dict_degrees[node] = G.degree(node)
	sorted_dict = sorted(dict_degrees.items(), key=itemgetter(1), reverse=True) # sorts nodes by degrees
#	sorted_dict = sorted_dict[:k];
	if(flag=="left"):
		count = 0
		for i in sorted_dict:
			if(count>k):
				break
			if(not dict_left.has_key(i[0])):
				continue
			random_nodes[i[0]] = i[1]
			count += 1
	elif(flag=="right"):
		count = 0
		for i in sorted_dict:
			if(count>k):
				break
			if(not dict_right.has_key(i[0])):
				continue
			random_nodes[i[0]] = i[1]
			count += 1
	else:
		count = 0
		for i in sorted_dict:
			if(count>k/2):
				break
			if(not dict_left.has_key(i[0])):
				continue
			random_nodes[i[0]] = i[1]
			count += 1
		count = 0
		for i in sorted_dict:
			if(count>k/2):
				break
			if(not dict_right.has_key(i[0])):
				continue
			random_nodes[i[0]] = i[1]
			count += 1
	return(random_nodes)

def performRandomWalk(G,starting_node,user_nodes_side1,user_nodes_side2): # returns if we ended up in a "left" node or a "right" node;
	dict_nodes = {} # contains unique nodes seen till now;
	nodes = G.nodes()
	num_edges = len(G.edges())
	step_count = 0
#	total_other_nodes = len(user_nodes.keys());
	flag = 0
	side = ""

	while(flag!=1):
		# print "starting from ", starting_node, "num nodes visited ", len(dict_nodes.keys()), " out of ", len(nodes);
		neighbors = list(G.neighbors(starting_node))
		random_num = random.randint(0,len(neighbors)-1)
		starting_node = neighbors[random_num]
		dict_nodes[starting_node] = 1
		step_count += 1
		if(starting_node in user_nodes_side1):
			side = "left"
			flag = 1
		if(starting_node in user_nodes_side2):
			side = "right"
			flag = 1
#		if(step_count>num_edges**2): # if stuck
#			break;
#		if(step_count%100000==0):
#			print >> sys.stderr, step_count, "steps reached";
	return(side)

def performRandomWalkFull(G,starting_node,user_nodes): # returns the number of steps taken before reaching *ALL* node from the set of user nodes. difference from the above method is that we should reach all nodes, instead of just any one of them.
	dict_nodes = {} # contains unique nodes seen till now;
	nodes = G.nodes()
	num_edges = len(G.edges())
	step_count = 0
	total_other_nodes = len(user_nodes.keys())
	dict_already_seen_nodes = {}
	flag = 0

	while(flag!=1):
		# print "starting from ", starting_node, "num nodes visited ", len(dict_nodes.keys()), " out of ", len(nodes);
		neighbors = G.neighbors(starting_node)
		random_num = random.randint(0,len(neighbors)-1)
		starting_node = neighbors[random_num]
		dict_nodes[starting_node] = 1
		step_count += 1
		if(user_nodes.has_key(starting_node)):
			dict_already_seen_nodes[starting_node] = 1
			print >> sys.stderr, "seen nodes ", len(dict_already_seen_nodes.keys())
			if(len(dict_already_seen_nodes.keys())==total_other_nodes):
				flag = 1
		if(step_count>num_edges**2): # if stuck
			break
		if(step_count%100000==0):
			print >> sys.stderr, step_count, "steps reached"
	return(step_count)

def getDict(nodes_list):
	dict_nodes = {}
	for node in nodes_list:
		dict_nodes[node] = 1
	return(dict_nodes)


'''
#############################################
#############################################
MAIN
#############################################
#############################################
'''
if __name__=='__main__':
	subreddits = returnSubreddits("data/")
	resultsFile = open("RWS.txt", 'a')
	for sf in subreddits:
		fileNames = returnEdgesFiles("data/" + sf + "/edges/")
		
		for graphType in fileNames:
			for submissionOrder in fileNames[graphType]:
				G = loadGraph("data/" + sf + "/edges/" + fileNames[graphType][submissionOrder])
				[left, dict_left, right, dict_right] = loadPartition("data/" + sf + "/partition/" + submissionOrder + "_" + graphType + ".txt")

				percent = 0.10;

				left_left = 0; # start_end
				left_right = 0;
				right_right = 0;
				right_left = 0;

				left_percent = int(percent*len(dict_left.keys()));
				right_percent = int(percent*len(dict_right.keys()));
				
				for j in range(1,1000):
					if(j%200 == 0):
						print("Iteration " + str(j))
					user_nodes_left = getRandomNodesFromLabels(G,left_percent,"left");
					user_nodes_right = getRandomNodesFromLabels(G,right_percent,"right");

					num_repetitions = 100 # number of repetitions, should change
					total_steps = []

					user_nodes_left_list = user_nodes_left.keys()
					for i in range(len(user_nodes_left_list)-1):
						node = list(user_nodes_left_list)[i]
						other_nodes = list(user_nodes_left_list)[:i] + list(user_nodes_left_list)[i+1:]
						other_nodes_dict = getDict(other_nodes)
						side = performRandomWalk(G,node,other_nodes_dict,user_nodes_right)
						# print(side)
						if(side=="left"):
							left_left += 1
						elif(side=="right"):
							left_right += 1

					user_nodes_right_list = user_nodes_right.keys()
					for i in range(len(user_nodes_right_list)-1):
						node = list(user_nodes_right_list)[i];
						other_nodes = list(user_nodes_right_list)[:i] + list(user_nodes_right_list)[i+1:];
						other_nodes_dict = getDict(other_nodes);
						side = performRandomWalk(G,node,user_nodes_left,other_nodes_dict);
						if(side=="left"):
							right_left += 1;
						elif(side=="right"):
							right_right += 1;
						else: # side == ""
							continue;

					# if(j%1==0):
					# 	print >> sys.stderr, j
				# print("left -> left:" + str(left_left))
				# print("left -> right:" + str(left_right))
				# print("right -> right:" + str(right_right))
				# print("right -> left:"+ str(right_left))

				e1 = left_left*1.0/(left_left+right_left)
				e2 = left_right*1.0/(left_right+right_right)
				e3 = right_left*1.0/(left_left+right_left)
				e4 = right_right*1.0/(left_right+right_right)

				score = e1*e4 - e2*e3
				print(sf + "\t" + graphType + "\t" + submissionOrder + "\t" + str(score))
				resultsFile.write(sf + "\t" + graphType + "\t" + submissionOrder + "\t" + str(score) + "\n")
				resultsFile.flush()
	resultsFile.close()		