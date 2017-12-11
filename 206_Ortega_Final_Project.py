###########################################
# File name: 206_Ortega_Final_Project.py  #
# Author: Nicolas Ortega                  #
# Submission date: 12/15/2017             #
# Instructor: Colleen Van Lent            #
###########################################

import requests
import json
import tweepy
import indicoio
import twitter_info
import unittest
import sqlite3
import plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go


#Indico text analysis API key for authentication. Enter your Indico API key here:
indicoio.config.api_key = ''


#Twitter keys for authentication, included in separate folder. Or delete the variable content and paste your own keys/tokens.
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

#Setting up caching pattern.
CACHE_FNAME = "twitter_cache.json"
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}


nusr = str(input("Enter user screen name - "))
def get_tweets(nusr):
    if nusr in CACHE_DICTION: #if statement to use cache
        print('using cache')
        resp_tweets = CACHE_DICTION[nusr]
        #print(resp_tweets)

    else:
        print('fetching') #using .user_timeline method, write to CACHE_FNAME

        resp_tweets = api.user_timeline(id=nusr, count=100)

        CACHE_DICTION[nusr] = resp_tweets #####
        dumped_cache = json.dumps(CACHE_DICTION) #make JSON format
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_cache)
        fw.close
        #print(resp_tweets)
    return resp_tweets


tweets_lst = get_tweets(nusr) #gets 100 tweets from the selected user.
# print (len(tweets_lst)) #100
# print (type(tweets_lst)) #List!


#Function to only get the text from the tweets lst variable that stores the result output of the first function, which includes caching.
def get_tweets_text(tweets_lst):
    only_text_lst = []
    for atweet in tweets_lst:
        tweet_text = atweet["text"]
        only_text_lst.append(tweet_text)

    return only_text_lst #returns a list with only the text for all tweets retrieved.

text_tweets = get_tweets_text(tweets_lst)
# print(type(text_tweets)) #still list
# print(len(text_tweets)) #still 100

##Function to extract the tweet time, will be useful for the plot.ly graph.
def get_tweets_time(tweets_lst):
    only_time_lst = []
    for atweet in tweets_lst:
        tweet_time = atweet["created_at"]
        only_time_lst.append(tweet_time)
    return only_time_lst

time_tweets = get_tweets_time(tweets_lst)
# print (len(time_tweets)) #100
# print(time_tweets) #format ex. 'Mon Nov 27 21:27:15 +0000 2017'


#defining this function only to analyze the text of the tweet using indicoio API.
def analyze_text(text_tweets):
    personality_scores_list = []
    emotion_scores_list = []

    personality = indicoio.personality(text_tweets)
    emotion = indicoio.emotion(text_tweets)

    for x in personality:
        personality_scores_list.append(x)

    for y in emotion:
        emotion_scores_list.append(y)

    return personality_scores_list, emotion_scores_list

text_analysis_sample = analyze_text(text_tweets)
# print(len(text_analysis_sample)) #2, because 2 lists with multiple dictionaries


## defining a variable outside the functions to represent a list, each with the scores for personality and scores for emotion. Use these variable to access the scores and do a graphic representation (plot.ly)

global_personality_scores = text_analysis_sample[0] #list with dictionaries, each dictionary represents personality of a single tweet
global_emotion_scores = text_analysis_sample[1] #list with dictionaries, each dictionary represents emotion of a single tweet


list_personality = list() #will contain only the values for all personality scores (meaning for all 100 of the user's tweets).
list_emotion = list() #will contain only the values for 100 emotion scores.

for adict in global_personality_scores:
    for x in adict:
        list_personality.append(adict[x])

for adict in global_emotion_scores:
    for y in adict:
        list_emotion.append(adict[y])

# print (len(list_personality)) #400, 4 personality categories for 100 tweets
# print (len(list_emotion)) #500, 5 emotions for 100 tweets


#below variable contains a joined list, with every element as a tuple in the order: text, time, personality_scores, emotion_scores

## (https://stackoverflow.com/questions/13704860/zip-lists-in-python)

complete_info_with_person_emotion = list(
zip(text_tweets, time_tweets, global_personality_scores, global_emotion_scores))


## start narrowing down data to days of the week with if/elif statements

monday_tuples = []
tuesday_tuples = []
wednesday_tuples = []
thursday_tuples = []
friday_tuples = []
saturday_tuples = []
sunday_tuples = []

