import matplotlib.pyplot as plt
import numpy as np
import os.path
import sys
import csv

class ExtractCSV:
	def __init__(self, filename):
		self.filename = filename
		self.originalTweetIdsHashtable = {}

	def startTransformation(self):
		file = open(self.filename, 'r')
		numberOfDeletedTweets = 0
		numberOfTweets = 0
		for line in file:
			'''
			CREATED TIME(t) | TWEET ID(T) | ORIGINAL TWEET ID(R) | CREATED TIME(Q_t) | ORIGINAL TWEET ID(Q) | CREATED TIME(RT_t) | ORIGINAL TWEET ID(RT)
			'''
			
			fields = self.extractFields(line)
			if(len(fields) == 0):
				numberOfDeletedTweets = numberOfDeletedTweets + 1
			else:
				numberOfTweets = numberOfTweets + 1
			if(len(fields) == 7):
				self.prepareCSV(fields)
		
		print("Deleted tweets: " + str(numberOfDeletedTweets))
		print("Total tweets: " + str(numberOfTweets))

		file.close()

	def prepareCSV(self, row):
		tweetID = row[1]
		createdAt = row[0]

		quoted_ = 0
		retweeted_ = 0
		if(row[2] == 'null'):
			if(row[4] == 'null'):
				if(row[6] == 'null'):
					originalTweetID = row[1]
				else:
					originalTweetID = row[6]
			else:
				if(row[6] == 'null'):
					originalTweetID = row[4]
				else:
					if(row[3] == 'null'):
						originalTweetID = row[4]
					else:
						quotedCreatedTime = row[3].replace("\n", "").split(" ")
						retweetedCreatedTime = row[5].replace("\n", "").split(" ")
						'''Check YEAR'''
						if(int(quotedCreatedTime[-1]) < int(retweetedCreatedTime[-1])):
							originalTweetID = row[4]
						elif(int(quotedCreatedTime[-1]) > int(retweetedCreatedTime[-1])):
							originalTweetID = row[6]
						else:
							'''Check MONTH'''
							months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
							if(months.index(quotedCreatedTime[1]) < months.index(retweetedCreatedTime[1])):
								originalTweetID = row[4]
							elif(months.index(quotedCreatedTime[1]) > months.index(retweetedCreatedTime[1])):
								originalTweetID = row[6]
							else:
								'''Check DAY'''
								if(int(quotedCreatedTime[2]) < int(retweetedCreatedTime[2])):
									originalTweetID = row[4]
								elif(int(quotedCreatedTime[2]) > int(retweetedCreatedTime[2])):
									originalTweetID = row[6]
								else:
									'''Check TIME'''
									'''Check HOUR'''
									if(int(quotedCreatedTime[3].split(":")[0]) < int(retweetedCreatedTime[3].split(":")[0])):
										originalTweetID = row[4]
									elif(int(quotedCreatedTime[3].split(":")[0]) > int(retweetedCreatedTime[3].split(":")[0])):
										originalTweetID = row[6]
									else:
										'''Check MINUTES'''
										if(int(quotedCreatedTime[3].split(":")[1]) < int(retweetedCreatedTime[3].split(":")[1])):
											originalTweetID = row[4]
										elif(int(quotedCreatedTime[3].split(":")[1]) > int(retweetedCreatedTime[3].split(":")[1])):
											originalTweetID = row[6]
										else:
											'''Check SECONDS'''
											if(int(quotedCreatedTime[3].split(":")[-1]) < int(retweetedCreatedTime[3].split(":")[-1])):
												originalTweetID = row[4]
											elif(int(quotedCreatedTime[3].split(":")[-1]) > int(retweetedCreatedTime[3].split(":")[-1])):
												originalTweetID = row[6]
											else:
												originalTweetID = -1
												print("ERROR - Date is same!")
		else:
			originalTweetID = row[2]
		self.updateInfo(originalTweetID)
		self.writeGT(originalTweetID, row[1])

	def writeGT(self, tweetID, currentTweetId):
		if('sample' in self.filename):
			nm = 'sample_gt.csv'
		else:
			nm = 'gt.csv'
		with open(nm, mode='a') as tmp_file:
			writer = csv.writer(tmp_file, delimiter=',')
			writer.writerow([tweetID, currentTweetId, self.originalTweetIdsHashtable[tweetID]])

	def updateInfo(self, originalTweetID):
		if(not(originalTweetID in self.originalTweetIdsHashtable)):
			self.originalTweetIdsHashtable[originalTweetID] = 1
		else:
			self.originalTweetIdsHashtable[originalTweetID] = self.originalTweetIdsHashtable[originalTweetID] + 1

	def extractFields(self, data):
		generalInfo = ["\"created_at\"", "\"id_str\"", "\"in_reply_to_status_id_str\"", "\"quoted_status_id_str\"", "\"retweeted_status\""]
		
		tmp_line = data.replace("\n", "").split(",")
		
		info = []
		if(not("delete" in data)):
		
			'''
			created_at = UTC time when this Tweet was created.
						String
			'''
			if(generalInfo[0] in tmp_line[0]):
				info.append(tmp_line[0].replace("\n", "").split("created_at\":")[1].replace("\"", ""))

				'''
				id_str = The string representation of the unique identifier for this Tweet. 
				Implementations should use this rather than the large integer in id. 
				'''
				if(generalInfo[1] in tmp_line[2]):
					info.append(tmp_line[2].replace("\n", "").split("id_str\":")[1].replace("\"", ""))
				else:
					info.append("")
			else:
				info.append("")


			tmp_in = False
			for f in range(0, len(tmp_line)):
				'''
				in_reply_to_status_id_str = If the represented Tweet is a reply, this field will 
				contain the string representation of the original Tweet’s ID.
				'''			
				if(generalInfo[2] in tmp_line[f]):
					info.append(tmp_line[f].replace("\n", "").split(":")[1].replace("\"", ""))
					tmp_in = True
					break
			if(tmp_in == False):
				info.append("null")

			tmp_in = False
			for f in range(0, len(tmp_line)):
				'''
				quoted_status_id_str = This field only surfaces when the Tweet is a quote Tweet. 
									This is the string representation Tweet ID of the quoted Tweet.
				A quote tweet is a kind of retweet. 
				While a simple retweet merely shares another person's tweet, 
				a quote tweet lets you share another person's tweet and add your own comments to it. 
				Quote tweets are sometimes also referred to as a "Retweet with comment."				
				'''

				if(generalInfo[3] in tmp_line[f]):
					info.append(tmp_line[f + 1].replace("\n", "").split("created_at\":")[-1].replace("\"", ""))
					info.append(tmp_line[f].replace("\n", "").split(":")[1].replace("\"", ""))
					if(not('+' in info[-2])):
						info[-2] = "null"
					tmp_in = True
					break
			if(tmp_in == False):
				info.append("null")
				info.append("null")

			tmp_in = False
			for f in range(0, len(tmp_line)):
				'''
				retweeted_status = Tweet
				EXTRACTED FIELD: retweeted_status.id_str
				'''
				if(generalInfo[4] in tmp_line[f]):
					info.append(tmp_line[f].replace("\n", "").split("created_at\":")[-1].replace("\"", ""))
					info.append(tmp_line[f+2].replace("\n", "").split(":")[-1].replace("\"", ""))
					tmp_in = True
					break
			if(tmp_in == False):
				info.append("null")
				info.append("null")

		return(info)

	def exportCDFValues(self):
		cdfValues = []
		for key in self.originalTweetIdsHashtable:
			cdfValues.append(self.originalTweetIdsHashtable[key])
		return(np.asarray(cdfValues))

