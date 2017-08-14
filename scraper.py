import settings
import tweepy
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json

import private
from sqlalchemy import create_engine
import pandas as pd
def create_db():
    import psycopg2.extensions
    con = psycopg2.connect(dbname='postgres',
                       user=private.user_name, host='localhost',
                       password=private.password)
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE
    cur = con.cursor()
    cur.execute("CREATE DATABASE %s  ;" % private.DB_NAME)
    return "Database created!"

engine = create_engine('postgresql://postgres' + ':' + private.password + '@localhost:5432/postgres')
dbname = private.DB_NAME
df = pd.read_sql_query("select * from pg_database where datname='" + dbname + "'", con=engine)
if df.empty is True:
    create_db()

db = dataset.connect(settings.CONNECTION_STRING)

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.retweeted:
            return

        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        sent = blob.sentiment

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)

        table = db[settings.TABLE_NAME]
        try:
            table.insert(dict(
                user_description=description,
                user_location=loc,
                coordinates=coords,
                text=text,
                geo=geo,
                user_name=name,
                user_created=user_created,
                user_followers=followers,
                id_str=id_str,
                created=created,
                retweet_count=retweets,
                user_bg_color=bg_color,
                polarity=sent.polarity,
                subjectivity=sent.subjectivity,
            ))
        except ProgrammingError as err:
            print(err)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

auth = tweepy.OAuthHandler(settings.Consumer_Key, settings.Consumer_Secret)
auth.set_access_token(settings.Access_Token, settings.Access_Token_Secret)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)
