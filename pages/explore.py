import taipy.gui.builder as tgb
from taipy.gui import notify
import tools.basicfns
import tools.commonData
import tools.tickerToSector
import tools.RecommendStocks

emaround = 3

newStock = ""
index = ""
rsqrd = 0
old = 0
new = 0
beta10 = 0
beta20 = 0
risk = 5
message = ""
tableData = {}
with tgb.Page() as explore_md:

    
    tgb.html("h3","Enter your risk level:")
    tgb.slider("{risk}",min=0,max=9)
    tgb.button("Add" , on_action='on_button_action')
    tgb.text("{message}", raw=True)
    tgb.table("{tableData}", rebuild=True)
    tgb.html("br")
    tgb.html("h2","Substituting a stock with a Index Fund")
    tgb.text("Scenario: Replace {newStock} with the index fund {index}", raw=True)
    tgb.text("R^2 between {newStock} and {index} : {rsqrd}", raw=True, hover_text="The R-squared value represents the percentage of a portfolio that can be explained by movements in a benchmark index. In this case, we are comparing the portfolio to the index fund associated with the sector of the stock. A value close to 1 indicates that the stock moves very cloesly with the index fund.")
    tgb.text("Portfolio variance will change from {old} to {new}", raw=True, hover_text="The Portfolio Variance is a measure of a portfolio’s overall risk. It uses the weights and variances of each stock in a portfolio as well as the co-variances between every pair. A lower variance signifies either a volatile or a non-diverse portfolio.")
    tgb.text("Stock Beta Value: {beta10}", raw=True,  hover_text="The Beta value measures the amount of risk or volatility a stock or portfolio has relative to the entire stock market, in this case, the S&P 500 tracker VOO. For example, a stock with a beta value of 1.5 is approximately 1.5 times more volatile than the market. ")
    tgb.text("Index Beta Value: {beta20}", raw=True,  hover_text="The Beta value measures the amount of risk or volatility a stock or portfolio has relative to the entire stock market, in this case, the S&P 500 tracker VOO. For example, a stock with a beta value of 1.5 is approximately 1.5 times more volatile than the market. ")
    tgb.html("br")
    tgb.html("br")
    tgb.html("br")
   


def on_button_action(state):
    dhruvTuple = tools.basicfns.suggestIndex(tools.basicfns.generate_portfolio(tools.commonData.userDataGlob))
    state.newStock, state.index, state.rsqrd, state.old, state.new, state.beta10,state.beta20 = dhruvTuple
    state.rsqrd = round(state.rsqrd, emaround)
    state.old = round(state.old, emaround)
    state.new = round(state.new, emaround)
    state.beta10 = round(state.beta10, emaround)
    state.beta20 = round(state.beta20, emaround)

    ema = tools.RecommendStocks.giveStocks(tools.commonData.userDataGlob,state.risk)
    print(ema)
    state.message = ema["Message"]
    tableDataR = {
            "Risk Level" : [],
            "Stocks" : [],
        }
    for i in ema["Possible Stocks"]:
        tableDataR["Risk Level"].append(i[0])
        tableDataR["Stocks"].append(str(i[1]))
    
    state.tableData = tableDataR
    return
    tableStuff = (tools.basicfns.generate_portfolio(tools.commonData.userDataGlob),)
    tableDataR = {
            "Stock 1" : [],
            "Stock 2" : [],
            "Co-variance" : []
        }
    
    for i in tableStuff:
        tableDataR["Stock 1"].append(i[0])
        tableDataR["Stock 2"].append(i[1])
        tableDataR["Co-variance"].append(i[2])
    
    state.tableData = tableDataR