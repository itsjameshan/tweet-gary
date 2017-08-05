# Twitter search API + pandas interactive dashboard for GaryVee related tweets
As one of the most influence social media icon, Gary Vaynerchuk has influenced hundreds thousnds of people, entrepreneurs, and bussinesses across United State by spreading the messages of hustle, care, positivity, Jets. I happended to be one of them. His work ethic moitivates hourdreds and thousands entrepreneurs to keep hard on their business and make an impact on others. 

This repository shows you how to use tweepy to scrape gary related tweets and hashtag thourgh twitter API and vaisulize them on a interactive map. It scrapes tweets and save them into a postgresql. Then users tweets are showed on a map by reading data from the DB. This turitial used 
* Pandas to cleaning data 
* Tweepy library scrape tweets through twitter api
* Flask to build the server 
* Javascript libraries d3.js, dc.js and crossfilter.js to buid the charts and 
* Leaflet.js for building the map

## Get Started
You can 
```python
git clone https://github.com/itsjameshan/tweet-gary.git
```
or download this repository to your local and test the app.

### Installation
Install the requirements.txt file first.This file included the packge for runing the app. I suggested to use python 2.7. If you use > python 3.x, the Shapely package may not compatiable. 

#### Python
Install pandas, tweepy, Shapely and other python packages.
```python
pip install -r requirements.txt
```

#### Twitter API
* Create a file named private.py for store your twitter app keys later.
* Register a [twitter developer account](https://dev.twitter.com/)
* Create an [twitter app](https://apps.twitter.com/) in the twitter developer account page after login by using your twitter account.
* Set the following keys in private.py. The keys can be found under *Keys and Access token tab* of your [twitter app](https://apps.twitter.com/) page:

  * `Consumer_Key`
  * Consumer_Secret
  * Access_Token
  * Access_Token_Secret

* Set the following key in private.py .
  
```python
CONNECTION_STRING = "postgresql://your_own_username:your_own_password@localhost:5432/your_db_name" 
```
as a default. It's recommended to use postgresql.
* Install [postgresql](https://www.postgresql.org/download/) in your computer. Create a user (your_own_username) or use default postgresql db user name. Create an passord (your_own_password). And create a table name (your_db_name).

```python
until finished!
```

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```python
Give an example
```


### And unit tests


Explain what these tests test and why

```python
Give an example
```


## Deployment

Add additional notes about how to deploy this on a live system


## Reference
This project is inspiared by:
https://github.com/dataquestio/twitter-scrape
https://github.com/adilmoujahid/kaggle-talkingdata-visualization/blob/master/README.md

