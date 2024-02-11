from taipy.gui import notify
from taipy.gui import Markdown
from tools import dbOperations
import tools.commonData

user = ""
pas = ""
login = ""

auth_md = Markdown("""
Username: 
                   
<|{user}|input|>
                   
Password:  

<|{pas}|input|password=True|>
                   

<|Create/Sign in|button|on_action=on_button_action|>
""")

def on_button_action(state):
    state.login = state.user + ":" + state.pas
    userData = dbOperations.find_document({"login" : state.login})
    if userData == -1:
        dbOperations.insert_document({"login" : state.login, "data" : {}})
        notify(state, 'success', "Created a new account")
        userData = {}
    else:
        userData = userData["data"]
        notify(state, 'success', f"Welcome back {state.user}!")
    tools.commonData.userDataGlob = userData

