import yfinance as yahooFinance

condensedSectors = [
'Basic Materials', #0
'Industrials', #1
'Consumer Goods', #2
'Healthcare', #3
'Financial Services', #4
'Technology and Communication', #5
'Real estate and utilities' #6
]

#condense 11 sectors into 7 more basic ones
condensedDic = {'Financial Services': condensedSectors[4],
                    'Technology': condensedSectors[5],
                    'Healthcare' : condensedSectors[3],
                    'Consumer Cyclical': condensedSectors[2],
                    'Industrials': condensedSectors[1],
                    'Communication Services': condensedSectors[5],
                    'Consumer Defensive': condensedSectors[2],
                    'Energy': condensedSectors[0],
                    'Basic Materials': condensedSectors[0],
                    'Real Estate': condensedSectors[6],
                    'Utilities': condensedSectors[6]
                    }

#get sector of given ticker
def getSector(ticker):
    ticker = yahooFinance.Ticker(ticker)
    sector = ticker.info['sector']
    sector = condensedDic.get(sector)
    return sector

#translate portfolio into total invested into different sectors
def getPortfolioInfo(portfolio):
    result = {"success" : True, "data": {}, "error": ""}
    sectors = {}
    for i in portfolio:
        try:
            if portfolio[i] < 0:
                result["success"] = False
                result["error"] = "Invalid stock amount entered"
                return result
            curTick = yahooFinance.Ticker(i)
            curSector = curTick.info['sector']
            curSector = condensedDic.get(curSector)
            data = curTick.history()
            last_quote = data['Close'].iloc[-1]
            price = last_quote
            if curSector in sectors:
                sectors[curSector] = sectors[curSector] + price * portfolio[i]
            else:
                sectors[curSector] = price * portfolio[i]
        except:
            result["success"] = False
            result["error"] = i + " is not a ticker"
            return result
    sectorsArr  = []
    moneys = []
    for sec,sum in sectors.items():
        sectorsArr.append(sec)
        moneys.append(sum)
    result["data"] = {"Sectors":sectorsArr, "Value":moneys}
    return result

#Testing
if __name__ == "Main":
    dummyPort = [('JPM', 2), ('META', 3), ('MSFT', 20)]
    print(getPortfolioInfo(dummyPort))