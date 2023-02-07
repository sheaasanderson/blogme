#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 15:41:38 2023

"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Reading excel/xlsx files
data = pd.read_excel('articles.xlsx')


# Getting summary of data and columns
data.describe()
data.info()


# Counting number of articles per source
data.groupby(['source_id'])['article_id'].count()


# Counting number of reactions per source
data.groupby(['source_id'])['engagement_reaction_count'].sum()


# Dropping engagement plugin count column
data = data.drop('engagement_comment_plugin_count', axis = 1)


# Creating keyword flag
keyword = 'crash'


# Creating a for loop to isolate each title row for first 10 rows
keyword_flag = [] # to create column for for loop results
for x in range(0,10):
    headline = data['title'][x]
    if keyword in headline: 
        flag = 1
    else: 
        flag = 0
    keyword_flag.append(flag) # to put flag value in the created keyword_flag column


# Creating a function to apply to entire dataset
def keywordflag(keyword):
    length = len(data)
    keyword_flag = [] 
    for x in range(0,length):
        headline = data['title'][x]
        if keyword in headline: 
            flag = 1
        else: 
            flag = 0
        keyword_flag.append(flag) 
    return keyword_flag
    
keywordflag = keywordflag('murder')
    

# Adjusting function to account for nulls
def keywordflag(keyword):
    length = len(data)
    keyword_flag = [] 
    for x in range(0,length):
        headline = data['title'][x]
        try:
            if keyword in headline: 
                flag = 1
            else: 
                flag = 0
        except: 
            flag = 0 # if the headline doesn't exist, just fill 0 since the keyword won't exist there
        keyword_flag.append(flag) 
    return keyword_flag
    
keywordflag = keywordflag('murder')
    

# Adding keywordflag to data frame
data['keyword_flag'] = pd.Series(keywordflag)
    

# SentimentIntensityAnalyzer
sent_int = SentimentIntensityAnalyzer()
text = data['title'][16]
sent = sent_int.polarity_scores(text)
# compound value closer to -1 is negative; closer to 1 is positive

neg = sent['neg']
pos = sent['pos']
neu = sent['neu']


# Adding a for loop to extract sentiment per title
title_neg_sentiment = []
title_pos_sentiment = []
title_neu_sentiment = []

for x in range(0,len(data)):
    try:
        text = data['title'][x]
        sent_int = SentimentIntensityAnalyzer()
        sent = sent_int.polarity_scores(text)
        neg = sent['neg']
        pos = sent['pos']
        neu = sent['neu']
    except: 
        neg = 0
        pos = 0
        neu = 0
    title_neg_sentiment.append(neg)
    title_pos_sentiment.append(pos)
    title_neu_sentiment.append(neu)


# Turning sentiment values into series to be added as columns
title_neg_sentiment = pd.Series(title_neg_sentiment)
title_pos_sentiment = pd.Series(title_pos_sentiment)
title_neu_sentiment = pd.Series(title_neu_sentiment)


# Adding sentiment columns to data frame
data['title_neg_sentiment'] = title_neg_sentiment
data['title_pos_sentiment'] = title_pos_sentiment
data['title_neu_sentiment'] = title_neu_sentiment


# Writing data as .xlsx
data.to_excel('blogme_clean.xlsx', sheet_name = 'blogmedata', index = False)



    