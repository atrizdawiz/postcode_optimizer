from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog
from PostCodeOptimizer import PostCodeOptimizer

class Example(Frame):

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
            self.readFileAndWriteOutput(fl)


    def readFileAndWriteOutput(self, input_filename):
        postCodeOptimizer = PostCodeOptimizer(input_filename)
        postal_dictionary = postCodeOptimizer.postal_dictionary_creator()
        postal_range_string = postCodeOptimizer.postal_range_finder(postal_dictionary)
        with open(postCodeOptimizer.output_file, 'w') as f:
            f.write(postal_range_string)

def main():

    root = Tk()
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()