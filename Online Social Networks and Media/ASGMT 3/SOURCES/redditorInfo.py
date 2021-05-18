import praw
import csv
import os

client_id = ""
client_secret = ""
user_agent = ""
username = ""
password = ""

def returnSubreddits(path):
	return([f.path for f in os.scandir(path) if f.is_dir()])

def returnEdgesFileNames(dir):
	return(os.listdir(dir))

def returnRedditos(filePath):
	file = open(filePath, 'r')
	users = []
	for edge in file:
		tmp_edge = edge.replace("\n", "").split(" ")
		if(not(tmp_edge[0] == 'None')):
			users.append(tmp_edge[0])
		if(not(tmp_edge[1] == 'None')):
			users.append(tmp_edge[1])
	file.close()
	return(list(set(users)))

def extractRedditorsInfo(R, usersList):
	with open('redittorInfo.csv', mode='a') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['username', 'user_id', 'comment_karma', 'link_karma', 'user_is_banned', 'over_18', 'submissions', 'comments'])
		
		for user in usersList:
			user = 'chterizi'
			'''
			Extract submissions(hot, top, new, controversial) where the specific user is the author 
			submission_id
			'''
			submissions_list = []
			for i in R.redditor(user).submissions.top('all'):
				submissions_list.append(str(i.id))
			for i in R.redditor(user).submissions.hot():
				submissions_list.append(str(i.id))
			for i in R.redditor(user).submissions.new():
				submissions_list.append(str(i.id))
			for i in R.redditor(user).submissions.controversial('all'):
				submissions_list.append(str(i.id))

			'''
			Extract comments information
			comment_id, submission_id, submission_author
			'''
			comments_list = []
			for i in R.redditor(user).comments.hot():
				comments_list.append((str(i.id), str(i.link_id), str(R.submission(id = i.link_id.split("_")[1]).author)))
			for i in R.redditor(user).comments.top('all'):
				comments_list.append((str(i.id), str(i.link_id), str(R.submission(id = i.link_id.split("_")[1]).author)))
			for i in R.redditor(user).comments.new():
				comments_list.append((str(i.id), str(i.link_id), str(R.submission(id = i.link_id.split("_")[1]).author)))
			for i in R.redditor(user).comments.controversial('all'):
				comments_list.append((str(i.id), str(i.link_id), str(R.submission(id = i.link_id.split("_")[1]).author)))
			writer.writerow([R.redditor(user).name, R.redditor(user).id, R.redditor(user).comment_karma, R.redditor(user).link_karma, R.redditor(user).subreddit['user_is_banned'], R.redditor(user).subreddit['over_18'], set(submissions_list), set(comments_list)])

			
if __name__=='__main__':
	reddit = praw.Reddit(client_id = client_id, client_secret = client_secret,
						user_agent = user_agent, username = username,
						password = password)

	'''load Redditors'''
	subreddits = returnSubreddits("data/")
	redditors = []
	for sf in subreddits[0:3]:
		files = returnEdgesFileNames(sf + "/edges/")
		for fl in files:
			redditors = redditors + returnRedditos(sf + "/edges/" + fl)
	
	redditors = list(set(redditors))
	extractRedditorsInfo(reddit, redditors)
