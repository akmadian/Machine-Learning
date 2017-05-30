# Machine-Learning
An extention of the Stock Monitor project, meant to predict whether or not the next scraped stock value will be higher, lower, or the same.
Python Version - 3.6
Dependencies:
 - lxml
 - requests
 ___

COMMODITIES Directory
 - Contains subdirectories for unit tests, get values, and predict value scripts

RANDOM Directory
 - Same as COMMODITIES
  
scrape.py
 - Main scrape script
 
test.py
 - Used for testing small chunks of code
 
NASDAQ_AMZN.py
 - Scrapes Amazon stock data
 
RANDOM.csv
 - Product of a modified scrape.py, instead of scraping values, generates a random integer in place of the value.