for atup in complete_info_with_person_emotion:
    if 'Mon' in atup[1]:
        monday_tuples.append(atup)
    elif 'Tue' in atup[1]:
        tuesday_tuples.append(atup)
    elif 'Wed' in atup[1]:
        wednesday_tuples.append(atup)
    elif 'Thu' in atup[1]:
        thursday_tuples.append(atup)
    elif 'Fri' in atup[1]:
        friday_tuples.append(atup)
    elif 'Sat'in atup[1]:
        saturday_tuples.append(atup)
    elif 'Sun' in atup[1]:
        sunday_tuples.append(atup)


#next do the mathematic calculations to get the average emotions and personality during the day


##the variables below will contain the values for each variable (PERSONALITY) stored in a list to be averaged and later used as data for plot.ly
monday_open_score = []
tuesday_open_score = []
wednesday_open_score = []
thursday_open_score = []
friday_open_score = []
saturday_open_score = []
sunday_open_score = []

monday_extra_score = []
tuesday_extra_score = []
wednesday_extra_score = []
thursday_extra_score = []
friday_extra_score = []
saturday_extra_score = []
sunday_extra_score = []

monday_agree_score = []
tuesday_agree_score = []
wednesday_agree_score = []
thursday_agree_score = []
friday_agree_score = []
saturday_agree_score = []
sunday_agree_score = []

monday_cons_score = []
tuesday_cons_score = []
wednesday_cons_score = []
thursday_cons_score = []
friday_cons_score = []
saturday_cons_score = []
sunday_cons_score = []


for atup in monday_tuples:
    openness_score = atup[2]['openness']
    # print (type(openness_score)) #float! success.
    monday_open_score.append(openness_score)
    extra_score = atup[2]['extraversion']
    monday_extra_score.append(extra_score)
    agree_score = atup[2]['agreeableness']
    monday_agree_score.append(agree_score)
    cons_score = atup[2]['conscientiousness']
    monday_cons_score.append(cons_score)

# print (monday_open_score) ## it's a list with float values of scores for monday

## do this for every day...
for atup in tuesday_tuples:
    openness_score = atup[2]['openness']
    tuesday_open_score.append(openness_score)
    extra_score = atup[2]['extraversion']
    tuesday_extra_score.append(extra_score)
    agree_score = atup[2]['agreeableness']
    tuesday_agree_score.append(agree_score)
    cons_score = atup[2]['conscientiousness']
    tuesday_cons_score.append(cons_score)

for atup in wednesday_tuples:
    openness_score = atup[2]['openness']
    wednesday_open_score.append(openness_score)
    extra_score = atup[2]['extraversion']
    wednesday_extra_score.append(extra_score)
    agree_score = atup[2]['agreeableness']
    wednesday_agree_score.append(agree_score)
    cons_score = atup[2]['conscientiousness']
    wednesday_cons_score.append(cons_score)

for atup in thursday_tuples:
    openness_score = atup[2]['openness']
    thursday_open_score.append(openness_score)
    extra_score = atup[2]['extraversion']
    thursday_extra_score.append(extra_score)
    agree_score = atup[2]['agreeableness']
    thursday_agree_score.append(agree_score)
    cons_score = atup[2]['conscientiousness']
    thursday_cons_score.append(cons_score)

for atup in friday_tuples:
    openness_score = atup[2]['openness']
    friday_open_score.append(openness_score)
    extra_score = atup[2]['extraversion']
    friday_extra_score.append(extra_score)
    agree_score = atup[2]['agreeableness']
    friday_agree_score.append(agree_score)
    cons_score = atup[2]['conscientiousness']
    friday_cons_score.append(cons_score)

for atup in saturday_tuples:
    openness_score = atup[2]['openness']
    saturday_open_score.append(openness_score)
    extra_score = atup[2]['extraversion']
    saturday_extra_score.append(extra_score)
    agree_score = atup[2]['agreeableness']
    saturday_agree_score.append(agree_score)
    cons_score = atup[2]['conscientiousness']
    saturday_cons_score.append(cons_score)

for atup in sunday_tuples:
    openness_score = atup[2]['openness']
    sunday_open_score.append(openness_score)
    extra_score = atup[2]['extraversion']
    sunday_extra_score.append(extra_score)
    agree_score = atup[2]['agreeableness']
    sunday_agree_score.append(agree_score)
    cons_score = atup[2]['conscientiousness']
    sunday_cons_score.append(cons_score)



