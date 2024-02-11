from taipy.gui import notify
from taipy.gui import Markdown
import tools.commonData
from tools.emotionDetection import EmotionalRiskCalculator
from tools.llmScore import score_response


dataWI = {
    "X" : ["Not Loaded"],
    "Y" : [1]
}

tickerWI = ""
amountWI = 0
answerWI = ""
gptResponse = ""
score = 0
whatif_md = Markdown("""
<|{tickerWI}|input|label=Ticker|>
<|{amountWI}|input|label=Amount of Stock|>


                     
How do you typically approach investment decisions and can you provide an example of why you invested in a certain stock?    
<|{answerWI}|input|multiline=True|id=eddy|>
                   
                   
<|Add|button|on_action=on_button_action|>

<|{dataWI}|chart|type=pie|labels=X|values=Y|>

## Well-developed Thesis Score: <|{score}|text|raw|>               
<|{gptResponse}|>
""")

def on_button_action(state):
    bro = EmotionalRiskCalculator()
    state.score = bro.process_free_response_question(state.answerWI) # number
    dataWIR = {
        "X" : ["Informative", "Emotional"],
        "Y" : [0,0]
    }
    dataWIR["Y"][0] = state.score
    dataWIR["Y"][1] = 100 - state.score
    state.dataWI = dataWIR
    print(state.dataWI["Y"][0], state.dataWI["Y"][1])
    state.gptResponse = score_response(state.answerWI) # more detail
    
