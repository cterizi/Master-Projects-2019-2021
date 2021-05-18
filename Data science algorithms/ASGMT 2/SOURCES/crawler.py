from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import credentials

import time
import sys

class TwitterStreamer():
	
	def stream_tweets(self, fetched_tweets_filename, hash_tag_list, runtime, startTime):
		listener = StdOutListener(fetched_tweets_filename, runtime, startTime)
		auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
		auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

		stream = Stream(auth, listener)
		#stream.filter(track = hash_tag_list)
		stream.sample()
		

class StdOutListener(StreamListener):

	def __init__(self, fetched_tweets_filename, runtime, startTime):
		self.fetched_tweets_filename = fetched_tweets_filename
		self.runtime = runtime
		self.startTime = startTime
		self.numberTweets = 0

	def on_data(self, data):
		try:
			print(data)
			with open(self.fetched_tweets_filename, 'a') as tf:
				tf.write(data)
				self.numberTweets = self.numberTweets + 1
		except ProtocolError as pe:
			#print("Protocol Error: %s" % str(pe))
			time.sleep(10)
			return(False)
		except BaseException as e:
			#print("Error on_data: %s" %str(e))
			time.sleep(10)
			return(False)

		currentTime = time.time()
		if(currentTime - self.startTime > self.runtime):
			print("Runtime is over")
			print(str(self.numberTweets) + " tweets have been collected!")
			return(False)
		else:
			return(True)
		#id_str = retweeted_status.id_str
		
	def on_error(self, status):
		print(status)


if __name__ == "__main__":
	runtime = float(sys.argv[1])

	hash_tag_list = ['australia']
	fetched_tweets_filename = "tweets.json"

	startTime = time.time()
	twitter_streamer = TwitterStreamer()
	twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list, runtime, startTime)