##the below variables contain the values for each variable (EMOTION) stored in a list to be averaged and later used as data for plot.ly
monday_anger_score = []
tuesday_anger_score = []
wednesday_anger_score = []
thursday_anger_score = []
friday_anger_score = []
saturday_anger_score = []
sunday_anger_score = []

monday_joy_score = []
tuesday_joy_score = []
wednesday_joy_score = []
thursday_joy_score = []
friday_joy_score = []
saturday_joy_score = []
sunday_joy_score = []

monday_sadness_score = []
tuesday_sadness_score = []
wednesday_sadness_score = []
thursday_sadness_score = []
friday_sadness_score = []
saturday_sadness_score = []
sunday_sadness_score = []

monday_fear_score = []
tuesday_fear_score = []
wednesday_fear_score = []
thursday_fear_score = []
friday_fear_score = []
saturday_fear_score = []
sunday_fear_score = []

monday_surprise_score = []
tuesday_surprise_score = []
wednesday_surprise_score = []
thursday_surprise_score = []
friday_surprise_score = []
saturday_surprise_score = []
sunday_surprise_score = []


for atup in monday_tuples:
    anger_score = atup[3]['anger']
    monday_anger_score.append(anger_score)
    joy_score = atup[3]['joy']
    monday_joy_score.append(joy_score)
    sadness_score = atup[3]['sadness']
    monday_sadness_score.append(sadness_score)
    fear_score = atup[3]['fear']
    monday_fear_score.append(fear_score)
    surprise_score = atup[3]['surprise']
    monday_surprise_score.append(surprise_score)

## do this for every day...

for atup in tuesday_tuples:
    anger_score = atup[3]['anger']
    tuesday_anger_score.append(anger_score)
    joy_score = atup[3]['joy']
    tuesday_joy_score.append(joy_score)
    sadness_score = atup[3]['sadness']
    tuesday_sadness_score.append(sadness_score)
    fear_score = atup[3]['fear']
    tuesday_fear_score.append(fear_score)
    surprise_score = atup[3]['surprise']
    tuesday_surprise_score.append(surprise_score)

for atup in wednesday_tuples:
    anger_score = atup[3]['anger']
    wednesday_anger_score.append(anger_score)
    joy_score = atup[3]['joy']
    wednesday_joy_score.append(joy_score)
    sadness_score = atup[3]['sadness']
    wednesday_sadness_score.append(sadness_score)
    fear_score = atup[3]['fear']
    wednesday_fear_score.append(fear_score)
    surprise_score = atup[3]['surprise']
    wednesday_surprise_score.append(surprise_score)

for atup in thursday_tuples:
    anger_score = atup[3]['anger']
    thursday_anger_score.append(anger_score)
    joy_score = atup[3]['joy']
    thursday_joy_score.append(joy_score)
    sadness_score = atup[3]['sadness']
    thursday_sadness_score.append(sadness_score)
    fear_score = atup[3]['fear']
    thursday_fear_score.append(fear_score)
    surprise_score = atup[3]['surprise']
    thursday_surprise_score.append(surprise_score)

for atup in friday_tuples:
    anger_score = atup[3]['anger']
    friday_anger_score.append(anger_score)
    joy_score = atup[3]['joy']
    friday_joy_score.append(joy_score)
    sadness_score = atup[3]['sadness']
    friday_sadness_score.append(sadness_score)
    fear_score = atup[3]['fear']
    friday_fear_score.append(fear_score)
    surprise_score = atup[3]['surprise']
    friday_surprise_score.append(surprise_score)

for atup in saturday_tuples:
    anger_score = atup[3]['anger']
    saturday_anger_score.append(anger_score)
    joy_score = atup[3]['joy']
    saturday_joy_score.append(joy_score)
    sadness_score = atup[3]['sadness']
    saturday_sadness_score.append(sadness_score)
    fear_score = atup[3]['fear']
    saturday_fear_score.append(fear_score)
    surprise_score = atup[3]['surprise']
    saturday_surprise_score.append(surprise_score)

