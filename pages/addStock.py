from taipy.gui import notify
from taipy.gui import Markdown
from tools import dbOperations
import tools.commonData

ticker = ""
numOf = 0
addstock_md = Markdown("""
Stock Ticker: <|{ticker}|input|>
                   
Price:  <|{numOf}|input|>
                   
<|Add|button|on_action=on_button_action|>
""")

def on_button_action(state):
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
