import taipy.gui.builder as tgb
from taipy.gui import notify
import tools.basicfns
import tools.commonData
import tools.tickerToSector
from tools import dbOperations
import yfinance


def isValidTicker(ticker):
    ret = True

    try:
        tick = yfinance.Ticker(ticker)
        info = tick.info['sector']
    except:
        ret = False
    return ret

data = {
    "Sectors" : ["NoData"],
    "Value" : [1]
}
tableData = {}
ticker = ""
numOf = 0
with tgb.Page() as port_md:
    tgb.input("{ticker}",label="Ticker: ", hover_text="Ticker symbol of stock to buy")
    tgb.html("br")
    tgb.input("{numOf}",label="Amount: ", hover_text="How much stock did you buy")
    tgb.html("br")
    tgb.button("Add/Remove" , on_action='on_button_action')
    tgb.button("Generate Portfolio" , on_action='on_gen_button_action')
    tgb.html("br")
    tgb.table("{tableData}", rebuild=True, hover_text="The Variance is a measure of a stock's overall risk. It uses the mean and standard deviations of the stock price each trading day over the past 1 year. A higher variance represents a more risky and volatile stock. \n The Beta value measures the amount of risk or volatility a stock or portfolio has relative to the entire stock market, in this case, the S&P 500 tracker VOO. For example, a stock with a beta value of 1.5 is approximately 1.5 times more volatile than the market. ")
    tgb.chart("{data}", type="pie", values="Value", labels="Sectors")

    tgb.part(partial='{dynamic_content}')
    
def on_gen_button_action(state):
    userData = dbOperations.find_document({"login" : state.login})
    if userData == -1:
        dbOperations.insert_document({"login" : state.login, "data" : {}})
        userData = {}
    else:
        tools.commonData.userDataGlob = userData["data"]

    test = tools.basicfns.beta_variances(tools.basicfns.generate_portfolio(tools.commonData.userDataGlob))
    bro = ""
    tableDataR = {
        "Tickers" : [],
        "Percentage" : [],
        "Beta" : [],
        "Variance" : []
    }
    for i in test:
        tableDataR["Tickers"].append(i)
        tableDataR["Percentage"].append(test[i][0])
        tableDataR["Beta"].append(test[i][1])
        tableDataR["Variance"].append(test[i][2])
    
    state.tableData = tableDataR
    if len(tools.commonData.userDataGlob) != 0:
        check = tools.tickerToSector.getPortfolioInfo(tools.commonData.userDataGlob)
        print(check)
        if check["success"] == True:
            state.data = check["data"]
    state.dynamic_content.update_content(state, bro)





def on_button_action(state):
    if isValidTicker(state.ticker):
        userData = dbOperations.find_document({"login" : state.login})
        if userData == -1:
            dbOperations.insert_document({"login" : state.login, "data" : {}})
            userData = {}
        else:
            neg = float(state.numOf) < 0
            if neg:
                toRemove = abs(float(state.numOf))
                if state.ticker in userData["data"]:
                    if toRemove < userData["data"][state.ticker]:
                        userData["data"][state.ticker] -= toRemove
                        notify(state, 'success', f"Updated {state.ticker} in your portfolio")
                    elif toRemove == userData["data"][state.ticker]:
                        del userData["data"][state.ticker]
                        notify(state, 'success', f"Removed {state.ticker} from your portfolio")
                    else:
                        notify(state, 'error', "You don't have enough stock")
                else:
                    notify(state, 'error', "You don't own this stock")
            else:
                if state.ticker in userData["data"]:
                    userData["data"][state.ticker] += float(state.numOf)
                    notify(state, 'success', f"Updated {state.ticker} in your portfolio")
                else:
                    userData["data"][state.ticker] = float(state.numOf)
                    notify(state, 'success', "Added new stock to you portfolio!")
            dbOperations.update_document({"login" : state.login}, userData)
            tools.commonData.userDataGlob = userData["data"]

        test = tools.basicfns.beta_variances(tools.basicfns.generate_portfolio(tools.commonData.userDataGlob))
        bro = ""
        tableDataR = {
            "Tickers" : [],
            "Percentage" : [],
            "Beta" : [],
            "Variance" : []
        }
        for i in test:
            tableDataR["Tickers"].append(i)
            tableDataR["Percentage"].append(test[i][0])
            tableDataR["Beta"].append(test[i][1])
            tableDataR["Variance"].append(test[i][2])
        
        state.tableData = tableDataR
        if len(tools.commonData.userDataGlob) != 0:
            check = tools.tickerToSector.getPortfolioInfo(tools.commonData.userDataGlob)
            print(check)
            if check["success"] == True:
                state.data = check["data"]
        state.dynamic_content.update_content(state, bro)
    else:
        notify(state, "error", f"{state.ticker} is not a valid ticker")

