from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog, StringVar, Label, RAISED, PanedWindow, VERTICAL, \
    Entry, LEFT, RIGHT, BOTTOM
from PostCodeOptimizer import PostCodeOptimizer

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
        self.pack(fill=BOTH, expand=1)
        global label_text
        label_text = StringVar()
        global info_label
        info_label = Label(self.parent, textvariable = label_text)
        info_label.place(relx= 0.0, rely = 1.0, anchor='sw')

        # Creating a menu instance
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        #File object of the menu is created
        fileMenu = Menu(menubar, tearoff=False)
        #Add open file command that will run the onOpen method.
        fileMenu.add_command(label="Open", command=self.onOpen)
        #Add a file button on the menu containing the fileMenu object
        menubar.add_cascade(label="File", menu=fileMenu)

    def showInfoText(self, was_success):
        if(was_success):
            info_label.configure(fg="lightgreen")
            label_text.set("File has been processed!")
        else:
            info_label.configure(fg="red")
            label_text.set("File contains forbidden characters!")


    def onOpen(self):
        ftypes = [('Text files', '*.txt'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            self.readFileAndWriteOutput(fl)

    def readFileAndWriteOutput(self, input_filename):
        postCodeOptimizer = PostCodeOptimizer(input_filename)
        is_input_valid = postCodeOptimizer.validate_input(input_filename)
        if(is_input_valid):
            print("Found valid input")
            postal_dictionary = postCodeOptimizer.postal_dictionary_creator()
            postal_range_string = postCodeOptimizer.postal_range_finder(postal_dictionary)
            with open(postCodeOptimizer.output_file, 'w') as f:
                f.write(postal_range_string)
                self.showInfoText(is_input_valid)
        else:
            self.showInfoText(is_input_valid)

def main():
    root = Tk()
    app = Window(root)
    root.geometry("600x250+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()