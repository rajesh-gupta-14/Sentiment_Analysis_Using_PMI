#==========================================
# Title:  Upload sentiment analysis results to Elastic Search server
# Author: Vismay Revankar
# Date:   8 Oct 2018
#==========================================

import logging
import json
from elasticsearch import Elasticsearch, helpers
from global_vars import *

class ElasticSearchUpload:

	def __init__(self):
		logging.info("==========Preparing to upload data to Elastic Search Instance==========")
		print("==========Preparing to upload data to Elastic Search Instance==========")
		self.elastic_search_upload()

	def bulk_update(self, es, obj_id, bulk_data):
		logging.info("Uploading records onto the server up till obj_id:" + str(obj_id))
		print("Creating a bulk request to the Elastic Search server")
		helpers.bulk(es,bulk_data)
		print("The data uploaded can now be accessed on the Elastic Search server")

	def create_json_objects(self, es, analysis_results):
		# Structure of JSON obj to be uploaded onto the ES server
		bulk_data = []
		obj_id = 0
		for result in analysis_results:
			action = {}
			action['_index'] = 'sentiment_analysis'
			action['_type'] = 'tweets_analysis'
			obj_id += 1
			action['_id'] = obj_id
			action['_source'] = result
			bulk_data.append(action)
			logging.debug("Object ID of the current JSON object that has been appended: " + str(obj_id))
		self.bulk_update(es, obj_id, bulk_data)


	def read_json_data(self):
		logging.info("Reading the JSON data from file: {}".format(COMBINED_ANALYSIS_JSON))
		with open(COMBINED_ANALYSIS_JSON,'r') as f:
			analysis_results = json.load(f)
		return analysis_results

	def create_index(self, es):
		request_body = {
		    "settings" : {
		        "number_of_shards": 5,
		        "number_of_replicas": 1
		    },

		    'mappings': {}
		}
		result = ""
		if es.indices.exists(INDEX_NAME):
			logging.info("Index " + INDEX_NAME + " already exists")
			logging.info("Deleting the previous index")
			result = es.indices.delete(index = INDEX_NAME)
			logging.info("Response: '%s'" % (result))
		logging.info("Creating new index: " + INDEX_NAME)
		print("Creating new index: " + INDEX_NAME)
		result = es.indices.create(index=INDEX_NAME, body=request_body)
		logging.info("Response: '%s" % (result))

	def elastic_search_upload(self):
		#Connect to Elastic Search instance and test the connection
		es = ""
		try:
			es = Elasticsearch(ES_INSTANCE, port=PORT, http_auth=AUTH_CREDENTIALS)
		except Exception as ex:
			print(str(ex))
		if es.ping():
			logging.info("Connected to elastic search instance: " + ES_INSTANCE)
			print("Connected to elastic search instance: " + ES_INSTANCE)
		else:
			logging.error("Error connecting to elastic search instance: " + ES_INSTANCE)
			logging.error(es)
			print("Error connecting to elastic search instance: " + ES_INSTANCE)

		# Create/Overwrite index 'sentiment_analysis'

		self.create_index(es)

		# Read analysis results from JSON file. This data will then be uploaded to the Elastic Search server
		analysis_results = self.read_json_data()

		# Write the JSON data into a JSON objects and upload onto the server
		self.create_json_objects(es, analysis_results)

		logging.info("============Elastic Search operations concluded============")
