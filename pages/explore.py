from taipy.gui import Markdown

text = "Welcome to the Taipy multi-page tutorial app!"

explore_md = Markdown("""
## What do these numbers mean?

<|{text}|>
""")