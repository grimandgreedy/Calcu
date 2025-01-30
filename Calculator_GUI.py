#!/bin/python3

from tkinter import *
from Reverse_Polish import *
from Convert_To_Equation import *

topColor = "#4D7CCC"

singleValOps = ["sqrt","√","cr","sin","cos","tan","acos","asin","atan","csc","sec","cot","cosh","sinh","tanh","log","log2","ln"]
trigOps = ["sin","cos","tan","csc","sec","cot","cosh","sinh","tanh"]
class Sci_Calculaor:
    """
    void __init__ (self, object master)
    @param: tkinter-root-object master: A tkinter application node

    @complexity: O(1)
    @description: Sets the calculator up for use and displays the window
    @preconditions: The Reverse_Polish and Convert_To_Equation functions are in the scope.
    @postconditions: The calculator is set up and ready for input
    """
    def __init__(self, master):
        self.master = master
        self.equationList = [0]
        self.displayAnswer = False
        self.inverseTrig = False
        self.topTextSize = 50
        self.createWindow()
    """
    void createWindow (self)

    @complexity Best & Worst: O(1)
    @description: Displays the initial window for the calculator.
    @preconditions: The Reverse_Polish and Convert_To_Equation functions are in the scope.
    @postconditions: The calculator is set up and ready for input
    """
    def createWindow(self):
        #change window title
        self.master.wm_title("Scientific Calculator")
        #Not resizable
        self.master.resizable(width=FALSE, height=FALSE)

        #Create window frame
        self.frame = Frame(self.master)
        self.frame.grid(column=0,row=0)

        self.scientificCalc()
        self.displayTopPanel()

        self.master.bind("<Key>",self.keyPress)
        self.master.bind("<BackSpace>",self.deleteChar)
        self.master.bind("<Escape>",self.clearExpression)
        self.master.bind("<Return>",self.getAnswer)
        #create equation frame
        self.equationFrame = Frame(self.topPanel,bg=topColor,width=self.topPanel.winfo_width(),height=15)
        self.equationFrame.pack(side="top")
        self.equationFrame.pack_propagate(0)
        self.equationFrame.update()

        self.displayTopPanel()
    """
    void scientificCalc (self)

    @complexity Best & Worst: O(1)
    @description: Draw the buttons onscreen.
    @preconditions: The Reverse_Polish and Convert_To_Equation functions are in the scope.
    @postconditions: The top/bottom portions of the calculator are created onscreen and the buttons are displayed.
    """
    def scientificCalc(self):
        #Create game topPanel
        self.topPanel = Frame(self.frame,width=550,height=80,bg=topColor, bd=0, highlightthickness=0, relief='ridge')
        self.topPanel.grid(column=0,row=0)
        self.topPanel.update()
        self.topPanel.pack_propagate(0)     #maintain size
        #Create game topPanel
        self.bottomPanel = Frame(self.frame,width=550,height=220,bg=topColor, bd=0, highlightthickness=0, relief='ridge')
        self.bottomPanel.grid(column=0,row=1)
        self.bottomPanel.update()
        self.bottomPanel.grid_propagate(0)  #maintain size
        #Bind buttons to move window

        self.c = ["#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#F27A02",
              "#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#F27A02",
              "#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#F27A02",
              "#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#F27A02",
              "#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#e0e0e0","#32A7CF","#F27A02"]
        r = ["inv","π","e","x²","(",")","%","AC",
              "sin","cos","tan","x³","7","8","9","÷",
              "sec","csc","cot","xⁿ","4","5","6","×",
              "sinh","cosh","tanh","√","1","2","3","-",
              "log","log₂","ln","1/x","0",".","=","+"]
        #display buttons
        self.buttons = []
        for j in range(5):
            for i in range(8):
                self.f = Frame(self.bottomPanel,bg=self.c[i+j*8],width=self.bottomPanel.winfo_width()/8,height=self.bottomPanel.winfo_height()/5,borderwidth=1,relief="raised")
                self.f.grid(row=j,column=i,sticky="NW")
                self.f.grid_propagate(0)    #keep size fixed
                self.f.update()
                self.l = Label(self.f,text="{0}".format(r[i+j*8]),bg=self.c[i+j*8],font="Arial 16")
                self.l.place(x=self.bottomPanel.winfo_width()/16, y=self.bottomPanel.winfo_height()/10, anchor="center")
                self.f.bind("<Button-1>",lambda event,a=[r[i+j*8],i,j]: self.buttonclicked(a))
                self.l.bind("<Button-1>",lambda event,a=[r[i+j*8],i,j]: self.buttonclicked(a))
                self.f.bind("<ButtonRelease-1>",lambda event,a=[r[i+j*8],i,j]: self.unhighlightButton(a))
                self.l.bind("<ButtonRelease-1>",lambda event,a=[r[i+j*8],i,j]: self.unhighlightButton(a))
                self.buttons.append([self.f,self.l]) #buttons[Frame, Label]
    """
    void displayTopPanel (self)
    @:param list arg: arg is a list with the first item being the value of the button pressed and the second being the
                coordinates of the button on the screen.
    @complexity Best & Worst: O(1)
    @description: Displays the label for the top panel to the user. Displays whatever is in the equationList variable.
                Whether that is a result or an equation depends on the context and time the function is called.
    @preconditions: The calculator has been initialized.
    @postconditions: The label for the top panel is displayed to the user.
    """
    def displayTopPanel(self):
        try:
            self.topLabel.destroy()
        except AttributeError:
            pass
        self.topLabel = Label(self.topPanel,text="".join([str(x) for x in self.equationList]),bg=topColor,font=("Arial {0}".format(self.topTextSize)),padx=10,anchor="e")
        loopCount = 0
        #adjust text size to fit screen. Max 50, Min 20.
        for i in range(30):
            self.topLabel.configure(font=("Arial {0}".format(self.topTextSize)))
            self.topLabel.pack(side="right")
            self.topPanel.update()
            if self.topLabel.winfo_width() == self.master.winfo_width() and self.topTextSize > 20: self.topTextSize -= 2
            elif self.topLabel.winfo_width() < self.master.winfo_width()-50 and self.topTextSize < 50: self.topTextSize += 2
            else: break
    """
    void keyPress (self, object event)
    @:param tkinter-event object event: The tkinter event created when a user presses a key, contains information
                                        about the event incuding which key/s were pressed.
    @complexity Best & Worst: O(1)
    @description: The function is called when the user presses a key. Determines the key and adds the value of the key
                    to the equationList and displaying the result onscreen.
    @preconditions: The Reverse_Polish and Convert_To_Equation functions are in the scope. The user had pressed a key.
    @postconditions: The users key is added to the equationList.

    TESTING:
    -----------------------------------------------
    Input: 2,[3, '×', 'cos', '(']
    Expected output: [3, '×', 'cos', '(', 2]
    Actual output: [3, '×', 'cos', '(', 2]
    -----------------------------------------------
    Input: 'c',[0]
    Expected output: ['c']
    Actual output: ['c']
    -----------------------------------------------
    Input: 'e',['e']
    Expected output: ['e', 'e']
    Actual output: ['e', 'e']
    -----------------------------------------------
    """
    def keyPress(self,event):
        if event.char == "":return
        if event.char == "*": event.char = "×"
        elif event.char == "/": event.char = "÷"
        elif event.char == "%": event.char = "mod"
        if self.equationList in [[0],["Error"],["Error: Overflow"]] or (self.displayAnswer == True and event.char in list("0123456789")):
            self.equationList = [event.char]
        elif event.char == "×" and self.equationList[-1]=="×":
            self.equationList[-1] = "^"
        else:
            self.equationList.append(event.char)
        self.displayAnswer = False
        self.displayTopPanel()
    """
    void deleteChar (self, object event)
    @:param tkinter-event object event: The tkinter event created when a user presses a key, contains information
                                        about the event.
    @complexity Best & Worst: O(1)
    @description: Called when the user presses the delete (mac)/backspace key (windows/linux). The previous value is
                removed from the equation and the updated equation is displayed onscreen. If there is only one value
                left in the list, then the list becomes [0].
    @preconditions: The Reverse_Polish and Convert_To_Equation functions are in the scope. The user has pressed the
                    backspace key.
    @postconditions: The most recent entry is removed from the equationList.

    TESTING:
    -----------------------------------------------
    Before: [3, '×', 'cos', '(']
    Expected after: [3, '×', 'cos']
    Actual after: [3, '×', 'cos']
    -----------------------------------------------
    Input: [2]
    Expected output: [0]
    Actual output: [0]
    -----------------------------------------------
    Input: [3, '×', 'log', '(',1000]
    Expected output: [3, '×', 'log', '(',100]
    Actual output: [3, '×', 'log', '(',100]
    -----------------------------------------------
    Input: [3, '×', 'log']
    Expected output: Input: [3, '×']
    Actual output: [3, '×']
    -----------------------------------------------
    """
    def deleteChar(self,event):
        #if there is one item in the array which is 1 character long or displayAnswer is true.
        if (len(self.equationList) == 1 and len(str(self.equationList[-1])) == 1) or self.displayAnswer:
            self.equationList = [0]
        elif itemType(self.equationList[-1]) in [1,2] and len(str(self.equationList[-1])) > 1:
            #if the number is an integer
            self.equationList[-1] = float(str(self.equationList[-1])[:-1])
            #if the item is an integer, remove decimal part
            if float(str(self.equationList[-1])[:-1]).is_integer():
                self.equationList[-1] = int(self.equationList[-1])
        elif len(self.equationList) == 1:
            self.equationList = [0]
        else:
            del self.equationList[-1]
        self.displayTopPanel()
    """
    void clearExpression (self, object event)
    @:param tkinter-event object event: The tkinter event created when a user presses a key, contains information
                                        about the event.
    @complexity Best & Worst: O(1)
    @description: Called when the user presses the delete (mac)/backspace key (windows/linux). The previous value is
                removed from the equation and the updated equation is displayed onscreen. If there is only one value
                left in the list, then the list becomes [0].
    @preconditions: The Reverse_Polish and Convert_To_Equation functions are in the scope. The user has pressed the
                    backspace key.
    @postconditions: The most recent entry is removed from the equationList.

    TESTING:
    -----------------------------------------------
    Before: [3, '×', 'cos', '(']
    Expected after: [3, '×', 'cos']
    Actual after: [3, '×', 'cos']
    -----------------------------------------------
    Input: [2]
    Expected output: [0]
    Actual output: [0]
    -----------------------------------------------
    Input: [3, '×', 'log', '(',1000]
    Expected output: [3, '×', 'log', '(',100]
    Actual output: [3, '×', 'log', '(',100]
    -----------------------------------------------
    Input: [3, '×', 'log']
    Expected output: Input: [3, '×']
    Actual output: [3, '×']
    -----------------------------------------------
    """
    def clearExpression(self,event):
        #if there is one item in the array which is 1 character long or displayAnswer is true.
        self.equationList = [0]
        self.displayTopPanel()
    """
    void getAnswer (self, object event=None)
    @:param tkinter-event object event: The tkinter event created when a user presses a key, contains information
                                        about the event. None by default, but accepts an event if the function is called
                                        by pressing = in the GUI.
    @complexity Best & Worst: O(1)
    @description: Called when the user presses the the return key or the equals key (=) onscreen. The result of the
                inputted equation is calculated and displayed. Also closes all open brackets if applicable.
    @preconditions: The Reverse_Polish and Convert_To_Equation functions are in the scope. The user has pressed the
                    return key or = key onscreen.
    @postconditions: The most recent entry is removed from the equationList.

    TESTING:
    -----------------------------------------------
    Before: [3, '×', '8']
    Expected after: [24]
    Actual after: [24]
    -----------------------------------------------
    Input: ['h','e','l','o',' ','t','h','e','r','e']
    Expected output: ["Error"]
    Actual output: ["Error"]
    -----------------------------------------------
    Input: [3, '×', 'log', '(',1000,")"]
    Expected output: [9]
    Actual output: [8.999999999999998]      ~~rounding error
    -----------------------------------------------
    Input: [3, '×', 10,"^",60]
    Expected output: Input: [3E+60]
    Actual output: [3E+60]
    -----------------------------------------------
    """
    def getAnswer(self,event=None):
        #join elements of the string, remove whitespace and replace any exponent with capital E, i.e. 1e+10 -> 1E+10
        equationString = "".join([str(x).replace("e","E") if type(x) == type(float()) else str(x) for x in self.equationList]).replace(" ","")
        #Close all open brackets
        while equationString.count(")") < equationString.count("("):
            equationString += ")"
        #convert to equation
        equation = convertToEquation(equationString)
        if equation == -1:
            self.equationList = ["Error"]
            self.displayTopPanel()
            return
        #Convert to infix and compute the result
        result = infixToRevPol(equation)
        print(result)
        if result == -1:
            self.equationList = ["Error"]
            self.displayTopPanel()
            return
        result = revPolResult(result)
        if result == None:
            self.equationList = ["Error"]
            self.displayTopPanel()
            return
        #if output is >25 characters long, convert to scientific notation.
        elif len(str(result)) > 25:
            try:
                result = float(result)
            #if too long to be converted to float
            except OverflowError:
                #if the result is greater than 45 characters long, display error, else leave as is.
                if len(str(result)) > 45:
                    self.equationList = ["Error: Overflow"]
                    self.displayTopPanel()
                    return
        #delete self.equation if it exists
        try:
            self.equation.destroy()
        except AttributeError:
            pass
        #display the equation at the top right
        self.equation = Label(self.equationFrame,text=equationString+" = ",bg=topColor,font=("Arial {0}".format(10)),padx=10,anchor="e")
        self.equation.pack(side="right")
        self.topPanel.update()

        self.equationList = [str(result).replace("e","E")]
        self.displayAnswer = True
        self.displayTopPanel()
    """
    void buttonclicked (self, list arg)
    @:param list arg: arg is a list with the first item being the value of the button pressed and the second being the
                coordinates of the button on the screen.
    @complexity Best & Worst: O(1)
    @description: A button on the screen is pushed and the result of the press is determined based on prior input.
                E.g. + is pressed after a previous + and nothing happens.
    @preconditions: The Calculator has been initialized and is ready for user input.
    @postconditions: The result of the button press is displayed.

    TESTING:
    -----------------------------------------------
    Input: 2,[3, '×', 'cos', '(']
    Expected output: [3, '×', 'cos', '(', 2]
    Actual output: [3, '×', 'cos', '(', 2]
    -----------------------------------------------
    Input: 'cos',[0]
    Expected output: ['cos']
    Actual output: ['cos']
    -----------------------------------------------
    Input: '+',[4,"-"]
    Expected output: [4, '+']
    Actual output: [4, '+']
    -----------------------------------------------
    """
    def buttonclicked(self,arg):
        #Highlight button - i.e. change it's color
        col = "#"+hex((int(self.c[arg[2]*8+arg[1]][1:],16) & 0xfefefe) >> 1)[2:]    #darker color based on the base value
        self.buttons[arg[2]*8+arg[1]][0].configure(bg=col)    #highlight frame
        self.buttons[arg[2]*8+arg[1]][1].configure(bg=col)
        item = arg[0]
        if item == "log₂": item = "log2"
        if item == "xⁿ": item = "^"

        if item == "=":
            self.getAnswer()
        elif item == "inv":
            self.inverseTrig = not self.inverseTrig
            trigList = ["sin","cos","tan",
                           "sec","csc","cot",
                           "sinh","cosh","tanh"]
            if self.inverseTrig:
                for j in range(1,4):
                    for i in range(0,3):
                        self.buttons[i+j*8][1].configure(text="{0}⁻¹".format(trigList[i+(j-1)*3]))
            else:
                for j in range(1,4):
                    for i in range(0,3):
                        self.buttons[i+j*8][1].configure(text="{0}".format(trigList[i+(j-1)*3]))
        elif item == "AC":
            self.equationList = [0]
            self.displayAnswer = False
            self.topTextSize = 50
        #if constant
        elif item in ["π","pi","e"]:
            #if displaying answer, empty array or error
            if self.equationList == [0] or "Error" in str(self.equationList[-1]) or self.displayAnswer==True:
                self.equationList = [item]
                self.displayAnswer = False
            #if constant follows an operator or open bracket
            elif str(self.equationList[-1]) in operators+["("]:
                self.equationList.append(item)
            #if input number follows another number or constant
            elif itemType(self.equationList[-1]) in [1,2] or self.equationList[-1] in [")","π","pi","e","."]:
                self.equationList.append("×")
                self.equationList.append(item)
        #if button is an integer
        elif item in list("0123456789"):
            #if displaying answer, empty array or error
            if self.equationList == [0] or "Error" in str(self.equationList[-1]) or self.displayAnswer==True:
                self.equationList = [int(item)]
                self.displayAnswer = False
            #if input number follows an operator, open bracket or decimal point
            elif str(self.equationList[-1]) in operators+["(","."]:
                self.equationList.append(int(item))
            #if input number follows an integer
            elif itemType(self.equationList[-1]) == 2:
                self.equationList[-1] = int(self.equationList[-1])*10+int(item)
            #if input number follows a closing bracket, constant or previously entered floating point num
            elif self.equationList[-1] in [")","π","pi","e"] or itemType(self.equationList[-1]) == 1:
                self.equationList.append("×")
                self.equationList.append(int(item))
        elif item == ".":
            #if displaying answer, empty array or error
            if self.equationList == [0] or "Error" in str(self.equationList[-1]) or self.displayAnswer==True:
                self.equationList = [0,"."]
                self.displayAnswer = False
            #if decimal point follows an operator, open bracket or decimal point
            elif str(self.equationList[-1]) in operators+["("]:
                self.equationList.append(0)
                self.equationList.append(".")
            #if the decimal point follows an integer and doesn't follow a float
            elif itemType(self.equationList[-1]) == 2 and (len(self.equationList) < 2 or self.equationList[-2] != "."):
                self.equationList.append(".")
            #if the decimal point follows a closing bracket, constant or previously entered float
            elif str(self.equationList[-1]) in [")","π","pi","e"] or itemType(self.equationList[-1]) == 1:
                self.equationList.append("×")
                self.equationList.append(0)
                self.equationList.append(".")
        elif item == "(":
            #if displaying answer, empty array or error
            if self.equationList == [0] or "Error" in str(self.equationList[-1]) or self.displayAnswer==True:
                self.equationList = ["("]
                self.displayAnswer = False
            #if bracket follows an operator or another open bracketℇ
            elif str(self.equationList[-1]) in operators+["("]:
                self.equationList.append("(")
            #if open bracket follows closed bracket, constant or number
            elif str(self.equationList[-1]) in [")","π","pi","e","."] or itemType(self.equationList[-1]) in [1,2]:
                self.equationList.append("×")
                self.equationList.append("(")
        elif item == ")":
            equationString = "".join([str(x) for x in self.equationList])
            #if displaying answer, empty array or error
            if self.equationList == [0] or "Error" in str(self.equationList[-1]) or self.displayAnswer==True:
                pass
            #if number of closed brackets is less than the number of open brackets
            elif equationString.count(")") < equationString.count("("):
            #if close bracket follows a bracet, decimal point or constant
                if str(self.equationList[-1]) in [")",".","π","pi","e"] or itemType(self.equationList[-1]) in [1,2]:
                    self.equationList.append(item)
        #if button pressed is a single value operation - i.e. sqrt(x)
        elif item in singleValOps:
            #if inverse trig option add a (arc) prefix to argument before assigning it.
            if self.inverseTrig == True and item in trigOps: item = "a"+item
            #if displaying answer, empty array or error
            if self.equationList == [0] or "Error" in str(self.equationList[-1]) or self.displayAnswer==True:
                self.equationList = [item,"("]
                self.displayAnswer = False
            #if single val operator follows an operator or another open bracket
            elif str(self.equationList[-1]) in operators+["("]:
                self.equationList.append(item)
                self.equationList.append("(")
            #if single val operator follows closed bracket, constant or number
            elif str(self.equationList[-1]) in [")","π","pi","e","."] or itemType(self.equationList[-1]) in [1,2]:
                self.equationList.append("×")
                self.equationList.append(item)
                self.equationList.append("(")
        #if operator
        elif item == "x²":
            if self.equationList == [0] or "Error" in str(self.equationList[-1]) or self.displayAnswer==True:
                self.equationList += ["^","(",2,")"]
                self.displayAnswer = False
            #if single val operator follows closed bracket, constant or number
            elif itemType(self.equationList[-1]) in [1,2] or str(self.equationList[-1]) in [")","π","pi","e","."]:
                self.equationList += ["^","(",2,")"]
        elif item == "x³":
            if self.equationList == [0] or "Error" in str(self.equationList[-1]) or self.displayAnswer==True:
                self.equationList += ["^","(",3,")"]
                self.displayAnswer = False
            #if single val operator follows closed bracket, constant or number
            elif itemType(self.equationList[-1]) in [1,2] or str(self.equationList[-1]) in [")","π","pi","e","."]:
                self.equationList += ["^","(",3,")"]
        elif item == "1/x":
            if not "Error" in str(self.equationList[-1]):
                self.equationList = [1,"/","("]+self.equationList+[")"]
                self.displayAnswer = False
            else:
                self.equationList = [1,"/","("]
        elif item == "-":
            #if displaying answer, empty array or error
            if self.equationList == [0] or "Error" in str(self.equationList[-1]) or self.displayAnswer==True:
                if self.displayAnswer == True:
                    self.equationList.append("-")
                else:
                    self.equationList = ["-"]
                self.displayAnswer = False
            #if negative follows an operator or another open bracket, but not a previous negative
            elif str(self.equationList[-1]) in list(set(operators)-set(["-"]))+["("]:
                self.equationList.append("-")
            #if negative follows closed bracket, constant or number
            elif str(self.equationList[-1]) in [")","π","pi","e","."] or itemType(self.equationList[-1]) in [1,2]:
                self.equationList.append("-")
        elif item in operators:
            #if displaying answer, empty array or error
            if self.equationList == [0] or "Error" in str(self.equationList[-1]) or self.displayAnswer==True:
                self.equationList.append(item)
                self.displayAnswer = False
            #if operator follows another operator
            elif str(self.equationList[-1]) in operators:
                self.equationList[-1] = item
            #if operator follows closed bracket, constant or number
            elif str(self.equationList[-1]) in [")","π","pi","e","."] or itemType(self.equationList[-1]) in [1,2]:
                self.equationList.append(item)
        self.displayTopPanel()
    """
    void unhighlightButton (self, list arg)
    @:param list arg: arg is a list with the first item being the value of the button pressed and the second being the
                coordinates of the button on the screen.
    @complexity Best & Worst: O(1)
    @description: Once an onscreen button is pushed, this function is called when the user releases the button and
                returns the button clicked to its unhighlighted/inactive state.
    @preconditions: A button has been clicked by the user.
    @postconditions: The button previously clicked by the user is no longer 'active'.
    """
    def unhighlightButton(self,arg):
        self.buttons[arg[2]*8+arg[1]][0].configure(bg=self.c[arg[2]*8+arg[1]])    #unhighlight frame
        self.buttons[arg[2]*8+arg[1]][1].configure(bg=self.c[arg[2]*8+arg[1]])    #unhighlight label
    """
    void displayTopPanel (self)
    @:param list arg: arg is a list with the first item being the value of the button pressed and the second being the
                coordinates of the button on the screen.
    @complexity Best & Worst: O(1)
    @description: Displays the label for the top panel to the user. Displays whatever is in the equationList variable.
                Whether that is a result or an equation depends on the context and time the function is called.
    @preconditions: The calculator has been initialized.
    @postconditions: The label for the top panel is displayed to the user.
    """
    def displayTopPanel(self):
        try:
            self.topLabel.destroy()
        except AttributeError:
            pass
        self.topLabel = Label(self.topPanel,text="".join([str(x) for x in self.equationList]),bg=topColor,font=("Arial {0}".format(self.topTextSize)),padx=10,anchor="e")
        loopCount = 0
        #adjust text size to fit screen. Max 50, Min 20.
        while True:
            self.topLabel.configure(font=("Arial {0}".format(self.topTextSize)))
            self.topLabel.pack(side="right")
            self.topPanel.update()
            if loopCount >= 30: break
            elif self.topLabel.winfo_width() == self.master.winfo_width() and self.topTextSize > 20: self.topTextSize -= 2
            elif self.topLabel.winfo_width() < self.master.winfo_width()-50 and self.topTextSize < 50: self.topTextSize += 2
            else: break
            loopCount += 1
