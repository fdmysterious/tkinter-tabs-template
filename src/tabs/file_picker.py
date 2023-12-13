from tkinter.ttk import (
    Frame,
    Label,
)

import tkinter as tk

from widgets.file_picker import FilePicker 

NAME    = "File picker tab"
obj_tab = None

async def build(tabs):
    global obj_tab
    
    obj_tab = Frame(tabs)
    obj_tab.grid(row=0, column=0, sticky="nwse", ipadx=10, ipady=10)
    tabs.add(obj_tab, text=NAME)

    obj_open_picker = FilePicker(obj_tab, "Pick open file", FilePicker.Type.Open)
    obj_open_picker.frame.pack(expand=True, fill=tk.X)

    obj_save_picker = FilePicker(obj_tab, "Pick save file", FilePicker.Type.Save)
    obj_save_picker.frame.pack(expand=True, fill=tk.X)

    obj_dir_picker = FilePicker(obj_tab, "Pick directory", FilePicker.Type.Directory)
    obj_dir_picker.frame.pack(expand=True, fill=tk.X)
