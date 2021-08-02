#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!pip install dataset


# In[19]:


import settings
import tweepy


# In[20]:


auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)


# In[21]:


class MYStreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        if status.retweeted:
            return
        else: 
            location = status.user.location
            if location != None and "India" in location:                
                print(status.text)
    
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


# In[ ]:


stream_listener = MYStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)

