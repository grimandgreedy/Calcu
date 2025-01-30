#!/bin/python3

from Stack import *
from Convert_To_Equation import *
from Reverse_Polish import *
from Calculator_GUI import *
from tkinter import *

def main():
    #Start calculator
    root = Tk()
    app = Sci_Calculaor(root)
    root.mainloop()

if "__main__":
    main()
