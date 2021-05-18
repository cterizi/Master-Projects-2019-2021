import networkx as nx
import numpy as np
import snap

def returnGraph():
	#load the undirected network
	G = nx.Graph()
	file = open("graph/dblp_graph", 'r')
	for line in file:
		tmp_line = line.replace("\n", "").split("\t")
		source = int(tmp_line[0])
		target = int(tmp_line[1])
		G.add_edge(source, target)
	file.close()
	return(G)

def convertNetworkxGraphIntoSnapGraph(G):
	G_new = snap.TUNGraph.New()
	for node in G.nodes():
		G_new.AddNode(node)
	for edge in G.edges():
		G_new.AddEdge(edge[0], edge[1])
	
	return(G_new)

def clusterNetwroxk(G):
	new_G = convertNetworkxGraphIntoSnapGraph(G)
	CmtyV = snap.TCnComV()
	modularity = snap.CommunityGirvanNewman(new_G, CmtyV)
	for Cmty in CmtyV:
		print("Community: ")
		for NI in Cmty:
			print(NI)
	print("The modularity of the network is %f" % modularity)

def loadCommunitiesAndCalculateModularity(G):
	file = open("communities.txt", 'r')
	data = {}
	tmp_community_id = 0
	for line in file:
		tmp_line = line.replace("\n", "")
		if("Community:" in tmp_line):
			tmp_community_id = tmp_community_id + 1
			data[tmp_community_id] = []
		elif("The modularity of the network is" in tmp_line):
			break
		else:
			data[tmp_community_id].append(int(tmp_line))
	file.close()

	#calculate modularity for each cluster
	new_G = convertNetworkxGraphIntoSnapGraph(G)
	modularityData = {}
	for community in data:
		Nodes = snap.TIntV()
		for nodeId in data[community]:
			Nodes.Add(nodeId)
		modularityData[community] = snap.GetModularity(new_G, Nodes)

	return(data, modularityData)

def exportFileCluster(x, tp):
	file = open("cluster" + tp + ".txt", 'w')
	for cluster_id in x:
		if("Size" in tp):
			file.write(str(cluster_id) + "\t" + str(len(x[cluster_id])) + "\n")
		elif("Modularity" in tp):
			file.write(str(cluster_id) + "\t" + str(x[cluster_id]) + "\n")
	file.close()

def main():
	G = returnGraph()
	clusterNetwroxk(G)
	[setOfNodesForEachCluster, modularityOfEachCluster] = loadCommunitiesAndCalculateModularity(G)
	exportFileCluster(setOfNodesForEachCluster, "Size")
	exportFileCluster(modularityOfEachCluster, "Modularity")

main()