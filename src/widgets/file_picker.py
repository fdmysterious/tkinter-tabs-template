"""
==================
Simple file picker
==================

:Authors: - Florian Dupeyron
:Date: December 2023
"""

from tkinter.ttk import (
    Frame,
    LabelFrame,
    Entry,
    Button,
)

import tkinter as tk
from tkinter   import filedialog

from enum import Enum

#####################################


class FilePicker:
    class Type(Enum):
        Open         = "open"
        Save         = "save"
        Directory    = "directory"

    PICK_FUNCTIONS = {
        Type.Open:      filedialog.askopenfilename,
        Type.Save:      filedialog.asksaveasfilename,
        Type.Directory: filedialog.askdirectory,
    }

    def __init__(self, parent, label, dialog_type, command=None, **dialog_args):
        self.frame = LabelFrame(parent, text=label, padding=2)
        self.entry = Entry(self.frame)
        self.btn   = Button(self.frame, text="...", command=self.pick_file)

        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.btn.pack(side=tk.LEFT, padx=2)

        self.dialog_type = FilePicker.Type(dialog_type)
        self.dialog_args = dialog_args

        self.command     = command

        if self.command is not None:
            self.entry.bind("<Return>", lambda *args: self.command(self.entry.get()))


    def pick_file(self):
        # Call dialog function from dialog dict functions with registered arguments
        file_name = self.PICK_FUNCTIONS[self.dialog_type](**self.dialog_args)

        # Save result in entry
        self.entry.delete(0, tk.END)
        self.entry.insert(0, file_name)

        # Callback
        if self.command is not None:
            self.command(file_name)

    @property
    def value(self):
        return self.entry.get()
