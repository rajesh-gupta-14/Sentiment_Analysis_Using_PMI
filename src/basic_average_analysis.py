#==========================================
# Title:  Perform sentiment analysis using average
# Author: Vismay Revankar
# Date:   2 Oct 2018
#==========================================

import re
from datetime import datetime
import csv
import numpy as np
import json
import logging
from global_vars import *

class BasicAverageSentimentAnalysis:
	np_dictionary = []			# Stores the dictionary in the form of a numpy array

	def __init__(self):
		logging.info("==========Sentiment analysis using basic average==========")
		pass
		
	@staticmethod
	def convert_sentiwordnet_to_csv(input_filename, output_filename):
		logging.info("Converting sentiwordnet lexicon to csv...")
		with open (input_filename,'r') as reader, open(output_filename,'w') as writer:
			reader = reader.readlines()
			start_time = datetime.now().time()
			line_count = 0
			for line in reader:
				line_count += 1
				# read the header and write into the other file
				line_contents = line.split('\t')
				line_contents = line_contents[:-1]
				pattern = re.compile(r'(.*?)#[\d]+')  # Non-greedy matching to stop at every match in the line
				words_to_clean = pattern.findall(line_contents[-1])
				cleaned_words_list = []
				for word in words_to_clean:
					cleaned_words_list.append(word.strip())
				cleaned_words = " ".join(cleaned_words_list)
				line_contents[-1] = cleaned_words
				new_line = ','.join(line_contents)
				writer.write(new_line)
				writer.write('\n')
		logging.info("CSV conversion completed...")

	@staticmethod
	def get_words_in_tweet(tweet):
		words_in_tweet=[]	
		if len(tweet)!=0:
			words_in_tweet = tweet.split()
		return words_in_tweet

	def load_dictionary(self, file_path):
		dictionary_list = []
		with open(file_path,'r') as f:
			csv_data = csv.reader(f, delimiter=',')
			for row in csv_data:
				word_list = []
				word_list.append(row[0])			# Add context of word i.e adjective, noun, etc
				word_list.append(row[2])			# Add positive score of word
				word_list.append(row[3])			# Add negative score of word		
				word_list.append(row[4])			# Add the word(s)
				dictionary_list.append(word_list)	# Add details of the word into the dictionary
		return dictionary_list
			
	@staticmethod
	def return_dictionary_object(raw_tweet, cleaned_tweet, tweet_sentiment, tweet_sentiment_score, tweet_words, tweet_words_scores):
		tweet_json_obj = {}
		tweet_json_obj["raw_tweet"] = raw_tweet
		tweet_json_obj["cleaned_tweet"] = cleaned_tweet
		tweet_json_obj["basic_avg_sentiment"] = tweet_sentiment
		tweet_json_obj["basic_avg_sentiment_score"] = tweet_sentiment_score
		tweet_json_obj["tweet_words"] = tweet_words	
		tweet_json_obj["tweet_words_scores"] = tweet_words_scores
		return tweet_json_obj

	@staticmethod
	def compute_sentiment_scores_of_word(word, dictionary_indices):
		rows = dictionary_indices[0]
		positive_score_sum = 0
		negative_score_sum = 0
		for r in rows:
			logging.debug(str(word) + "(p,n) = (" + str(np_dictionary[r][1]) + "," + str(np_dictionary[r][2]) + ")")
			positive_score_sum += float(np_dictionary[r][1])
			negative_score_sum += float(np_dictionary[r][2])
		logging.debug("\'" + str(word) + "\' p score: " + str(positive_score_sum) + "/" + str(len(rows)))
		logging.debug("\'" + str(word) + "\' n score: " + str(negative_score_sum) + "/" + str(len(rows)))
		avg_positive_score_word = positive_score_sum/(len(rows))
		avg_negative_score_word = negative_score_sum/(len(rows))
		#print("word scores p,n: " + str(avg_positive_score_word) + " " + str(avg_negative_score_word)) 
		return (avg_positive_score_word,avg_negative_score_word)

	def sentiment_analysis(self, raw_tweets, cleaned_tweets):
		sentiment_analysis_results = []
		analysis_results_to_plot = []
		dictionary_list = self.load_dictionary("sentiwordnet_dictionary.csv")	# Change file path as required
		global np_dictionary
		np_dictionary = np.array(dictionary_list)	# Converted to numpy.array for faster search using numpy.where()
		for c_tweet, r_tweet in zip(cleaned_tweets, raw_tweets):
			analysis_result_tweet = {}
			words = self.get_words_in_tweet(c_tweet.strip())
			logging.info("Current tweet: " + str(r_tweet))
			if not words:					# If tweet is empty (exception handling)
				logging.info("Assigning neutral rating for: " + str(r_tweet))
				analysis_result_tweet = self.return_dictionary_object(r_tweet,c_tweet,"neutral","0",[],[])
				sentiment_analysis_results.append(analysis_result_tweet)
			else:
				analysis_result_tweet["raw_tweet"] = r_tweet
				analysis_result_tweet["cleaned_tweet"] = c_tweet
				analysis_result_tweet["tweet_words"] = words
				positive_scores_sum = 0
				negative_scores_sum = 0
				tweet_words_scores = []
				for word in words:
					logging.debug("Current word: " + word)
					word_scores = {}
					indices = np.where(np_dictionary == str(word))
					dict_rows = indices[0]
					logging.debug("dict rows: " + str(dict_rows))
					if len(dict_rows) == 0:							#If the word is not present in the dictionary.
						result = (positive_sentiment_score,negative_sentiment_score) = (0,0) # Consider it neutral
						logging.debug( "\'"+ str(word) + "\' is not in the lexicon. Assigning sentiment (0,0)")
						word_scores["word"] = str(word)
						word_scores["positive"] = str(positive_sentiment_score)
						word_scores["negative"] = str(negative_sentiment_score)
						tweet_words_scores.append(word_scores)
						continue
					else:
						(positive_sentiment_score, negative_sentiment_score) = self.compute_sentiment_scores_of_word(word, indices)
						logging.debug("Sentiment score of " + str(word) + " : " + "(" + str(positive_sentiment_score) + "," + str(negative_sentiment_score) + ")")
						word_scores["word"] = str(word)
						word_scores["positive"] = str(positive_sentiment_score)
						word_scores["negative"] = str(negative_sentiment_score)
						tweet_words_scores.append(word_scores)
						positive_scores_sum += float(positive_sentiment_score)		#Sum up score of every word in tweet
						negative_scores_sum += float(negative_sentiment_score)
				word_count = len(words)
				tweet_sentiment_score = (positive_scores_sum - negative_scores_sum)/word_count
				logging.debug("Calculation for tweet sentiment score = (" + str(positive_scores_sum) + " - "+ str(negative_scores_sum) + ")/" + str(word_count))
				logging.info("Tweet sentiment score: " + str(tweet_sentiment_score))
				if tweet_sentiment_score > 0:
					tweet_sentiment = "positive"
				elif tweet_sentiment_score < 0:
					tweet_sentiment = "negative"
				else:
					tweet_sentiment = "neutral"
				analysis_result_tweet["tweet_words_scores"] = tweet_words_scores
				analysis_result_tweet["basic_avg_sentiment_score"] = str(tweet_sentiment_score)
				analysis_result_tweet["basic_avg_sentiment"] = tweet_sentiment
				sentiment_analysis_results.append(analysis_result_tweet)
				analysis_results_to_plot.append(str(tweet_sentiment_score))
			print("{Basic Avg} Tweet: " + str(c_tweet) + " -> [" + str(tweet_sentiment) + ", " + "{:1.6f}".format(tweet_sentiment_score) + "]")
			logging.info("==========Sentiment analysis using averages concluded==========")
		with open(BASIC_AVG_SENTIMENT_SCORES,'w') as f:
			f.write(str(analysis_results_to_plot))
		return sentiment_analysis_results