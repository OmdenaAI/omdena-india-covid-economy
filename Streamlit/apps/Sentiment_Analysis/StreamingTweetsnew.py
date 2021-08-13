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

"""
searchTerms = ["corona", "covid"]
noOfSearch = 5000
searchCountry = "India"

places = api.geo_search(query=searchCountry, granularity="country")
place_id = places[0].id
print(place_id)
tweets = tweepy.Cursor(api.search , q='{} place:{}'.format(searchTerms, place_id)).items(noOfSearch)


for i,tweet in enumerate(tweets):
    print(i, tweet.text)
"""





class MyStreamListener(tweepy.StreamListener):
    def __init__(self,api=None):
        super(MyStreamListener,self).__init__()
        self.num_tweets=0 
    
    def on_status(self, status):
        if status.retweeted:
            return
        else: 
            location = status.user.location
            if location != None and "India" in location:
                print(status.text)
                self.num_tweets+=1
                print(self.num_tweets)
                if self.num_tweets<200:
                    return True
                else:
                    return False
                    #log = open("/path/to/my/file.txt", "r")
                    #print str(log)

                
            
    
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False



stream_listener = MyStreamListener()
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