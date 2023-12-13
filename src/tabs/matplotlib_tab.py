from tkinter.ttk import (
    Frame,
    Label,
    Scale
)

import tkinter as tk

from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from matplotlib.figure import Figure

import numpy as np

#############################################

# Settings
NAME = "Matplotlib test"

# Global objects
obj_tab = None

async def build(tabs):
    global obj_tab

    obj_tab = Frame(tabs)
    obj_tab.grid(row=0, column=0, sticky="nwse", ipadx=10, ipady=10)
    tabs.add(obj_tab, text=NAME)

    # Create figure
    fig   = Figure(figsize=(5,4), dpi=100)
    t     = np.arange(0, 3, .01)
    ax    = fig.add_subplot()
    line, = ax.plot(t, 2*np.sin(2*np.pi*t))
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("f(t)"    )

    canvas = FigureCanvasTkAgg(fig, master=obj_tab)
    canvas.draw()

    toolbar= NavigationToolbar2Tk(canvas, obj_tab, pack_toolbar=False)
    toolbar.update()


    canvas.mpl_connect("key_press_event", lambda ev: print(f"you pressed {ev.key}"))
    canvas.mpl_connect("key_press_event", key_press_handler)

    def update_freq(new):
        f = float(new)
        y = 2*np.sin(2*np.pi*f*t)
        line.set_data(t, y)

        canvas.draw()

    freq_slider = Scale(obj_tab, from_=1, to=5, orient=tk.HORIZONTAL, command=update_freq)

    ####

    freq_slider.pack(side=tk.BOTTOM)
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