for atup in sunday_tuples:
    anger_score = atup[3]['anger']
    sunday_anger_score.append(anger_score)
    joy_score = atup[3]['joy']
    sunday_joy_score.append(joy_score)
    sadness_score = atup[3]['sadness']
    sunday_sadness_score.append(sadness_score)
    fear_score = atup[3]['fear']
    sunday_fear_score.append(fear_score)
    surprise_score = atup[3]['surprise']
    sunday_surprise_score.append(surprise_score)


## start getting the necessary values to input into plot.ly portion of the project. This means getting the average for every single emotion and personality trait, for every single day. Variables were previously defined.

## averages for PERSONALITY part
### sometimes the len of the list was 0, and we can't divide by zero. I used if/else statements to check if length of the list is more than 0. If it is, perform the calculation, if not, then the score is 0 for the day.

## OPEN SCORES
if len(monday_open_score) > 0:
    avg_monday_open_score = sum(monday_open_score)/len(monday_open_score)
else:
    avg_monday_open_score = 0

if len(tuesday_open_score) > 0:
    avg_tuesday_open_score = sum(tuesday_open_score)/len(tuesday_open_score)
else:
    avg_tuesday_open_score = 0

if len(wednesday_open_score) > 0:
    avg_wednesday_open_score = sum(wednesday_open_score)/len(wednesday_open_score)
else:
    avg_wednesday_open_score = 0

if len(thursday_open_score) > 0:
    avg_thursday_open_score = sum(thursday_open_score)/len(thursday_open_score)
else:
    avg_thursday_open_score = 0

if len(friday_open_score) > 0:
    avg_friday_open_score = sum(friday_open_score)/len(friday_open_score)
else:
    avg_friday_open_score = 0

if len(saturday_open_score) > 0:
    avg_saturday_open_score = sum(saturday_open_score)/len(saturday_open_score)
else:
    avg_saturday_open_score = 0

if len(sunday_open_score) > 0:
    avg_sunday_open_score = sum(sunday_open_score)/len(sunday_open_score)
else:
    avg_sunday_open_score = 0


## EXTRA SCORES
if len(monday_extra_score) > 0:
    avg_monday_extra_score = sum(monday_extra_score)/len(monday_extra_score)
else:
    avg_monday_extra_score = 0

if len(tuesday_extra_score) > 0:
    avg_tuesday_extra_score = sum(tuesday_extra_score)/len(tuesday_extra_score)
else:
    avg_tuesday_extra_score = 0

if len(wednesday_extra_score) > 0:
    avg_wednesday_extra_score = sum(wednesday_extra_score)/len(wednesday_extra_score)
else:
    avg_wednesday_extra_score = 0

if len(thursday_extra_score) > 0:
    avg_thursday_extra_score = sum(thursday_extra_score)/len(thursday_extra_score)
else:
    avg_thursday_extra_score = 0

if len(friday_extra_score) > 0:
    avg_friday_extra_score = sum(friday_extra_score)/len(friday_extra_score)
else:
    avg_friday_extra_score = 0

if len(saturday_extra_score) > 0:
    avg_saturday_extra_score = sum(saturday_extra_score)/len(saturday_extra_score)
else:
    avg_saturday_extra_score = 0

if len(sunday_extra_score) > 0:
    avg_sunday_extra_score = sum(sunday_extra_score)/len(sunday_extra_score)
else:
    avg_sunday_extra_score = 0


# AGREE SCORES
if len(monday_agree_score) > 0:
    avg_monday_agree_score = sum(monday_agree_score)/len(monday_agree_score)
else:
    avg_monday_agree_score = 0

if len(tuesday_agree_score) > 0:
    avg_tuesday_agree_score = sum(tuesday_agree_score)/len(tuesday_agree_score)
else:
    avg_tuesday_agree_score = 0

if len(wednesday_agree_score) > 0:
    avg_wednesday_agree_score = sum(wednesday_agree_score)/len(wednesday_agree_score)
else:
    avg_wednesday_agree_score = 0

if len(thursday_agree_score) > 0:
    avg_thursday_agree_score = sum(thursday_agree_score)/len(thursday_agree_score)
else:
    avg_thursday_agree_score = 0

if len(friday_agree_score) > 0:
    avg_friday_agree_score = sum(friday_agree_score)/len(friday_agree_score)
else:
    avg_friday_agree_score = 0

if len(saturday_agree_score) > 0:
    avg_saturday_agree_score = sum(saturday_agree_score)/len(saturday_agree_score)
