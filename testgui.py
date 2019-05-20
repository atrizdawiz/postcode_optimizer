from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog
from PostCodeOptimizer import PostCodeOptimizer

class Example(Frame):
    postCode = PostCodeOptimizer()

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("Postcode optimizer")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)


    def onOpen(self):

        ftypes = [('Text files', '*.txt'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFileAndWriteOutput(fl)
            self.txt.insert(END, text)

    def readFileAndWriteOutput(self, filename):
        PostCodeOptimizer.input_filename = filename
        postcode_dictionary = PostCodeOptimizer.postal_dictionary_creator(filename)
        postal_range_string = PostCodeOptimizer.postal_range_finder(postcode_dictionary)
        with open(PostCodeOptimizer.output_file, 'w') as f:
            f.write(postal_range_string)


def main():

    root = Tk()
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()