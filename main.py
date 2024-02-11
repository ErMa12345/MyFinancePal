from taipy import Gui
from taipy.gui import navigate, notify


from pages.home import home_md
from pages.portfolio import port_md
from pages.learn import learn_md
from pages.signin import auth_md, login
from pages.addStock import addstock_md
from pages.nyun import pager
from pages.explore import explore_md

root_md = """
# MyFinancePal
<|menu|label=Menu|lov={[('port', 'HOME'), ('ana', 'ANAYLSIS'),  ('whatif', 'WHAT IF'), ('explore', 'EXPLORE'), ('learn', 'LEARN'), ('auth', 'AUTH')]}|on_action=on_menu|>
"""


def on_menu(state, action, info):
    page = info["args"][0]
    if state.login == "":
        notify(state, "warning", "Please sign in!")
        navigate(state, to="auth")
    else:
        navigate(state, to=page)
    

pages = {
    "/" : root_md,
    "ana": home_md,
    "port": port_md,
    "learn" : learn_md,
    "auth" : auth_md,
    "whatif" : addstock_md,
    "test" : pager,
    "explore" : explore_md
}
    

if __name__ == "__main__":
    gui = Gui(pages=pages, css_file="styles.css")
    dynamic_content = gui.add_partial('')
    gui.run(use_reloader=True, port=5012, title="MyFinancePal")
