from taipy.gui import Markdown

text = "Welcome to the Taipy multi-page tutorial app!"

learn_md = Markdown("""
## What do these numbers mean?

<|{text}|>
""")