class cdfPlots:
	def __init__(self, values, filename):
		self.values = values
		self.filename = filename

	def cdf(self):
		sortedData_ = np.sort(np.asarray(self.values))
		y_values_ = []
		for i in list(set(self.values)):
			y_values_.append(float((sortedData_<=i).sum()) / len(self.values))
		
		fig, ax1 = plt.subplots()
		ax1.plot(list(set(self.values)), y_values_)
		ax1.tick_params(axis='y', labelcolor = "black", labelsize=14)
		ax1.tick_params(axis='x', labelcolor = "black", labelsize=14)
		ax1.set_ylabel("probability", fontsize=14)
		ax1.set_xlabel("frequency values", fontsize=14)
		plt.title("CDF of value from (key, value)\n where (key, value) = (Original Tweet, Frequency)", loc = 'center', fontsize = 14, color = 'orange')

		plt.grid()
		plt.tight_layout()

		if('sample' in self.filename):
			plt.savefig("sample_cdf_key_values.png")
		else:
			plt.savefig("cdf_key_values.png")
		plt.show()

'''
MAIN PROCEDURE
'''
if __name__ == "__main__":
	if(not(len(sys.argv) == 2)):
		print("====================================================================")
		print("====================================================================")
		print("Wrong input parameters!\nCommand format: python3 \"PYTHON FILE NAME.py\" \"FILE NAME.json\"\ne.g. python3 extractFields.py tweets.json")
		print("OR the input file is not in the same path with the executed python file.\nPlease, COPY-PASTE your input file in the same folder!")
		print("====================================================================")
		print("====================================================================")
		exit()
	
	csvObject = ExtractCSV(sys.argv[1])
	csvObject.startTransformation()

	cdfValues = csvObject.exportCDFValues()
	cdfObject = cdfPlots(cdfValues, sys.argv[1])
	cdfObject.cdf()