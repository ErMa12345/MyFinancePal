from taipy.gui import notify
from taipy.gui import Markdown
import tools.ticketToSector
import tools.basicfncs


data = {
    "Sectors" : ["Loading"],
    "Value" : [1]
}


doSlider = 0
wantSlider = 0
num = 0

text = ""
home_md = Markdown("""
How much risk do you tend to take: 

<|{doSlider}|slider|min=0|max=10|>

How much risk do you want to take:

<|{wantSlider}|slider|min=0|max=10|>

<|{num}|>

<|Calculate|button|on_action=on_button_action|>

<|{data}|chart|type=pie|values=Value|labels=Sectors|> Does this work

<|{text}|input|>
                   

                   


""")



def on_button_action(state):
    notify(state, 'success', f'Calculated new data!')

def on_change(state, var_name, var_value):
    print(var_name, var_value)
    if var_name == "text" and var_value == "Reset":
        state.text = ""
        return
    
    if var_name == "doSlider" or var_name == "wantSlider":
        print(state.doSlider, state.wantSlider)
        return

def on_slider_change(state):
    #notify(state, 'success', f'Slider was changed {state}')
    pass