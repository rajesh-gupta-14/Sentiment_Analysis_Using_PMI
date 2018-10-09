#==========================================
# Title: Main program to run Sentiment Analysis
# Authors: Rajesh Gupta & Vismay Revankar
# Date:   6 Oct 2018
#==========================================

import logging
from datetime import datetime
import csv, json
import os

from fetch_tweets import FetchTwitterData
from clean_twitter_data import CleanTwitterData
from basic_average_analysis import BasicAverageSentimentAnalysis
from pointwise_mutual_information import PointwiseMutualInformation
from upload_to_elasticsearch_server import *
from utility_functions import *
from global_vars import *
from plot_graph import *
				
def main():
	raw_twitter_data=[]
	configure_logger()
	logging.info("==========Script execution started==========")
	logging.info("Authenticating with the Twitter API...")
	raw_tweets_json = FetchTwitterData(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
	for query in TWITTER_QUERIES:
		query_result = raw_tweets_json.get_tweets(query)
		raw_twitter_data.append(query_result)
	logging.info("Writing the fetched tweets into a csv file")
	write_raw_twitter_data_to_csv(raw_twitter_data) #writing raw tweets to a csv
	raw_tweets = get_raw_tweets_from_csv()
	logging.info("Cleaning the tweets to retain only textual content")
	process_tweets = CleanTwitterData()
	cleaned_tweets = process_tweets.clean_with_regex(raw_tweets)
	print("Sentinment analysis method 1: Performing sentiment analysis using basic averages")
	basic_avg_analysis = BasicAverageSentimentAnalysis()
	basic_avg_analysis.convert_sentiwordnet_to_csv(SENTIWORDNET_TXT_FORMAT,SENTIWORDNET_CSV_FORMAT)
	basic_avg_analysis_result = basic_avg_analysis.sentiment_analysis(raw_tweets, cleaned_tweets)
	print("Sentinment analysis method 2: Performing sentiment analysis using Pointwise Mutual Information (PMI)")
	pmi_analysis = PointwiseMutualInformation(basic_avg_analysis_result)
	combined_analysis_result = pmi_analysis.calculate_sentiment()
	logging.info("Writing JSON into file for elastic search")
	combined_analysis_json = json.dumps(combined_analysis_result)
	with open(COMBINED_ANALYSIS_JSON,"w") as op:
		op.write(combined_analysis_json)
	logging.info("==========Sentiment Analysis step completed==========")
	print("==========Sentiment Analysis step completed==========")
	print("Uploading the results to Elastic Search...")
	logging.info("==========Preparing to upload data to Elastic Search Instance==========")
	es_upload = ElasticSearchUpload()
	logging.info("==========Data uploaded to Elastic Search Instance==========")
	print("Elastic Search upload completed")
	print("Plotting graph for the analyses. The graph can be found in the plot_data folder.")
	plot_data = collect_data()
	visualize_data(plot_data)
	logging.info("==========End of program execution==========")
	
if __name__ == "__main__":
	main()
