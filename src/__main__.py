from   tkinter     import Tk, Text, TclError

import tkinter     as tk
import tkinter.ttk as ttk

import asyncio

from pathlib import Path
from logging import Handler, Formatter, getLogger, DEBUG, basicConfig

import sys

import tabs


class ScrolledText(Text):
    # From tkinter.scrolledtext module, tuned to use ttk.Scrollbar

    def __init__(self, master=None, **kw):
        self.frame = ttk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)

        kw.update({'yscrollcommand': self.vbar.set})
        Text.__init__(self, self.frame, **kw)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(tk.Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)


class TtkLogHandler(Handler):
    def __init__(self, text_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_widget = text_widget

    def emit(self, record):
        log_message = self.format(record)
        self.text_widget.insert('end', log_message + "\n")
        self.text_widget.see(tk.END)

###############################

async def build_main_win(root):
    frame    = ttk.Frame(root)
    frame.pack(expand=1, fill="both")

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=4)
    frame.rowconfigure(1, weight=1)


    # Build log
    log_widget = ScrolledText(frame, height = 15, width = 100)
    log_widget.bind("<Key>", lambda e: "break")
    log_widget.grid(row=1,column=0, sticky="nwse")


    # Add log formatter and handler
    log_formatter = Formatter('%(asctime)s - %(levelname)10s - %(message)s')
    log_handler   = TtkLogHandler(log_widget, level=DEBUG)
    log_handler.setFormatter(log_formatter)

    getLogger().addHandler(log_handler)

    # Add tabs
    tabs_obj = ttk.Notebook(frame)

    await tabs.hello_tab.build(tabs_obj)
    await tabs.matplotlib_tab.build(tabs_obj)
    await tabs.file_picker.build(tabs_obj)

    tabs_obj.grid(row=0, column=0, sticky="NWSE")


async def mainloop(root):
    is_running = True
    while is_running:
        root.update()
        await asyncio.sleep(1.0/25.0)

        # Try to call winfo: will fail if window is destroyed
        try:
            root.winfo_exists()
        except TclError:
            is_running = False


async def hello_worker():
    log = getLogger("hello_task")
    while True:
        log.info("hello world!")
        await asyncio.sleep(1)

async def main():
    # Current source path
    cwd      = (Path(__file__) / "..").resolve()
    res_path = cwd / "res"

    # Create the main window
    root = Tk()
    root.title("This is test")

    # Load the color theme
    root.tk.eval(f"source {res_path}/colorutils.tcl")
    root.tk.eval(f"source {res_path}/awthemes.tcl"  )
    root.tk.eval(f"source {res_path}/awdark.tcl"    )
    root.resizable(True,True)

    style = ttk.Style(root)
    style.theme_use("awdark")

    ###################

    await build_main_win(root)

    ###################

    hello_task = asyncio.create_task(hello_worker())
    await mainloop(root)
    hello_task.cancel()


if __name__ == "__main__":
    basicConfig(level=DEBUG)
    asyncio.run(main())