else:
    avg_saturday_agree_score = 0

if len(sunday_agree_score) > 0:
    avg_sunday_agree_score = sum(sunday_agree_score)/len(sunday_agree_score)
else:
    avg_sunday_agree_score = 0


# CONS SCORES
if len(monday_cons_score) > 0:
    avg_monday_cons_score = sum(monday_cons_score)/len(monday_cons_score)
else:
    avg_monday_cons_score = 0

if len(tuesday_cons_score) > 0:
    avg_tuesday_cons_score = sum(tuesday_cons_score)/len(tuesday_cons_score)
else:
    avg_tuesday_cons_score = 0

if len(wednesday_cons_score) > 0:
    avg_wednesday_cons_score = sum(wednesday_cons_score)/len(wednesday_cons_score)
else:
    avg_wednesday_cons_score = 0

if len(thursday_cons_score) > 0:
    avg_thursday_cons_score = sum(thursday_cons_score)/len(thursday_cons_score)
else:
    avg_thursday_cons_score = 0

if len(friday_cons_score) > 0:
    avg_friday_cons_score = sum(friday_cons_score)/len(friday_cons_score)
else:
    avg_friday_cons_score = 0

if len(saturday_cons_score) > 0:
    avg_saturday_cons_score = sum(saturday_cons_score)/len(saturday_cons_score)
else:
    avg_saturday_cons_score = 0

if len(sunday_cons_score) > 0:
    avg_sunday_cons_score = sum(sunday_cons_score)/len(sunday_cons_score)
else:
    avg_sunday_cons_score = 0



## averages for EMOTION part

# ANGER SCORES
if len(monday_anger_score) > 0:
    avg_monday_anger_score = sum(monday_anger_score)/len(monday_anger_score)
else:
    avg_monday_anger_score = 0

if len(tuesday_anger_score) > 0:
    avg_tuesday_anger_score = sum(tuesday_anger_score)/len(tuesday_anger_score)
else:
    avg_tuesday_anger_score = 0

if len(wednesday_anger_score) > 0:
    avg_wednesday_anger_score = sum(wednesday_anger_score)/len(wednesday_anger_score)
else:
    avg_wednesday_anger_score = 0

if len(thursday_anger_score) > 0:
    avg_thursday_anger_score = sum(thursday_anger_score)/len(thursday_anger_score)
else:
    avg_thursday_anger_score = 0

if len(friday_anger_score) > 0:
    avg_friday_anger_score = sum(friday_anger_score)/len(friday_anger_score)
else:
    avg_friday_anger_score = 0

if len(saturday_anger_score) > 0:
    avg_saturday_anger_score = sum(saturday_anger_score)/len(saturday_anger_score)
else:
    avg_saturday_anger_score = 0

if len(sunday_anger_score) > 0:
    avg_sunday_anger_score = sum(sunday_anger_score)/len(sunday_anger_score)
else:
    avg_sunday_anger_score = 0


# JOY SCORES

if len(monday_joy_score) > 0:
    avg_monday_joy_score = sum(monday_joy_score)/len(monday_joy_score)
else:
    avg_monday_joy_score = 0

if len(tuesday_joy_score) > 0:
    avg_tuesday_joy_score = sum(tuesday_joy_score)/len(tuesday_joy_score)
else:
    avg_tuesday_joy_score = 0

if len(wednesday_joy_score) > 0:
    avg_wednesday_joy_score = sum(wednesday_joy_score)/len(wednesday_joy_score)
else:
    avg_wednesday_joy_score = 0

if len(thursday_joy_score) > 0:
    avg_thursday_joy_score = sum(thursday_joy_score)/len(thursday_joy_score)
else:
    avg_thursday_joy_score = 0

if len(friday_joy_score) > 0:
    avg_friday_joy_score = sum(friday_joy_score)/len(friday_joy_score)
else:
    avg_friday_joy_score = 0

if len(saturday_joy_score) > 0:
    avg_saturday_joy_score = sum(saturday_joy_score)/len(saturday_joy_score)
else:
    avg_saturday_joy_score = 0

if len(sunday_joy_score) > 0:
    avg_sunday_joy_score = sum(sunday_joy_score)/len(sunday_joy_score)
else:
    avg_sunday_joy_score = 0

