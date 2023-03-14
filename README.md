# twitterData
**twitterData** is a data web app for the non-tech-savvy.  It consists of a simple search engine, which uses the twitter API to return datasets on the basis of the keyword & number of tweets requested by the user.

Users must simply register to create an account and may then use the twitterData search engine, see their history under the MyData tab, as well as download their SQL database in .csv format.

You can run the app by followng the steps below.

#### Tech used:
1. Python (Flask)
2. SQLite
3. HTML/CSS

## Installation:
```
pip install -r requirements.txt
```

## Main files and folders:
- app.py : contains routes for authentication (registration, log in, log out), search results and data downloads
- helpers.py : contains functions to connect to Twitter API, return the tweet variables needed, require the user to be logged in, return errors
- templates/ : all HTML forms used in the app (page layout, registration, log in, results page, myData page)

## Twitter API:
To run the app, you must gain access to the Twitter API ([here's how](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)).

Then, you should create a file called 'config.py' (or whatever suits you) inside the app folder and store the API keys and tokens:

```
API_key_public          = "Your_API_key_public"
API_key_Secret          = "Your_API_key_Secret"
Bearer_Token            = "Your_Bearer_Token"
Access_token            = "Your_Access_token"
Access_token_secret     = "Your_Access_token_secret"
```
As your API keys are secret, it is **very important** to hide it within .gitignore. To do this, type `code .gitignore` in the terminal and then type `config.py` within the .gitignore file. Close .gitignore

## SQL databse:
Create a database by typing `code final.db` in the terminal and then launch sqlite3 by typing `sqlite3 final.db`. twitterData uses two tables within the final database:

- users : user id, username and hash password
- u_db : search results table, delivering the relevant twitter data searched by each user

The initial schema to be typed within sqlite3 is the following:
```
CREATE TABLE users (username TEXT NOT NULL, hash TEXT NOT NULL, 'id' INTEGER PRIMARY KEY NOT NULL );
```
```
CREATE TABLE u_db (id INTEGER, username TEXT NOT NULL, user_description TEXT, tweet TEXT NOT NULL
, date DATETIME, retweets INTEGER, 'keyword' TEXT, 'likes' INTEGER, 'location' TEXT, FOREIGN KEY (id) REFERENCES users);
```
You're ready to go.
   
------------
#### Credits:
The initial version of this web app was submitted as my final project for Harvard's CS50 introduction to computer science. 
I thank Professor Malan and his team for this fantastic journey and strongly recommend this course to anyone looking substantive, in-depth introduction to the art of programming. You can register [here](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x?utm_source=google&utm_campaign=19339199037&utm_medium=cpc&utm_term=harvard%20cs50%20online&hsa_acc=7245054034&hsa_cam=19339199037&hsa_grp=145482383700&hsa_ad=642397268536&hsa_src=g&hsa_tgt=kwd-422823376443&hsa_kw=harvard%20cs50%20online&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gclid=CjwKCAiA3pugBhAwEiwAWFzwdVAWQLlh0fnX2npfXVe9L4TC4F7ls9-qmu0vqTjW8oj0ev27RWzasBoCWHEQAvD_BwE).