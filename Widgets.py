import Tkinter as tk
import re as re


class Widgets(object):

    def __init__(self):
        self.equals_was_last_key_pressed = None
        self.buttons = ["0", ".", "x10^", "ANS", "=",
                        "1", "2", "3", "+", "-",
                        "4", "5", "6", "x", "/",
                        "7", "8", "9", "DEL", "AC",
                        "(", ")", "<", ">"
                       ]
        self.special_buttons = ["=", "DEL", "AC", "ANS", "spare", "<", ">"]
        self.digit_buttons = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.button_dict = {}
        self.keysym_guide = {"BackSpace": "DEL", "period": ".", "Return": "=", "KP_Enter": "=",
                             "plus": "+", "equal": "=", "Clear": "AC",
                             "minus": "-", "slash": "/", "e": "x10^", "E": "x10^", "a": "ANS", "A": "ANS",
                             "Left": "<", "Right": ">", "X": "x"
                             }
        self.shift_keysym_guide = {"parenright": ")", "parenleft": "(", "plus": "+"}

        self.button_pressed = tk.StringVar()
        self.button_go = False
        self.insert_is_active = None

    def make_buttons(self, buttons_frame):
        self.buttons_frame = buttons_frame
        self.c = 0
        self.r = 100 # I want them bottom to top

        self.small_frame = tk.Frame(self.buttons_frame)
        self.small_frame.grid(row=50, sticky=tk.N, columnspan=5)


        for b in self.buttons:
            if b in ("(", ")", "<", ">"):
                self.button_dict[b] = tk.Button(self.small_frame, text=b, height=2, width=4, font=("TkDefaultFont", 20))
            else:
                self.button_dict[b] = tk.Button(self.buttons_frame, text=b, height=2, width=4, font=("TkDefaultFont", 20))
            self.button_dict[b].grid(row=self.r, column=self.c)

            if b == "DEL" or b == "AC":
                self.button_dict[b].configure(bg="orange red")
            elif b == "/":
                self.button_dict[b].configure(text=u"\u00f7", bg="gray52")
            elif b == "x10^":
                self.button_dict[b].configure(text=u"x10\u207F", bg="gray52")
            elif b == "(" or b == ")":
                self.button_dict[b].configure(bg="gray")
            elif b == "<" or b == ">":
                self.button_dict[b].configure(bg="SteelBlue3")

            else:
                self.button_dict[b].configure(bg="gray52")

            self.c += 1
            if self.c == 5:
                self.c = 0
                self.r -= 1

            def make_lambda(x): #to make lambda work with for loop
                return lambda event: self.key_function(x)
            self.button_dict[b].bind("<Button-1>", make_lambda(b))


    def make_displays(self, displays_frame):
        self.displays_frame = displays_frame
        self.entry_box = tk.Entry(self.displays_frame)
        self.entry_box.configure(font=("TkDefaultFont",20))
        self.entry_box.grid(row=1, column=2, columnspan=4)

        self.result_stringvar = tk.StringVar()
        self.result = tk.Label(self.displays_frame, textvariable=self.result_stringvar, anchor=tk.E, width=15, background="grey",
                               font=("TkDefaultFont", 20))
        self.result.grid(row=2, column=2, columnspan=4)

        self.entry_box.bind("<Button-1>", lambda event: self.entry_click())
        self.entry_box.bind("<Key>", lambda event: self.keyboard(event))
        self.entry_box.bind("<Shift-Key>", lambda event: self.keyboard(event))

    def key_function(self, label):
        self.label = label
        self.button_pressed.set(self.label)
        #print "button pressed is: %r, self.label is: %r" % (self.button_pressed.get(), self.label)
        self.button_pressed.set(label)
        self.button_go = True  # NB this is not the same buttons_go as in init?


    def keyboard(self,event):
        self.keyboard_input = event.keysym
        print "keyboard_input %r" % self.keyboard_input
        if self.keyboard_input in self.button_dict:
            self.key_function(self.keyboard_input)
            return "break"
        elif self.keyboard_input in self.keysym_guide:
            self.key_function(self.keysym_guide[self.keyboard_input])
            return "break"
        elif self.keyboard_input in self.shift_keysym_guide:
            self.key_function(self.shift_keysym_guide[self.keyboard_input])
            return "break"
        elif self.keyboard_input == "asterisk":
            self.key_function("x")
            return "break"
        else:
            print "unsuitable keyboard event"
            return "break"


    def entry_click(self):
        print "click in the box"
        self.entry_box.focus_set()
        if self.equals_was_last_key_pressed is True:
            self.entry_box.delete(0, tk.END)


    def check_for_error(self, key):
        #key is button_pressed for buttons, and event.keysym for keyboard Entry
        self.key = key
        self.unwanted_pairs = ["..", "xx", "//", "x10^x10^", "SANS",
                          ".x", "./", ".x10^", ".)", ".(", ").", ".ANS", "ANS.",
                          "x/", "/x", "x)", "(x", "xx10^", "x10^x", "-x", "+x",
                          "/x10^", "/)", "(/", "x10^/", "()", "+/", "-/",
                          "-x10^", "+x10^", "-)", "+)", "(x10^", ")x10^",
                          "Nonex", "None/", "None)", ".+", ".-"
                                ]
        self.number_has_dot = re.compile(r"""
                                \d* # 0 or more digits
                                \. # escaped dot
                                \d+ # 1 or more digits
                                $ # end of the line
                                """, re.VERBOSE)
        self.function_characters = ["x", "/", "+", "-", "^"]

        self.most_recent_in_entrybox = self.entry_box.get()
        print "most recent in entrybox is : %r" % self.most_recent_in_entrybox

        if self.key in self.buttons:
            self.key = self.key
        elif self.key in self.keysym_guide:
            self.key = self.keysym_guide[self.key]
        elif self.key in self.shift_keysym_guide:
            self.key = self.shift_keysym_guide[self.key]
        else:
            print "unsuitable key"
            return 1
        print "Widgets check_for_error, self.key is: %r" % self.key
        print len(self.most_recent_in_entrybox)

        if len(self.most_recent_in_entrybox) == 0 and (self.equals_was_last_key_pressed is not True):
            if ("None" + self.key) in self.unwanted_pairs:
                print "inappropriate button choice at beginning of entry_box"
                return 1
            else:
                return 0
        elif len(self.most_recent_in_entrybox) > 0:
            print self.most_recent_in_entrybox[-1] + self.key
            if self.most_recent_in_entrybox[-1] + str(self.key) in self.unwanted_pairs:
                print "unwanted pair of functions"
                return 1
            elif (self.most_recent_in_entrybox[-1] == "S") and (self.key in self.digit_buttons):
                print "no digits after ANS"
                return 1
            elif (self.most_recent_in_entrybox[-1] in self.digit_buttons) and (self.key == "ANS") \
                    and (self.equals_was_last_key_pressed is not True):
                print "no ANS immediately after digit"
                return 1
            elif ((self.most_recent_in_entrybox[-2:] == "--") or (self.most_recent_in_entrybox[-2:] == "++")) \
                    and (self.key == "-" or self.key == "+"):
                print "too many -- or ++ in a row"
                return 1
            elif (re.search(self.number_has_dot, self.most_recent_in_entrybox) != None) and self.key == ".":
                print "two dots error"
                return 1
            elif ("(" not in self.most_recent_in_entrybox) and self.key == ")":
                print "closing bracket before opening error"
                return 1
            elif (self.most_recent_in_entrybox[-1] in self.function_characters) and self.key == "=":
                print "function at the end of the line"
                return 1
            elif self.equals_was_last_key_pressed is True and self.key == "=":
                self.function_in_box = filter(lambda x: x in self.most_recent_in_entrybox, self.function_characters)
                if len(self.function_in_box)>0:
                    print "doing ANS sums, = and = is ok"
                    return 0
                else:
                    print "don't do = and ="
                    return 1

            else:
                return 0
        else:
            return 0