#==========================================
# Title:  Perform sentiment analysis using Pointwise Mutual Information
# Author: Rajesh Gupta
# Date:   4 Oct 2018
#==========================================

import csv, re
from math import log2
import logging
from global_vars import *

class PointwiseMutualInformation():
	
	def __init__(self, all_tweets):
		logging.info("==========Sentiment analysis using pointwise mutual information (PMI)==========")
		self.all_tweets = all_tweets
		self.get_positive_tweets()
		self.get_negative_tweets()
		
	def get_positive_tweets(self):
		self.positive_tweets = list(filter(lambda tweet: tweet["basic_avg_sentiment"]=="positive",self.all_tweets))
		return self.positive_tweets 
	
	def get_negative_tweets(self):
		self.negative_tweets = list(filter(lambda tweet: tweet["basic_avg_sentiment"]=="negative",self.all_tweets))
		return self.negative_tweets

	def get_no_positive_tweets(self):
		return len(self.positive_tweets)
	
	def get_no_negative_tweets(self):
		return len(self.negative_tweets)
			
	def get_count_positive_tweets_with_word(self, word):
		return len(list(filter(lambda tweet: tweet["basic_avg_sentiment"]=="positive" and word in tweet["tweet_words"], self.all_tweets)))
		
	def get_count_negative_tweets_with_word(self, word):
		return len(list(filter(lambda tweet: tweet["basic_avg_sentiment"]=="negative" and word in tweet["tweet_words"], self.all_tweets)))
		
	def pmi(self, word):
		try:
			return log2((self.get_count_positive_tweets_with_word(word)*self.get_no_negative_tweets())/							
				(self.get_count_negative_tweets_with_word(word)*self.get_no_positive_tweets()))
		except Exception as e:
			return 0
		
	def calculate_sentiment(self):
		analysis_results_to_plot = []
		for index, tweet in enumerate(self.all_tweets):
			score = 0
			for word in tweet["tweet_words"]:
				score += self.pmi(word)
			score = score/len(tweet["tweet_words"]) if len(tweet["tweet_words"])>0 else 0
			sentiment = "positive" if score>0 else "negative"
			logging.info("PMI sentiment score for {}: {} - {}".format(tweet, score, sentiment))
			self.all_tweets[index].update({"pmi_sentiment_score":score,"pmi_sentiment":sentiment})
			print("{PMI} Tweet: " + str(tweet["cleaned_tweet"]) + " -> [" + str(sentiment) + ", " + "{:1.6f}".format(score) + "]")
			analysis_results_to_plot.append(str(score))
			#logging.info("==========Sentiment analysis completed==========")
		logging.info("==========Sentiment analysis using pointwise mutual information completed==========")
		with open(PMI_SENTIMENT_SCORES,'w') as f:
			f.write(str(analysis_results_to_plot))
		return self.all_tweets
	
