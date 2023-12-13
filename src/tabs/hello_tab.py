from tkinter.ttk import (
    Frame,
    Label,
)


# Settings
NAME = "Hello tab"

# Global objects
obj_tab = None


async def build(tabs):
    global obj_tab

    obj_tab = Frame(tabs)
    obj_tab.grid(row=0, column=0, sticky="nwse")
    tabs.add(obj_tab, text=NAME)

    obj_label = Label(obj_tab, text="Hello world!")
    obj_label.pack(expand=True)
