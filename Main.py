from __future__ import division
import Tkinter as tk

import Widgets as wg
import Inputs as ip


class MainWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="grey")
        self.parent = parent
        self.parent.title("Calculator")

        self.displays_frame = tk.Frame(parent, background="grey")
        self.displays_frame.grid(padx=10, pady=10)

        self.buttons_frame = tk.Frame(parent, background="grey")
        self.buttons_frame.grid()

        self.button = wg.Widgets()
        self.button.make_buttons(self.buttons_frame)
        self.button.make_displays(self.displays_frame)

        self.input = ip.Inputs(self.button)
        self.focus()

        print "this is contents of Entry: %r" % self.button.entry_box.get()


    def take_inputs(self):

        # Setting bindings so that only have one keyboard binding active at a time
        # Otherwise get two of each entry when inserting directly into the Entry box
        # Bound Key and Shift+Key separately to avoid inserting eg (9 or *8
        self.make_binding = self.parent.bind("<Key>", lambda event: self.button.keyboard(event))
        self.make_binding2 = self.parent.bind("<Shift-Key>", lambda event: self.button.keyboard(event))
        #print "bound to keyboard"
        if self.parent.focus_get() != self.parent:
            self.parent.unbind("<Key>", self.make_binding)
            self.parent.unbind("<Shift-Key>", self.make_binding2)
            #print "unbound"

        # This is where the actual button press is processed
        if self.button.button_go is True:
            self.input.process_input()
            self.button.button_go = False
            if self.parent.focus_get() == self.button.result:  # Returns the focus to root after using move buttons
                self.parent.focus_set()
            print "take_inputs finished"
        self.after(100, self.take_inputs)


def main():
    root = tk.Tk()
    print "main %r" % root
    app = MainWindow(root)
    root.configure(background="grey")
    root.resizable(tk.FALSE, tk.FALSE)
    root.focus_set()
    app.take_inputs()
    print "main, now starting mainloop?"
    root.mainloop()
    print "finished"


if __name__ == '__main__':
    main()

