import os

#Twitte API credentials
CONSUMER_KEY = "eRvtkP6oXaUK6ZiCKCnOPujQ8"
CONSUMER_SECRET = "91vze0F0XCeNw442JWtW7vQdN36fAthDcfsXAhOCuM3KScvGQK"
ACCESS_KEY = "1044693780224462849-sgHwgJaSKB5Vm9C6R9yKsHlApxdwlx"
ACCESS_SECRET = "XP9kVkHm8b7DAqqDi3CqSm4JznLdCc0yNrXpkWVM7JaBD"
#User Query
TWITTER_QUERIES = ["Apple","@Windows", "#Google","\"One Plus\"", "Samsung", "Xiaomi", "Huawei", "Sony", "#Asus", "Amazon", "Dell"]
#Raw Twitter Data CSV filename
TWITTER_DATA_CSV = "raw_twitter_data.csv"
#Sentiwordnet lexicon
SENTIWORDNET_TXT_FORMAT="sentiwordnet_dictionary.txt"
SENTIWORDNET_CSV_FORMAT="sentiwordnet_dictionary.csv"
#Combined analysis result file
COMBINED_ANALYSIS_JSON="combined_analysis.json"
#Variables used for Elastic Search related operations
ES_INSTANCE = "https://portal-ssl60-37.bmix-dal-yp-97350131-99a6-4192-8c65-2396e69530aa.2008549710.composedb.com:58425"
PORT = 58425
AUTH_CREDENTIALS = ('admin','WBEYBYTJVEMWUKFP')
INDEX_NAME = "sentiment_analysis"
#Filenames for plotting the graphs
BASIC_AVG_SENTIMENT_SCORES = os.path.join(os.getcwd(),"plot_data\\basic_avg_sentiment_scores.txt")
PMI_SENTIMENT_SCORES = os.path.join(os.getcwd(),"plot_data\pmi_sentiment_scores.txt")