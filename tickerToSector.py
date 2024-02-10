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

#translate portfolio into total invested into different sectors
def getPortfolioInfo(portfolio):
    sectors = {}
    for i in portfolio:
        curTick = yahooFinance.Ticker(i[0])
        curSector = curTick.info['sector']
        curSector = condensedDic.get(curSector)
        data = curTick.history()
        last_quote = data['Close'].iloc[-1]
        price = last_quote
        if curSector in sectors:
            sectors[curSector] = sectors[curSector] + price
        else:
            sectors[curSector] = price
    sectorsArr  = []
    moneys = []
    for sec,sum in sectors.items():
        sectorsArr.append(sec)
        moneys.append(sum)
    finalDict = {"Sectors":sectorsArr, "Moneys":moneys}
    return finalDict

#Testing
dummyPort = [('JPM', 2), ('META', 3), ('MSFT', 20)]
print(getPortfolioInfo(dummyPort))






