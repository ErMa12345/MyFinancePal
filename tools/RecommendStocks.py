from tools.basicfns import generate_portfolio
from tools.tickerToSector import getSector
from pymongo import MongoClient
import random

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the MongoDB URI from the environment variables
mongodb_uri = os.getenv("MONGODB_URI")

dummyPort = {'SHW': 1, 'CAT': 6, 'BEN': 20, 'ET':12, 'LOW': 5, 'CSCO': 3, 'CMCSA':6, 'ABT':4, 'ABT':2, 
             'CL':4, 'ATO':9, 'ESS':3}
dummyPort2 = {'MSFT': 2, 'AMZN':3}

def giveStocks(portfolio, desiredRisk):
    uninvestedSectors = [
        'Basic Materials', #0
        'Industrials', #1
        'Consumer Goods', #2
        'Healthcare', #3
        'Financial Services', #4
        'Technology and Communication', #5
        'Real estate and utilities' #6
    ]
    weightedPort = generate_portfolio(portfolio)
    weightedSectors = {}
    for t in weightedPort:
        sector = getSector(t)
        if sector in uninvestedSectors:
            uninvestedSectors.remove(sector)
        if sector in weightedSectors:
            weightedSectors[sector] = weightedSectors[sector] + weightedPort[t]
        else:
            weightedSectors[sector] = weightedPort[t]
    

    # Connect to the MongoDB server
    client = MongoClient(mongodb_uri) 

    # Access the database
    db = client.myfinancedata  # Replace 'myfinancedata' with your database name

    # Access the collection (similar to a table in relational databases)
    collection = db.recommend  # Replace 'users' with your collection name

    cursor = list(collection.find())
    riskDict = cursor[0]
    del riskDict[list(riskDict.keys())[0]]

    possibleStocks = {}
    message = ''
    ret = {'Message':message, 'Possible Stocks':possibleStocks}
    if len(uninvestedSectors) > 0:
        uninvested = ""
        for i in range(len(uninvestedSectors)):
            if i == len(uninvestedSectors) - 1:
                uninvested += "and " + uninvestedSectors[i] + "."
            else:
                uninvested += uninvestedSectors[i] + ", "
        message = "It seems your portfolio is not as diversified as it could be, here are some stocks and their associated risk that you could look into in the following industries: " + uninvested
        for risk in riskDict:
            if int(risk) <= desiredRisk:
                for sector in riskDict[str(risk)]:
                    if sector in uninvestedSectors:
                        if risk in possibleStocks:
                            possibleStocks[risk] = possibleStocks[risk] + (riskDict[risk][sector])
                        else:
                            possibleStocks[risk] = riskDict[risk][sector]
    else:
        minWeight = min(weightedSectors, key=weightedSectors.get)
        message = "Your portfolio is pretty diverse, but there might be some minor imbalances as you don't have much in " + minWeight + ", here are some recommendations and their risk level!"
        for risk in riskDict:
            if int(risk) <= desiredRisk:
                for sector in riskDict[str(risk)]:
                    if sector == minWeight:
                        if risk in possibleStocks:
                            possibleStocks[risk] = possibleStocks[risk] + (riskDict[risk][sector])
                        else:
                            possibleStocks[risk] = riskDict[risk][sector]

    for i in possibleStocks:
        if (len(possibleStocks[i]) > 3):
            option1, option2, option3 = random.sample(range(0, len(possibleStocks[i])), 3)
            tempArr = [possibleStocks[i][option1], possibleStocks[i][option2],possibleStocks[i][option3]]
            possibleStocks[i] = tempArr
    possibleStocks = sorted(possibleStocks.items())
    ret['Message'] = message
    ret['Possible Stocks'] = possibleStocks
    return ret
    
if __name__ == "__main__":
    print(giveStocks(dummyPort2, 3))