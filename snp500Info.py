import yfinance as yahooFinance
import bs4 as bs
import requests
import datetime
from datetime import datetime as dt
from tickerToSector import getSector
from basicfns import calculate_beta
import json

"""
This script gets the current s&p500 tickers, their sector, and displays the volatility risk associated with investing in it

IMPORTANT: The entire script takes like a while to run so try not to call it more than once, ideally only query database
"""


resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(resp.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})
tickers = []

#get current sp500 tickers
for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text
    tickers.append(ticker)

tickers = [s.replace('\n', '') for s in tickers]


tableToStore = {}
#get sector and individual stock voalitily risk
for curTick in tickers:
    try:
        curRow = {}
        risk = calculate_beta(curTick)
        risk = int(10*risk)
        risk = str(risk)

        sector = getSector(curTick)

        if risk in tableToStore:
            if sector in tableToStore.get(risk):
                tempArr = tableToStore.get(risk).get(sector)
                tempArr.append(curTick)
                tableToStore[risk][sector] = tempArr
            else:
                tableToStore[risk][sector] = [curTick]
        else:
            tableToStore[risk] = {sector : [curTick]}
    except:
        print("failed on", curTick)

# with open("data.json", "w") as json_file:
#     json.dump(tableToStore, json_file, indent=4)
# print("Finished proessing stocks")

from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient("mongodb+srv://ema:ZguNapUP3KZ31mlN@myfinancedata.eqaszft.mongodb.net/?retryWrites=true&w=majority")  # Update with your MongoDB connection string

# Access the database
db = client.myfinancedata  # Replace 'myfinancedata' with your database name

# Access the collection (similar to a table in relational databases)
collection = db.recommend  # Replace 'users' with your collection name

# Define the data to be inserted
user_data = tableToStore

try:
    # Insert data into the collection
    result = collection.insert_one(user_data)
    print("Data inserted successfully with id:", result.inserted_id)

except Exception as e:
    # Handle any errors that occur during insertion
    print("Error:", e)

finally:
    # Close the MongoDB connection
    client.close()