# SADNESS SCORES

if len(monday_sadness_score) > 0:
    avg_monday_sadness_score = sum(monday_sadness_score)/len(monday_sadness_score)
else:
    avg_monday_sadness_score = 0

if len(tuesday_sadness_score) > 0:
    avg_tuesday_sadness_score = sum(tuesday_sadness_score)/len(tuesday_sadness_score)
else:
    avg_tuesday_sadness_score = 0

if len(wednesday_sadness_score) > 0:
    avg_wednesday_sadness_score = sum(wednesday_sadness_score)/len(wednesday_sadness_score)
else:
    avg_wednesday_sadness_score = 0

if len(thursday_sadness_score) > 0:
    avg_thursday_sadness_score = sum(thursday_sadness_score)/len(thursday_sadness_score)
else:
    avg_thursday_sadness_score = 0

if len(friday_sadness_score) > 0:
    avg_friday_sadness_score = sum(friday_sadness_score)/len(friday_sadness_score)
else:
    avg_friday_sadness_score = 0

if len(saturday_sadness_score) > 0:
    avg_saturday_sadness_score = sum(saturday_sadness_score)/len(saturday_sadness_score)
else:
    avg_saturday_sadness_score = 0

if len(sunday_sadness_score) > 0:
    avg_sunday_sadness_score = sum(sunday_sadness_score)/len(sunday_sadness_score)
else:
    avg_sunday_sadness_score = 0

# FEAR SCORES

if len(monday_fear_score) > 0:
    avg_monday_fear_score = sum(monday_fear_score)/len(monday_fear_score)
else:
    avg_monday_fear_score = 0

if len(tuesday_fear_score) > 0:
    avg_tuesday_fear_score = sum(tuesday_fear_score)/len(tuesday_fear_score)
else:
    avg_tuesday_fear_score = 0

if len(wednesday_fear_score) > 0:
    avg_wednesday_fear_score = sum(wednesday_fear_score)/len(wednesday_fear_score)
else:
    avg_wednesday_fear_score = 0

if len(thursday_fear_score) > 0:
    avg_thursday_fear_score = sum(thursday_fear_score)/len(thursday_fear_score)
else:
    avg_thursday_fear_score = 0

if len(friday_fear_score) > 0:
    avg_friday_fear_score = sum(friday_fear_score)/len(friday_fear_score)
else:
    avg_friday_fear_score = 0

if len(saturday_fear_score) > 0:
    avg_saturday_fear_score = sum(saturday_fear_score)/len(saturday_fear_score)
else:
    avg_saturday_fear_score = 0

if len(sunday_fear_score) > 0:
    avg_sunday_fear_score = sum(sunday_fear_score)/len(sunday_fear_score)
else:
    avg_sunday_fear_score = 0

# SURPRISE SCORES

if len(monday_surprise_score) > 0:
    avg_monday_surprise_score = sum(monday_surprise_score)/len(monday_surprise_score)
else:
    avg_monday_surprise_score = 0

if len(tuesday_surprise_score) > 0:
    avg_tuesday_surprise_score = sum(tuesday_surprise_score)/len(tuesday_surprise_score)
else:
    avg_tuesday_surprise_score = 0

if len(wednesday_surprise_score) > 0:
    avg_wednesday_surprise_score = sum(wednesday_surprise_score)/len(wednesday_surprise_score)
else:
    avg_wednesday_surprise_score = 0

if len(thursday_surprise_score) > 0:
    avg_thursday_surprise_score = sum(thursday_surprise_score)/len(thursday_surprise_score)
else:
    avg_thursday_surprise_score = 0

if len(friday_surprise_score) > 0:
    avg_friday_surprise_score = sum(friday_surprise_score)/len(friday_surprise_score)
else:
    avg_friday_surprise_score = 0

if len(saturday_surprise_score) > 0:
    avg_saturday_surprise_score = sum(saturday_surprise_score)/len(saturday_surprise_score)
else:
    avg_saturday_surprise_score = 0

if len(sunday_surprise_score) > 0:
    avg_sunday_surprise_score = sum(sunday_surprise_score)/len(sunday_surprise_score)
else:
    avg_sunday_surprise_score = 0


### begin plot.ly magic

## Output will be two html files, one showing personality scores (all subdivisions within a GROUPED BAR CHART, segmented into 7 different days of the week) and one showing emotion scores (all subdivisions within a GROUPED BAR CHART, segmented into 7 different days of the week)

