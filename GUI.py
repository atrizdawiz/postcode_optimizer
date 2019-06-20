from tkinter import Frame, Tk, BOTH, Button, Text, Menu, END, filedialog, StringVar, Label, RAISED, PanedWindow, \
    VERTICAL, \
    Entry, LEFT, RIGHT, BOTTOM, DISABLED, NORMAL
import tkinter as tk
import os
from PostCodeOptimizer import PostCodeOptimizer

global postCodeOptimizer
postCodeOptimizer = ""


class AutoScrollbar(tk.Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 10.0:
            self.grid_remove()
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)


class Window(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        # reference to the master widget, which is the tk window
        self.parent = parent
        self.initUI()

    def initUI(self):
        # changing the title of our master widget
        self.parent.title("Postcode optimizer")
        # allowing the widget to take the full space of the root window
        global processing_frm
        processing_frm = tk.Frame(self.parent, width=1400, height=800, bg='#888888')
        input_frm = tk.Frame(processing_frm, width=600, height=600).grid(row=0, column=0)
        output_frm = tk.Frame(processing_frm, width=600, height=600).grid(row=0, column=1)

        global input_info_value
        input_info_value = StringVar()
        global input_size_label
        input_size_label = Label(output_frm, textvariable=input_info_value).grid(row=2, column=0)

        global output_info_value
        output_info_value = StringVar()

        global output_size_label
        output_size_label = Label(output_frm, textvariable=output_info_value).grid(row=2, column=3)

        global label_text
        label_text = StringVar()
        global info_label
        info_label = Label(self.parent, textvariable=label_text)
        info_label.place(relx=0.0, rely=1.0, anchor='sw')

        global input_textbox
        input_textbox = Text(input_frm, height=30, width=90)
        input_scroll = AutoScrollbar(input_frm, command=input_textbox.yview)
        input_scroll.grid(row=1, column=1, sticky='nsew')
        input_textbox.configure(yscrollcommand=input_scroll.set)
        input_textbox.grid(row=1, column=0, sticky="nsew")

        global input_label_text
        input_label_text = StringVar()
        global input_label
        input_label = Label(input_frm, textvariable=input_label_text).grid(row=0, column=0)

        global output_label_text
        output_label_text = StringVar()
        global output_label
        output_label = Label(output_frm, textvariable=output_label_text).grid(row=0, column=3)

        global input_file_path
        input_file_path = ""

        global output_textbox
        output_textbox = Text(output_frm, height=30, width=90)
        output_scroll = AutoScrollbar(output_frm, command=output_textbox.yview)
        output_scroll.grid(row=1, column=4, sticky='nsew')
        output_textbox.configure(yscrollcommand=output_scroll.set)
        output_textbox.grid(row=1, column=3, sticky='nsew')
        global optimize_button
        optimize_button = Button(self.parent, text="Optimize!", command=self.clickOptimizeButton)

        # Creating a menu instance
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        # File object of the menu is created
        fileMenu = Menu(menubar, tearoff=False)
        # Add open file command that will run the onOpen method.
        fileMenu.add_command(label="Open", command=self.onOpen)
        # Add a file button on the menu containing the fileMenu object
        menubar.add_cascade(label="File", menu=fileMenu)

    def showInfoText(self, was_success):
        if (was_success):
            info_label.configure(fg="lightgreen")
            label_text.set("File is in valid format and ready to be optimized!")

        else:
            info_label.configure(fg="red")
            label_text.set("File contains forbidden characters!")

    def clickOptimizeButton(self):
        self.processInputAndWriteOutput(self.postCodeOptimizer.input_file_path)
        print("You pressed the button!")

    def onOpen(self):
        ftypes = [('Text files', '*.txt'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        fl = dlg.show()
        if fl != '':
            self.createPostCodeOptimizerObject(fl)
            self.loadFileInput(fl)

    def loadFileInput(self, input_filename):
        input_label_text.set("Input file: " + input_filename)
        is_input_valid = self.postCodeOptimizer.is_input_valid
        if (is_input_valid):
            optimize_button.grid(row=4, column=2)
            input_textbox.delete('1.0', END)
            input_textbox.insert(tk.END, self.postCodeOptimizer.input_read)
            self.postCodeOptimizer.input_file_path = input_filename
            input_info_value.set(
                "Number of postal codes: " + str(self.postCodeOptimizer.number_of_postcodes_processed) + ".\n"
                + "File size: " + str(self.postCodeOptimizer.input_file_size) + " bytes."
            )
            self.showInfoText(is_input_valid)

    def createPostCodeOptimizerObject(self, filepath):
        self.postCodeOptimizer = PostCodeOptimizer(filepath)

    def processInputAndWriteOutput(self, input_filename):
        postal_range_string = self.postCodeOptimizer.written_output
        with open(self.postCodeOptimizer.output_file_path, 'w') as f:
            output_textbox.delete('1.0', END)
            output_textbox.insert(tk.END, postal_range_string)
            f.write(postal_range_string)
            f.close()
        output_info_value.set(
            "Number of entries: " + str(self.postCodeOptimizer.number_of_entries_in_output) + ".\n" +
            "File size: " + str(f.__sizeof__()) + " bytes."
        )
        output_label_text.set("Output file: " + self.postCodeOptimizer.output_file_path)


def main():
    root = Tk()
    app = Window(root)
    root.geometry("1600x600+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()
