# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import folium
import json
import pandas as pd
from sqlalchemy import create_engine
from numpy import nan
from pygeocoder import Geocoder
from geopy.geocoders import Nominatim
import geocoder
import multiprocessing as mp
import os
from shapely.geometry import Point, shape
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    engine = create_engine('postgresql://dbuser:cc0901-!@localhost:5432/gary_test')
    df = pd.read_sql_query('select * from gary', con=engine)
    data_path = './input/'
    df = df.rename(columns={'coordinates': 'coord'})
    df['latitude'] = 0
    df['longitude'] = 0
    df['lat_state'] = 0
    df['long_state'] = 0
    geolocator = Nominatim()
    for i in df.coord.index:
        if df.coord[i] is not None:
            df.loc[i, 'latitude'] = json.loads(df.coord[i]).get('coordinates')[1]
            df.loc[i, 'longitude'] = json.loads(df.coord[i]).get('coordinates')[0]
        # else:
        #     if df.user_location[i] is not None:
        #         try:
        #             #df.loc[i, 'lat_state'] = geolocator.geocode(df.user_location[i]).latitude
        #             #df.loc[i, 'long_state'] = geolocator.geocode(df.user_location[i]).longitude
        #
        #             # df.loc[i, 'lat_state'] = geocoder.google(df.user_location[i]).lat
        #             # df.loc[i, 'long_state'] = geocoder.google(df.user_location[i]).lng
        #
        #             print(i)
        #         except:
        #             print("faster...")
    print ("Finished load latlng !")

    # set 30000
    #df = df[df['lat_state'] != 0].sample(n=100)
    df = df[df['longitude'] != 0]

    def get_follower_segment(user_followers):
        if user_followers <= 100:
            return '0-100'
        elif user_followers <= 1000:
            return '100-1,000'
        elif user_followers <= 10000:
            return '1000-10,000'
        else:
            return '> 10,000'

    df['phone_brand_en'] = df['user_followers'].apply(
        lambda user_followers: get_follower_segment(user_followers))

    df['gender'] = "Yes"
    df['age_segment'] = "No"


    from shapely.geometry import Point, shape
    import json

    with open(data_path + 'geojson/us-states.json') as data_file:
        states_json = json.load(data_file)

    def get_location(longitude, latitude, states_json):
        point = Point(longitude, latitude)
        for record in states_json['features']:
            polygon = shape(record['geometry'])
            polygon = polygon.buffer(0)
            if polygon.contains(point):
                return record['properties']['name']
        return 'other'

    df['location'] = df.apply(lambda row: get_location(row['longitude'], row['latitude'], states_json), axis=1)
    df = df.rename(columns={'created': 'timestamp'})
    cols_to_keep = ['timestamp', 'longitude', 'latitude', 'phone_brand_en', 'gender', 'age_segment',
                    'location','user_description','text']
    df.to_csv('save_gary.csv', index=False, encoding='utf-8')
    df_clean = df[cols_to_keep].dropna()
    df_clean['timestamp'] = df_clean['timestamp'].astype(str)
    tt = df_clean.to_json( orient='records', date_format='iso', date_unit = 's')
    return tt

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
