import praw
import json
import csv
import os

client_id = ""
client_secret = ""
user_agent = ""
username = ""
password = ""

def getInfo_subreddits(subred):
	with open('subreddits_info.csv', mode='a') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		
		#[display_name, subscribers, over18, user_is_banned, public_description]
		writer.writerow([subred.display_name, subred.subscribers, subred.over18, subred.user_is_banned, subred.public_description.replace("\n", "")])

def returnPostPerSubreddit(subred):
	limit = 1000000
	hot = subred.hot(limit = limit) 						#Return the hot items
	controversial = subred.controversial(limit = limit) 	#Return the controversial submissions
	gilded = subred.gilded(limit = limit) 					#Return gilded items
	new = subred.new(limit = limit) 						#Return new items
	top = subred.top(limit = limit) 						#Return top items
	rising = subred.rising(limit = limit) 					#Return the rising submissions
	random_rising = subred.random_rising(limit = limit) 	#Return the random rising submissions
	return([hot, new, top, rising, random_rising, controversial, gilded])

def commentsForest(comments_, fileName, ssUsrFileName, submission_author):
	#Provides an instance of CommentForest (praw.models.comment_forest.CommentForest)
	print("--- COMMENTS-REPLIES FOREST ---")
	comments_.replace_more(limit = None)
	print("--- REPLACE_MORE DONE ---")
	all_comments = comments_.list()
	'''
		The ID of the parent comment. 
		If it is a top-level comment, this returns the submission ID instead 
		(prefixed with ‘t3’).

		Comment ID: ff3e1s7
		Author NAME: accountabilitycounts
		Author ID: pj8rp
		Parent ID: t3_erft6d
	'''
	edgesFile = open(fileName, 'w')
	dictionary_t3_t1 = {} 							#comment_id: user_id
	suspended_users = []
	for com in all_comments:
		if(com.author == 'AutoModerator'): #BOT
			continue
		try:
			#dictionary_t3_t1[str(com)] = str(reddit.redditor(com.author.id))
			dictionary_t3_t1[str(com)] = str(com.author)
			if(not('t3' in str(com.parent_id))):
				edgesFile.write(str(com.author) + " " + dictionary_t3_t1[str(com.parent_id).split("_")[-1]] + "\n")
			else:
				edgesFile.write(str(com.author) + " " + str(submission_author) + "\n")
			
			'''Check if user is suspended or deleted'''
			is_suspended_ = reddit.redditor(com.author.id)
		except:
			''' This account has been suspended or deleted(com.author = None)'''
			if(not(com.author == None)):
				suspended_users.append(str(com.author))
			#print("Account " + str(com.author) + " has been suspended!")
	edgesFile.close()

	#Store suspended users
	suspendedFile = open(ssUsrFileName, 'w')
	for SS_users in list(set(suspended_users)):
		suspendedFile.write(SS_users + "\n")
	suspendedFile.close()
	
	#{'comment_id':username}
	return(dictionary_t3_t1)

def checkInfoPerPost(posts, subredditName, orderType):
	if(not(os.path.exists('data'))):
		os.mkdir('data')
	if(not(os.path.exists('data/' + subredditName))):
		os.mkdir('data/' + subredditName)
	fileName = 'data/' + subredditName + "/" + orderType + '_submissions.csv'
	
	with open(fileName, mode='w') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		
		for post in posts:
			#[title, id, author, score, upvote_ratio, num_comments, total_awards_received]
			# writer.writerow([post.title.replace("\n", "").replace(",", ""), post.id, post.author, post.score, post.upvote_ratio, post.num_comments, post.total_awards_received])
			# print("Number of comments: " + str(post.num_comments))
			# edgeFileName = 'data/' + subredditName + "/" + orderType + '_replyEdges.txt'
			# suspendedUsersFileName = 'data/' + subredditName + "/" + orderType + '_suspendedUsers.txt'
			# comments_usernames_dict = commentsForest(post.comments, edgeFileName, suspendedUsersFileName, post.author)
			# # comments_usernames_dict[str(post.id)] = str(post.author)
			# edgeFileName = 'data/' + subredditName + "/" + orderType + '_shareEdges.txt'
			# generateShareGraph(edgeFileName, comments_usernames_dict, post)
			if(post.num_comments > 10000 and post.num_comments < 15000):
				writer.writerow([post.title.replace("\n", "").replace(",", ""), post.id, post.author, post.score, post.upvote_ratio, post.num_comments, post.total_awards_received])
				print("Number of comments: " + str(post.num_comments))
				edgeFileName = 'data/' + subredditName + "/" + orderType + '_replyEdges.txt'
				suspendedUsersFileName = 'data/' + subredditName + "/" + orderType + '_suspendedUsers.txt'
				comments_usernames_dict = commentsForest(post.comments, edgeFileName, suspendedUsersFileName, post.author)
				break

if __name__=='__main__':
	reddit = praw.Reddit(client_id = client_id, client_secret = client_secret,
						user_agent = user_agent, username = username,
						password = password)

	#focused_subreddits = ['politics', 'gaming', 'worldnews', 'sports', 'atheism', 'jokes', 'art', 'fitness', 'travel', 'tattoos']
	focused_subreddits = ['worldnews']
	for r in focused_subreddits:
		print("--- Subreddit " + r + " ---")
		subred = reddit.subreddit(r)

		#getInfo_subreddits(subred)
		posts = returnPostPerSubreddit(subred)
		'''
		index 0: HOT, index 1: NEW, index 2: TOP, index 3: RISING
		index 4: RANDOM_RISING, index 5: CONTROVERSIAL, index 6: GILDED
		'''
		#print("--- HOT submissions ---")
		#checkInfoPerPost(posts[0], r, 'hot') 			#hot
		#print("--- TOP submissions ---")
		#checkInfoPerPost(posts[2], r, 'top') 			#top
		print("--- CONTROVERSIAL submissions ---")
		checkInfoPerPost(posts[5], r, 'controversial') 	#controversial

# x = next(hot)
# x = dir(x)
