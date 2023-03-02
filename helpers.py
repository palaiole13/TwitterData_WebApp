from config import API_key_public
from config import API_key_Secret
from config import Bearer_Token
from config import Access_token
from config import Access_token_secret

import tweepy
import json
import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session, jsonify
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Read credentials
api_key = API_key_public
api_key_secret = API_key_Secret
access_token = Access_token
access_token_secret = Access_token_secret

# Authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api =tweepy.API(auth)

'''
def jsonify_tweepy(object):
    for i in object:
        json_str = json.dumps(i._json, indent = 2)
    return json.loads(json_str)
'''

def jsonify_tweepy(object):
    json_str = json.dumps(object._json)
    return json.loads(json_str)


#followers = list(tweepy.Cursor(api.followers).items())
#followers_list = [jsonify_tweepy(follower) for follower in followers]

keyword = 'offsets'
limit = 10

def lookup(keyword):
    try:
        tweets = [tweet for tweet in tweepy.Cursor(api.search_tweets, q = {keyword}, result_type = "mixed").items(15)]
        tweets_list = [jsonify_tweepy(tweet) for tweet in tweets]
        lst = []
        for item in tweets_list:
            lst_tmp = []
            lst_tmp.append(item['user']['name']),
            lst_tmp.append(item['user']['description']),
            lst_tmp.append(item['user']['location']),
            lst_tmp.append(item["text"]),
            lst_tmp.append(item['created_at']),
            lst_tmp.append(item['retweet_count']),
            lst_tmp.append(item['favorite_count'])

            lst.append(lst_tmp)
        return {
            "users": [i[0:] for i in lst]
        }

    except (KeyError, TypeError, ValueError):
        return None



'''
def lookup(keyword):
    try:
        tweets = [tweet for tweet in tweepy.Cursor(api.search_tweets, q = {keyword}, result_type = "mixed").items(limit)]
        return {
            "name": jsonify_tweepy(tweets)['user']['name'],
            "description": jsonify_tweepy(tweets)['user']['description'],
            "date": jsonify_tweepy(tweets)['created_at'],
            "tweet": jsonify_tweepy(tweets)['text'],
            "retweet_count": jsonify_tweepy(tweets)['retweet_count']
        }
    except (KeyError, TypeError, ValueError):
        return None
'''