## further, for this, use offline plotting with the plot.ly python API
### https://stackoverflow.com/questions/37745917/using-plotly-without-online-plotly-account


# variable for use in the x axis of the graphs.
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

## code for personality traits graphing (defining a function for each)
def graph_personality():
    global nusr
    trace1 = go.Bar(
        x = week_days,
        y = [avg_monday_open_score, avg_tuesday_open_score, avg_wednesday_open_score, avg_thursday_open_score, avg_friday_open_score, avg_saturday_open_score, avg_sunday_open_score],
        name='openness',
        marker=dict(
        color='rgb(55, 83, 109)'
        )
    )
    trace2 = go.Bar(
        x = week_days,
        y = [avg_monday_extra_score, avg_tuesday_extra_score, avg_wednesday_extra_score, avg_thursday_extra_score, avg_friday_extra_score, avg_saturday_extra_score, avg_sunday_extra_score],
        name='extraversion',
        marker=dict(
        color='rgb(158,202,225)')

    )

    trace3 = go.Bar(
        x = week_days,
        y = [avg_monday_agree_score, avg_tuesday_agree_score, avg_wednesday_agree_score, avg_thursday_agree_score, avg_friday_agree_score, avg_saturday_agree_score, avg_sunday_agree_score],
        name='agreeableness',
        marker=dict(
        color='rgb(26, 118, 255)'
    )
    )

    trace4 = go.Bar(
        x = week_days,
        y = [avg_monday_cons_score, avg_tuesday_cons_score, avg_wednesday_cons_score, avg_thursday_cons_score, avg_friday_cons_score, avg_saturday_cons_score, avg_sunday_cons_score],
        name='conscientiousness',
        marker=dict(
        color='rgb(8,48,107)'
        )
    )

    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        title='Personality Scores',
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, filename=nusr+'_personality_summary.html') #using string concatenation to customize the html file name to match the entered user.



## code for emotions graphing

def graph_emotion():
    global nusr
    trace1 = go.Bar(
        x = week_days,
        y = [avg_monday_anger_score, avg_tuesday_anger_score, avg_wednesday_anger_score, avg_thursday_anger_score, avg_friday_anger_score, avg_saturday_anger_score, avg_sunday_anger_score],
        name='anger'
    )
    trace2 = go.Bar(
        x = week_days,
        y = [avg_monday_joy_score, avg_tuesday_joy_score, avg_wednesday_joy_score, avg_thursday_joy_score, avg_friday_joy_score, avg_saturday_joy_score, avg_sunday_joy_score],
        name='joy'
    )

    trace3 = go.Bar(
        x = week_days,
        y = [avg_monday_sadness_score, avg_tuesday_sadness_score, avg_wednesday_sadness_score, avg_thursday_sadness_score, avg_friday_sadness_score, avg_saturday_sadness_score, avg_sunday_sadness_score],
        name='sadness'
    )

    trace4 = go.Bar(
        x = week_days,
        y = [avg_monday_fear_score, avg_tuesday_fear_score, avg_wednesday_fear_score, avg_thursday_fear_score, avg_friday_fear_score, avg_saturday_fear_score, avg_sunday_fear_score],
        name='fear'
    )

    trace5 = go.Bar(
        x = week_days,
        y = [avg_monday_surprise_score, avg_tuesday_surprise_score, avg_wednesday_surprise_score, avg_thursday_surprise_score, avg_friday_surprise_score, avg_saturday_surprise_score, avg_sunday_surprise_score],
        name='surprise'
    )

    data = [trace1, trace2, trace3, trace4, trace5]
    layout = go.Layout(
        title='Emotion Scores',
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, filename=nusr+'_emotion_summary.html')


offline_personality_plot = graph_personality()
offline_emotion_plot = graph_emotion()

## Two graphs should open in your browser and be stored in your repository

## onwards, SQL.
conn = sqlite3.connect('tweet_analysis.sqlite')
cur = conn.cursor()


## ('@WorldAndScience Wow, they played D&amp;D in D&amp;D', 'Mon Nov 27 20:55:40 +0000 2017', {'openness': 0.4366378155, 'extraversion': 0.2283626084, 'agreeable ness': 0.4371619276, 'conscientiousness': 0.6269446036}, {'anger': 0.0034544326, 'joy': 0.6675025225, 'sadness': 0.016367323700000002, 'fear': 0.015056027100000001, 'surprise': 0.29761976})
## ^^ sample tuple formats obtained from the ...day_tuples variables.

