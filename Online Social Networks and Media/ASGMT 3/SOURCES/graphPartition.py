import networkx as nx
import nxmetis
import os

def returnFolders(dir):
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

def applyMetis(G, path):
	A = nxmetis.partition(G, 2)
	file = open(path, 'w')
	file.write("A:")
	for u in A[1][0]:
		file.write(u + ",")
	file.write("\n")
	file.write("B:")
	for u in A[1][1]:
		file.write(u + ",")
	file.close()

if __name__=='__main__':
	subfolders = returnFolders("data/")
	for sf in subfolders:
		fileNames = returnEdgesFiles("data/" + sf + "/edges/")
		
		for graphType in fileNames:
			for submissionOrder in fileNames[graphType]:
				G = loadGraph("data/" + sf + "/edges/" + fileNames[graphType][submissionOrder])
				applyMetis(G, "data/" + sf + "/partition/" + submissionOrder + "_" + graphType + ".txt")
