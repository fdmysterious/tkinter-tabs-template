"""
=======================
Customized frame widget
=======================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: December 2023
"""


from tkinter.ttk import Frame as Frame_TTK

class Frame(Frame_TTK):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _state_set(self, state):
        def r_enable(widget):
            # https://stackoverflow.com/questions/51902451/how-to-enable-and-disable-frame-instead-of-individual-widgets-in-python-tkinter
            if widget.winfo_children:
                # It's a container, so iterate through its children
                for w in widget.winfo_children():
                    # change its state
                    w.state((state,))
                    # and then recurse to process ITS children
                    r_enable(w)
        r_enable(self)


    def enable(self):
        self._state_set("!disabled")

    def disable(self):
        self._state_set("disabled")
