import taipy.gui.builder as tgb
from taipy.gui import notify
import tools.basicfncs
import tools.commonData
import tools.ticketToSector
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
    tgb.button("Add" , on_action='on_button_action')
    tgb.html("br")
    tgb.table("{tableData}", rebuild=True)
    tgb.chart("{data}", type="pie", values="Value", labels="Sectors")

    tgb.part(partial='{dynamic_content}')
    


def on_button_action(state):
    if isValidTicker(state.ticker):
        userData = dbOperations.find_document({"login" : state.login})
        if userData == -1:
            dbOperations.insert_document({"login" : state.login, "data" : {}})
            userData = {}
        else:
            if state.ticker in userData["data"]:
                userData["data"][state.ticker] += int(state.numOf)
                notify(state, 'success', f"Updated {state.ticker} in your portfolio")
            else:
                userData["data"][state.ticker] = int(state.numOf)
                notify(state, 'success', "Added new stock to you portfolio!")
            dbOperations.update_document({"login" : state.login}, userData)
            tools.commonData.userDataGlob = userData["data"]

        test = tools.basicfncs.portfolio_beta_variance(tools.basicfncs.generate_portfolio(tools.commonData.userDataGlob))
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
            check = tools.ticketToSector.getPortfolioInfo(tools.commonData.userDataGlob)
            print(check)
            if check["success"] == True:
                state.data = check["data"]
        state.dynamic_content.update_content(state, bro)
    else:
        notify(state, "error", f"{state.ticker} is not a valid ticker")