### create the table for each user, if it doesn't exist.
# https://stackoverflow.com/questions/34392011/create-table-using-a-variable-in-python

cur.execute(
'''
CREATE TABLE IF NOT EXISTS {} (
	"entered_user" TEXT,
	"text" TEXT,
	"time_posted" TIMESTAMP,
	"personality_dict" TEXT,
	"emotion_dict" TEXT)
'''.format(nusr)
)

checky = cur.execute("SELECT * FROM {}".format(nusr))
db_already = cur.fetchall()

#complete_info_with_person_emotion is the previous defined zipped list, excluding entered user to be entered within the iteration.
for atup in complete_info_with_person_emotion:
    #print(atup)

    entry1_text = atup[0]
    entry2_time = atup[1]
    entry3_person = str(atup[2])
    entry4_emotion = str(atup[3])

    input_tup = (nusr, entry1_text, entry2_time, entry3_person, entry4_emotion)

    #handling the case if the information has been written to the db already
    if input_tup not in db_already:

        cur.execute("INSERT INTO {} (entered_user, text, time_posted, personality_dict, emotion_dict) VALUES (?,?,?,?,?)".format(nusr), input_tup)
    else:
        continue

conn.commit()

print ("\n")

print ("Daily Twitter Activity (# of tweets) - ")
a = 'Monday: '+str(len(monday_tuples))
b = 'Tuesday: '+str(len(tuesday_tuples))
c = 'Wednesday: '+str(len(wednesday_tuples))
d = 'Thursday: '+str(len(thursday_tuples))
e = 'Friday: '+str(len(friday_tuples))
f = 'Saturday: '+str(len(saturday_tuples))
g = 'Sunday: '+str(len(sunday_tuples))

print (a)
print (b)
print (c)
print (d)
print (e)
print (f)
print (g)

## Now, finally, generate output for terminal, showing the twitter activity breakdown for each day. Use length of monday_tuples and other days
print ("\n")

print ("Project Unit Tests:")


#############

# Unit tests for further debugging.

class ProjTests(unittest.TestCase):
    def test_cache(self):
        global nusr
        file_read = open("twitter_cache.json","r")
        info = file_read.read()
        file_read.close()
        self.assertTrue(nusr in info)

    def test_getting_tweets(self):
        global nusr
        tweet_lst = get_tweets(nusr)
        self.assertEqual(len(tweet_lst),100, "Testing to see that we have 100 tweets exactly. It will use the cache as it as written into it previously.")

    def test_analysis(self):
        text_tweets = get_tweets_text(tweets_lst)
        analysis_testing = analyze_text(text_tweets)
        self.assertEqual(len(analysis_testing), 2, "Testing to check if text analysis returns 2 dictionaries with the scores.")

    def test_personality_list(self):
        self.assertEqual(len(list_personality), 400, "Testing to check that the list containing personality scores has 400 elements, as personality analyzed 4 categories for 100 tweets, totaling 400.")

    def test_emotion_list(self):
        self.assertEqual(len(list_emotion), 500, "Testing to check that the list with emotion scores has 500 elements. Emotion has 5 categories for 100 tweets, grand total of 500.")

    def test_first_tuple(self):
        for atup in complete_info_with_person_emotion:
            self.assertEqual(len(atup), 4, "Testing if initial tuple is correct length to be inserted to db, not including the user entered.")

    def test_database_length(self):
        global nusr
        conn = sqlite3.connect('tweet_analysis.sqlite')
        cur = conn.cursor()
        cur.execute("SELECT * FROM {} ".format(nusr))
        ans = cur.fetchall()
        self.assertEqual(len(ans), 100, "Testing that the 100 tweets are correctly written to database.")

    def test_database_columns(self):
        global nusr
        conn = sqlite3.connect('tweet_analysis.sqlite')
        cur = conn.cursor()
        cur.execute("SELECT * FROM {}".format(nusr))
        ans = cur.fetchall()
        self.assertEqual(len(ans[1]), 5, "Testing that table created has the 5 columns needed.")


unittest.main(verbosity=2)
