# Twitter search API + pandas interactive dashboard for GaryVee related tweets

![alt text](./demo3.gif)
As one of the most influence social media icon, Gary Vaynerchuk has influenced hundreds thousnds of people, entrepreneurs, and bussinesses across United State by spreading the messages of hustle, care, positivity, Jets. I happended to be one of them. His work ethic moitivates hourdreds and thousands entrepreneurs to work hard on their business and make an impact on others. 

This repository shows you how to use tweepy to scrape gary related tweets or hashtag through twitter API and visualize them on a interactive map. It scrapes tweets and save them into a postgresql DB. Then users tweets are showed on a map by reading data from the DB. This turitial used 
* `Pandas` to cleaning data 
* `Tweepy` library scrape tweets through twitter api
* `Flask` framework to build the server 
* `d3.js`,`dc.js` and `crossfilter.js` to buid the charts and 
* `Leaflet.js` for building the map

## Step 1. Installation

First, cd to a path in terminal where you want to put the repository. Then
```python
git clone https://github.com/itsjameshan/tweet-gary.git
```
or download this repository to your local folder.

#### Python
cd into the folder you cloned or downloaded and create an virtual enviroment by
```python
pip install virtualenv
virtualenv py27
```
Activate the enviroment in the folder
```python
source py27/bin/activate
```
Install `pandas`, `tweepy`, `Shapely` and other python packages. This file included the packge for runing the app. I suggested to use python 2.7. If you use > python 3.x, the Shapely package may not compatible.
```python
pip install -r requirements.txt
```
If you get en erro on `OSError: Could not find or load any library geos_c icts of variants ['libgeos_c.so.1', 'libgeos_c.so']`, use `pip uninstall Shapely` to unstall Shapely, and then use `conda install Shapely` to install Shapely. But You need to install [conda](https://conda.io/docs/install/quick.html) first.

## Step 2. Modify one script

#### Twitter API
* Create a file named private.py for store your twitter app keys later.
* Register a [twitter developer account](https://dev.twitter.com/)
* Create an [twitter app](https://apps.twitter.com/) in the twitter developer account page after login by using your twitter account.
* Generate API keys and tokens. The keys can be found under *Keys and Access token* tab of your [twitter app](https://apps.twitter.com/) page. You need to go to the bottom of that tab and click *create my access token* to get the token:
* Copy and paste the keys and tokens into `private.py`

  * `Consumer_Key = ""`
  * `Consumer_Secret = ""`
  * `Access_Token = ""`
  * `Access_Token_Secret = ""`

* Install [postgresql](https://www.postgresql.org/download/) on your computer. Create a user (your_own_username) or use default postgresql db user name. Create an password (your_own_password)(suggest to use the Mac password if you run on a Mac). And create a new database(your_db_name). You can download a [pgAdmin](https://www.pgadmin.org/download/) to make the operation easier.
* Replace `your_own_username`,`your_own_password`,`your_db_name` with your own respectively in `private.py`.
  
  * `user_name = "your_own_username"`
  * `password = "your_own_password"`
  * `DB_NAME = "your_db_name"`
 
* If you want to change the search key words, replace the keywords in the first line of `setting.py`.

## Step 3. Run the script
#### Pandas dashboard

##### Realtime data
* Run `scraper.py` first before run `app.py`. It will scrape gary related tweets in real-time. It creates a table named gary under the new database. And search tweets which have `#garyvee`, `Gary vee`, `GaryVee`, `Gary Vaynerchuk`, `vaynermedia` and store them in the databse. Use `Ctrl + C` to stop the script.
##### Demo data 
* Change the `DB_NAME` to a radom one.
* Run `app.py` from the repository root folder. Copy and paste **`http://0.0.0.0:5002/`** to your browser. The browser will show the map and charts in **about 7 seconds** after loading data from the database, and show 
* **Number of tweets** in a period of time, 
* The users **followers numbers**, 
* **Tweets content** when used garyvee hashtag, 
* which **states** the tweets came from if the user's location is set on, and
* User **nearby location** on an map if the user's location is set "on". 

The number of tweets in timestamp charts will show once tweets collected from more than one hour. The `app.py` script will load less than 10 tweets if any tweets has been collected at the monent of starting the script. Otherwise, the script will load an example file data.json to show gary related tweets collected previously. **If you tereminate `app.py` by `Ctrl + C` and re-run `app.py`, done't forget clear the cache of your browser before re-run**. 

## Reference
This project is inspired by:

https://github.com/dataquestio/twitter-scrape

https://github.com/adilmoujahid/kaggle-talkingdata-visualization/blob/master/README.md

**This YouTube video explain why I collected GaryVee Tweets**

<a href="http://www.youtube.com/watch?feature=player_embedded&v=Wlyqd4EMWY8
" target="_blank"><img src="https://img.youtube.com/vi/Wlyqd4EMWY8/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
