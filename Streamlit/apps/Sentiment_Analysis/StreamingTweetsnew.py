#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!pip install dataset


# In[19]:


import settings
import tweepy
import datetime

# In[20]:


auth = tweepy.OAuthHandler(settings.API_key, settings.API_Secret_Key)
auth.set_access_token(settings.Access_token, settings.Access_Token_Secret)
api = tweepy.API(auth)


# In[21]:


class MYStreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        if status.retweeted:
            return
        else: 
            location = status.user.location
            if location != None and "India" in location:
                if status.created_at.strftime("%Y/%m/%d") == "2021/08/08": #figure month
                    with open("./Tweet/August__2021.txt", "w") as text_file: #month
                        text_file.write(status.text)
                        print(status.text)
                    #log = open("/path/to/my/file.txt", "r")
                    #print str(log)

                
            
    
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False



stream_listener = MYStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)

"""
USE TWINT WITH MAJOR CITY NAME IF TWEEPY DOESNT WORK
INPSIRATION: https://www.kaggle.com/general/207512
import twint
#configuration
config = twint.Config()
config.Search = ["corona", "covid"]
config.limit=4000
config.Lang = "en"
config.Since = '2021-08-07'
config.Until = '2021-08-8'
config.Geo= ""
config.Pandas = True

#running search
twint.run.Search(config)

df = twint.storage.panda.Tweets_df

print(df.tweet)
"""