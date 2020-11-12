"""
Created on Fri Nov  6 10:53:17 2020

@author: zwies
"""

import praw
from datetime import datetime
import pandas as pd

#connect to reddit api (private data removed)
reddit = praw.Reddit(
    client_id="'*********************',",
    client_secret="'*********************',",
    user_agent="'*********************',",
    username = '*********************',
    password = '*********************'
) 

#Grab top supmission from subreddit
subreddit = reddit.subreddit('politics')
subs = subreddit.top('week')


#create empty dataframe
dfp = pd.DataFrame()


#grab all comments from sumbissions and append them to the dataframe
i = 0
for sub in subs:
    i = i + 1
    print(i)
    if sub.created_utc > 1604188800: #limit to election week only
        
        dt = datetime.utcfromtimestamp(sub.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        
        
        sub.comments.replace_more(limit=0) # flatten tree
        comments = sub.comments.list() # all comments
    for comment in comments:
        sub_dict = {
          "sub": sub,
          "id": sub.id,
          "score": sub.score,
          "title": sub.title,
          "stickied": sub.stickied,
          "url": sub.url,
          "date": dt,
          
          "comment_id": comment.id,
          "comment_score": comment.score,
          "comment": comment.body
        }
        dfp = dfp.append(sub_dict, ignore_index=True)


#%% Sentiment Analysis
from textblob import TextBlob
from tqdm import tqdm
tqdm.pandas()

def sentiment_calc(text):
    try:
        return TextBlob(text).sentiment.polarity, TextBlob(text).sentiment.subjectivity
    except:
        return None
    
dfp['sent'] = dfp['comment'].progress_apply(sentiment_calc)
dfp[['polarity', 'subjectivity']] = pd.DataFrame(dfp['sent'].tolist(), index=dfp.index) 


#%% Aggergate to day
dfp['date'] = pd.to_datetime(dfp['date'])
dfp['day'] = pd.DatetimeIndex(dfp['date']).day
agg = dfp.groupby('day',   as_index = False).mean()

#graph
import seaborn as sns
import matplotlib

import matplotlib.pyplot as plt
import numpy as np
plt.style.use('fivethirtyeight')


a4_dims = (13, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)


ax =sns.lineplot(data=df, x="day", y="polarity",  markers=True, color  ='red' , alpha = .5 )
ax.set_title("r/Conservative's Sentiment Over Election Week", size=24 )
ax.set_ylabel('Positivity')
ax.set_xlabel('Date')
ax.set_xticklabels(['0','11-1', '11-2', '11-3', '11-4', '11-5', '11-6'])
plt.text(5.5,.0495,'u/zweaselfear', alpha = .1)

