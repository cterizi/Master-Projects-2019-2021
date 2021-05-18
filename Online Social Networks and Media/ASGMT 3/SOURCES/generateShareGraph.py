import matplotlib.pyplot as plt
import networkx as nx
import praw
import csv
import os

client_id = ""
client_secret = ""
user_agent = ""
username = ""
password = ""

def returnPostPerSubreddit(subred):
	limit = 1000
	hot = subred.hot(limit = limit) 						#Return the hot items
	controversial = subred.controversial(limit = limit) 	#Return the controversial submissions
	gilded = subred.gilded(limit = limit) 					#Return gilded items
	new = subred.new(limit = limit) 						#Return new items
	top = subred.top(limit = limit) 						#Return top items
	rising = subred.rising(limit = limit) 					#Return the rising submissions
	random_rising = subred.random_rising(limit = limit) 	#Return the random rising submissions
	return([hot, new, top, rising, random_rising, controversial, gilded])

def generateGraph(R, data, fileName, ssFileName):
	G = nx.Graph()
	ssUsers = []
	author_shared_submissions = {}
	with open(fileName, mode='w') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for submission_id in data:
			#title, id, author, score, upvote_ratio, total_awards_received
			writer.writerow([submission_id.title.replace("\n", "").replace(",", ""), submission_id.id, submission_id.author, submission_id.score, submission_id.upvote_ratio, submission_id.total_awards_received])
			for i in R.submission(id = submission_id).duplicates():
				if(str(submission_id.author) == "None" or str(i.author) == "None"):
					continue
				G.add_edge(str(submission_id.author), str(i.author))
				try:
					is_suspended_ = R.redditor(i.author.id)
				except:
					ssUsers.append(str(i.author))
				try:
					is_suspended_ = R.redditor(submission_id.author.id)
				except:
					ssUsers.append(str(submission_id.author))
	H = G.subgraph(list(max(nx.connected_components(G), key=len)))
	
	#Store suspended users
	file = open(ssFileName, 'w')
	for u in list(set(ssUsers)):
		file.write(u + "\n")
	file.close()
	return(H)

def writeGraph(G, filePath):
	file = open(filePath, 'w')
	for edge in G.edges():
		file.write(edge[0] + " " + edge[1] + "\n")
	file.close()

if __name__=='__main__':
	reddit = praw.Reddit(client_id = client_id, client_secret = client_secret,
						user_agent = user_agent, username = username,
						password = password)

	#focused_subreddits = ['politics', 'worldnews', 'sports']
	focused_subreddits = ['sports']

	for r in focused_subreddits:
		print("--- Subreddit " + r + " ---")
		subred = reddit.subreddit(r)
		posts = returnPostPerSubreddit(subred)
		'''
		index 0: HOT, index 1: NEW, index 2: TOP, index 3: RISING
		index 4: RANDOM_RISING, index 5: CONTROVERSIAL, index 6: GILDED
		'''
		# G_hot= generateGraph(reddit, posts[0], "data/" + r + "/info/hot_sharedGraph.csv", "data/" + r + "/suspendedUsers/hot_share.txt")
		# writeGraph(G_hot, "data/" + r + "/edges/hot_sharedEdges.txt")
		# print("--- HOT GRAPH DONE ---")

		# G_top = generateGraph(reddit, posts[2], "data/" + r + "/info/top_sharedGraph.csv", "data/" + r + "/suspendedUsers/top_share.txt")
		# writeGraph(G_top, "data/" + r + "/edges/top_sharedEdges.txt")
		# print("--- TOP GRAPH DONE ---")

		G_controversial = generateGraph(reddit, posts[5], "data/" + r + "/info/controversial_sharedGraph.csv", "data/" + r + "/suspendedUsers/controversial_share.txt")
		writeGraph(G_controversial, "data/" + r + "/edges/controversial_sharedEdges.txt")
		print("--- CONTROVERSIAL GRAPH DONE ---")
		
