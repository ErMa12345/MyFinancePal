import taipy.gui.builder as tgb

input_name = "Taipy"
message = None
bro = ""

with tgb.Page() as pager:
    tgb.input("{input_name}")
    tgb.text("{message}")
    tgb.button("add" , on_action='add_element')
    tgb.part(partial='{dynamic_content}')



def add_element(state):
    global bro
    bro += "<|input|> \n\n"
    state.dynamic_content.update_content(state, bro)
    


