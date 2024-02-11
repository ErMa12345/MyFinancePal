import taipy.gui.builder as tgb
from taipy.gui import notify
import tools.basicfns
import tools.commonData
import tools.tickerToSector

emaRound = 3

var = 0
beta = 0
rsqred = 0

tableData = {}
with tgb.Page() as ana_md:

    tgb.text("Portfolio Variance: {var}", raw=True, hover_text="The Portfolio Variance is a measure of a portfolio’s overall risk. It uses the weights and variances of each stock in a portfolio as well as the co-variances between every pair. A lower variance signifies either a volatile or a non-diverse portfolio.")
    tgb.text("Portfolio Beta: {beta}", raw=True, hover_text="The Beta value measures the amount of risk or volatility a stock or portfolio has relative to the entire stock market, in this case, the S&P 500 tracker VOO. For example, a stock with a beta value of 1.5 is approximately 1.5 times more volatile than the market. ")
    tgb.text("Portfolio R^2: {rsqred}", raw=True, hover_text="The Portfolio R-squared value represents the percentage of a portfolio that can be explained by movements in a benchmark index. In this case, we are comparing the portfolio to the S&P 500 tracker $VOO. A value close to 1 represents a very diverse, yet generic portfolio while a low R^2 value suggests a non-diverse portfolio.")
    tgb.html("br")
    tgb.button("Add" , on_action='on_button_action')
    tgb.table("{tableData}", rebuild=True, hover_text="The covariance between two stocks is calculated by analyzing similarities in the movement of the stocks over the past year.")


def on_button_action(state):
    state.var, state.beta, state.rsqred = tools.basicfns.get_analysis_data(tools.basicfns.generate_portfolio(tools.commonData.userDataGlob))
    state.var = round(state.var,emaRound)
    state.beta = round(state.beta,emaRound)
    state.rsqred = round(state.rsqred,emaRound)
    tableStuff = tools.basicfns.find_high_covariance_pairs(tools.basicfns.generate_portfolio(tools.commonData.userDataGlob),0.1)
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