from __future__ import division
import Tkinter as tk
import re as re


class Inputs(object):
    def __init__(self, widgets):
        self.widgets = widgets # this will be the actual Widgets instance
        self.final_result = False
        self.entry_focus = None
        self.error = None

    def process_input(self):

        print "this is contents of Entry: %r" % self.widgets.entry_box.get()

        # Checking whether the Entry cursor should be visible or not
        if self.widgets.entry_box.focus_get() == self.widgets.entry_box:
            self.entry_focus = True
        else:
            self.entry_focus = False

        self.error = self.widgets.check_for_error(self.widgets.button_pressed.get())
        print "process_input, error is: %r" % self.error

        print "the cursor index is: %r" % self.widgets.entry_box.index("insert")
        print "equals was last key pressed: %r" % self.widgets.equals_was_last_key_pressed

        # This is tidying up Entry and/or Label
        if self.error == 0:
            # This clears the input area after a calculation has been made
            if self.widgets.equals_was_last_key_pressed is True and self.widgets.button_pressed.get() == "=" \
                    and "ANS" in self.widgets.entry_box.get():
                print "ANS with repeated equals"
            elif self.widgets.equals_was_last_key_pressed is True and \
                            self.widgets.button_pressed.get() not in ("DEL", "<", ">"):
                print "clearing everything after = press"
                self.widgets.entry_box.delete(0, tk.END)
                self.widgets.result_stringvar.set("")
            elif self.widgets.equals_was_last_key_pressed is True:
                self.widgets.result_stringvar.set("")

        # ANS needs to know if equals_was_last_key_pressed, so can't set it to False up here


        # Normal button press:
        if (self.widgets.button_pressed.get() not in self.widgets.special_buttons) and self.error == 0:
            if (self.final_result != False) and (self.widgets.equals_was_last_key_pressed is True) \
                    and (self.widgets.button_pressed.get() not in (self.widgets.digit_buttons, "x10^", "(")):
                self.widgets.entry_box.insert(tk.INSERT, "ANS")

            self.widgets.entry_box.insert(tk.INSERT, self.widgets.button_pressed.get())
            self.widgets.equals_was_last_key_pressed = False

        # Special buttons:
        elif self.widgets.button_pressed.get() == "DEL":
            self.cursor_index = self.widgets.entry_box.index("insert")
            if len(self.widgets.entry_box.get())>0:
            # special cases for x10^ and ANS
                if self.widgets.entry_box.get()[self.cursor_index-1] == "S":
                    self.widgets.entry_box.delete(self.cursor_index-3, tk.END)
                elif self.widgets.entry_box.get()[self.cursor_index-1] == "^":
                    self.widgets.entry_box.delete(self.cursor_index-4, tk.END)
                else:
                    self.widgets.entry_box.delete(self.cursor_index-1)
                    self.widgets.equals_was_last_key_pressed = False

        elif self.widgets.button_pressed.get() == "AC":
            self.widgets.entry_box.delete(0, tk.END)
            self.widgets.equals_was_last_key_pressed = False

        elif self.widgets.button_pressed.get() == "ANS" and self.error == 0:
            if self.widgets.equals_was_last_key_pressed is True:
                self.widgets.entry_box.delete(0, tk.END)
            if self.final_result != False:
                if self.entry_focus is True:
                    self.widgets.entry_box.insert(tk.INSERT, "ANS")
                else:
                    self.widgets.entry_box.insert(tk.INSERT, "ANS")
                self.widgets.equals_was_last_key_pressed = False

        # these are for movement in the Entry box, needs caret
        elif self.widgets.button_pressed.get() == "<":
            # No visible cursor if entry_box doesn't have focus, so show the cursor first
            if self.entry_focus is not True:
                self.widgets.entry_box.focus()
                self.entry_focus = True
                #print "entry focus is %r" % self.entry_focus
            elif len(self.widgets.entry_box.get())>0:
                # set this cursor_index to wherever the cursor is right now
                self.cursor_index = self.widgets.entry_box.index("insert")
                # Jumps over ANS as if one character
                if self.widgets.entry_box.get()[self.cursor_index-1] == "S":
                    self.widgets.entry_box.icursor(self.cursor_index-3)
                elif self.widgets.entry_box.get()[self.cursor_index-1] == "^":
                    self.widgets.entry_box.icursor(self.cursor_index-4)
                else:
                    self.widgets.entry_box.icursor(self.cursor_index-1)
            self.widgets.equals_was_last_key_pressed = False

        elif self.widgets.button_pressed.get() == ">":
            if self.entry_focus is not True:
                self.widgets.entry_box.focus()
                self.entry_focus = True
            else:
                self.cursor_index = self.widgets.entry_box.index("insert")
                # To find ANS going right, need to look one in front of the cursor
                # But cursor first position is 1, not 0 like normal index
                if (self.cursor_index < len(self.widgets.entry_box.get())) \
                        and self.widgets.entry_box.get()[self.cursor_index] == "A":
                    self.widgets.entry_box.icursor(self.cursor_index+3)
                elif self.cursor_index+4 <= len(self.widgets.entry_box.get()) \
                        and self.widgets.entry_box.get()[self.cursor_index+3] == "^":
                    self.widgets.entry_box.icursor(self.cursor_index+4)
                else:
                    self.widgets.entry_box.icursor(self.cursor_index+1)
                if self.cursor_index == self.widgets.entry_box.index("end"):
                    self.widgets.result.focus() # Giving focus to Label to hide the cursor
                    self.entry_focus = False
            self.widgets.equals_was_last_key_pressed = False

        # This is the only one left so must be = press
        elif self.error == 0:
            self.widgets.equals_was_last_key_pressed = True
            try:
                self.get_answer(self.widgets.result_stringvar)
            except SyntaxError:
                print "bad syntax"
            except ZeroDivisionError:
                print "don't divide by zero!"
            except TypeError:
                print "type error"
        else:
            print "there was an error of some sort"


    def get_answer(self, printout):
        self.printout = printout # This will be the StringVar for the answer Label
        print "Inputs, this is from entry box: %r" % self.widgets.entry_box.get()
        self.from_entry_box = self.widgets.entry_box.get()

        self.widgets.result.focus()  # Giving focus to Label to hide cursor
        self.entry_focus = False
        self.widgets.entry_box.icursor(tk.END)

        self.left_bracket_without_x_symbol = re.compile(r"""
                                (\d+ # 1 or more digits
                                \.* # 0 or more escaped dots
                                \d* # 0 or more digits
                                ) # re part 1
                                (\( # escaped bracket
                                ) # re part 2
                                                """, re.X)
        self.exp_style_number = re.compile(r"""
                                (\d*\.?\d+) # 0 or more digits, 0 or 1 dot, 1 or more digits
                                e # e
                                ([+-]) # + or -
                                0? # 1 or 0 zero
                                (\d+) # 1 or more digits
                                """, re.X)
        self.pretend_superscript = {"0": u"\u2070", "1": u"\u00B9", "2": u"\u00B2", "3": u"\u00B3",
                                    "4": u"\u2074", "5": u"\u2075", "6": u"\u2076", "7": u"\u2077",
                                    "8": u"\u2078", "9": u"\u2079"}

        # Making result ready to eval
        if "ANS" in self.from_entry_box:
            self.from_entry_box = self.from_entry_box.replace("ANS", self.final_result)
        if re.match(r"(^x10\^)", self.from_entry_box) is not None:
            self.from_entry_box = re.sub(r"(^x10\^)", r"1e", self.from_entry_box)
            self.widgets.entry_box.insert(0, "1")
        self.from_entry_box = re.sub(r"x10\^", r"e", self.from_entry_box)
        # Adds a * for multiplying by a bracket if no x on left
        self.from_entry_box = re.sub(self.left_bracket_without_x_symbol, "\g<1>*\g<2>", self.from_entry_box)
        self.from_entry_box = self.from_entry_box.replace("x", "*")

        print "Inputs, final input to eval: %r" % self.from_entry_box
        try:
            self.final_result = str(eval(self.from_entry_box))

            # Prettifying the result
            self.pretty_final_result = re.sub(r"\.0$", r"", self.final_result) # removes extraneous .0 from answer
            # If entry had x10^, result should be in same format (within reason)
            # Also needs same number of decimal places
            if ("e" in self.from_entry_box) and "0.00" in self.pretty_final_result:
                self.counting_decimal_places = re.search(r"\d+\.?0*([1-9]*)", self.pretty_final_result)
                self.decimal_places = "{:." + str(len(self.counting_decimal_places.group(1))-1) + "e}"
                self.pretty_final_result = self.decimal_places.format(float(self.pretty_final_result))
            # Changing e to x10^ and adding unicode "superscript"
            if re.search(self.exp_style_number, self.pretty_final_result) is not None:
                self.looking_for_exp = re.search(self.exp_style_number, self.pretty_final_result)
                self.times_ten_to_the = []
                for i in self.looking_for_exp.group(3):
                    self.times_ten_to_the.append(self.pretend_superscript[i])
                self.times_ten_to_the_string = "".join(self.times_ten_to_the)
                if self.looking_for_exp.group(2) == "+":
                    self.pretty_final_result = self.looking_for_exp.group(1) + "x10" + self.times_ten_to_the_string
                elif self.looking_for_exp.group(2) == "-":
                    self.pretty_final_result = self.looking_for_exp.group(1) + "x10" + u"\u207b" + self.times_ten_to_the_string
                # NB pretty_final_result is unicode now, not a normal string

            self.printout.set(self.pretty_final_result)
            print "The result is %r or %r" % (self.final_result, self.pretty_final_result)
        except SyntaxError:
            print "get_answer SyntaxError"
            self.printout.set("")



