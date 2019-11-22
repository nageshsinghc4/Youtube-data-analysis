#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 16:40:36 2019

@author: nageshsinghchauhan
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from subprocess import check_output
import json
from wordcloud import WordCloud, STOPWORDS

data = pd.read_csv("/Users/nageshsinghchauhan/Downloads/ML/kaggle/youtubevideo/USvideos.csv")
#for getting unique values
data.nunique() 

#Let's start looking if Views, likes, dislikes and comment counts have a normal distribuition
data['likes_log']= np.log(data['likes']+1)
data['views_log']= np.log(data['views']+1)
data['dislikes_log']= np.log(data['dislikes']+1)
data['comment_log']= np.log(data['comment_count']+1)

plt.figure(figsize = (12,6))

plt.subplot(221)
g1 = sns.distplot(data['views_log'])
g1.set_title("VIEWS LOG DISTRIBUITION", fontsize=16)

plt.subplot(224)
g1 = sns.distplot(data['likes_log'],color='green')
g1.set_title("LIKES LOG DISTRIBUITION", fontsize=16)

plt.subplot(223)
g1 = sns.distplot(data['dislikes_log'], color='red')
g1.set_title("DISLIKES LOG DISTRIBUITION", fontsize=16)

plt.subplot(222)
g1 = sns.distplot(data['comment_log'], color='blue')
g1.set_title("COMMENT COUNT LOG DISTRIBUITION", fontsize=16)
plt.subplots_adjust(wspace = 0.2, hspace = 0.4,top = 0.9)
plt.show()

#Find the quantile for each normal distribution
print("Views quantile")
print(data['views'].quantile([0.01, 0.25, 0.50, 0.75, 0.99]))
print(" ")

print("Likes quantile")
print(data['likes'].quantile([0.01, 0.25, 0.50, 0.75, 0.99]))
print(" ")

print("Dislikes quantile")
print(data['dislikes'].quantile([0.01, 0.25, 0.50, 0.75, 0.99]))
print(" ")

print("Comment count quantile")
print(data['comment_count'].quantile([0.01, 0.25, 0.50, 0.75, 0.99]))
print(" ")

#If we look at the trending_date or publish_time columns, we see that they are not yet in the correct format of datetime data.
data['trending_date'] = pd.to_datetime(data['trending_date'], format = '%y.%d.%m')
data['publish_time'] = pd.to_datetime(data['publish_time'], format = '%Y-%m-%dT%H:%M:%S.%fZ')

#Here we are adding the category column after the category_id column, using the US_category_id.json file for lookup | creates a dictionary that maps `category_id` to `category`
id_to_category = {}
with open("/Users/nageshsinghchauhan/Downloads/US_category_id.json", 'r') as f:
    data_category = json.load(f)
    for category in data_category['items']:
        id_to_category[category['id']] = category['snippet']['title']

data['category_id'] = data['category_id'].astype(str)
data.insert(4, 'category', data['category_id'].map(id_to_category))

#Users like videos from which CATEGORY the most?
trend_df = data['category'].value_counts().reset_index()
plt.figure(figsize=(10,7))
sns.set_style("whitegrid")
ax = sns.barplot(y=trend_df['index'],x=trend_df['category'], data=data,orient='h')
plt.xlabel("Number of Videos")## From United Kingdom users : 
plt.ylabel("Categories")
plt.title("Catogories of trend videos in USA")

def visualize_most(data, column, num): # getting the top 10 videos by default
    sorted_df = data.sort_values(column, ascending=False).iloc[:num]
    ax = sorted_df[column].plot.bar()
    labels = []
    for item in sorted_df['title']:
        labels.append(item[:10])
    ax.set_xticklabels(labels, rotation=45, fontsize=10)
    plt.show()
    
visualize_most(data, 'views', 10)
visualize_most(data, 'likes')
visualize_most(data, 'views')









