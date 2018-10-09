#==========================================
# Title: Plot the results of the analyses 
# Authors: Rajesh Gupta
# Date:   8 Oct 2018
#==========================================

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import ast, os
from global_vars import BASIC_AVG_SENTIMENT_SCORES, PMI_SENTIMENT_SCORES

def collect_data():
    sentiment_data=[]
    with open(BASIC_AVG_SENTIMENT_SCORES,"r") as f:
        basic_avg_data = f.read()
    basic_avg_data = ast.literal_eval(basic_avg_data)
    with open(PMI_SENTIMENT_SCORES,"r") as f:
        pmi_data = f.read()
    pmi_data = ast.literal_eval(pmi_data)
    for i in zip(basic_avg_data,pmi_data):
        sentiment_data.append([float(i[1]),float(i[0])])
        
    sentiment_dataframe = pd.DataFrame(sentiment_data, columns=["pmi_data","basic_avg_data"])
    return sentiment_dataframe

def visualize_data(sentiment_dataframe):
	fig, ax= plt.subplots()
	fig.set_size_inches(11,8)
	sns.set_context("poster")
	sns.set_style("white")
	sns_plot = sns.lineplot(data=sentiment_dataframe, ax=ax, hue="event", dashes=False)
	plt.savefig(os.path.join(os.getcwd(),"plot_data/visualize_basic_avg_and_pmi.png"))

visualize_data(collect_data())
