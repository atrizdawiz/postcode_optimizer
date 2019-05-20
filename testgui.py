from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog
from listofnumbertoranges.PostCodeOptimizer import postal_dictionary_creator

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
            text = self.readFile(fl)
            self.txt.insert(END, text)

    def readFile(self, filename):
        postcode_dictionary = postal_dictionary_creator(filename)
        f = open(filename, "r")
        text = f.read()
        return text


def main():

    root = Tk()
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()