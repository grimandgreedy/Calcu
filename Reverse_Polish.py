#!/bin/python3

from Stack import Stack
import sys
import math

"""
Implementation of the Reverse Polish stack. Subclass of Stack. The push function is
reimplemented so that operations are done as everything is pushed onto the stack.

superclass: Stack
class RevPolStack
"""
class RevPolStack(Stack):
    """
    void __init__(self)
    @:returns N/A

    @:returns: initialized stack.
    """
    def __init__(self):
        Stack.__init__(self)
    """
    Bool push(self, string item)
    @:param string item: the item to be pushed onto the stack.
    @:returns Bool indicating if the push was successful. True: yes, False: no

    @description: takes an item and (if valid) pushes it onto the stack.
    @preconditions: The stack has been initialized.
    @postconditions: The item is pushed onto the stack and if it is an operator a result is calculated.
    @complexity: O(1)

    TESTING:
    #Note that in the stacks are represented as lists with the top of the stack to the right
    #Input: item,[current state]
    Input: 4,[1,2]              After push (expected): [1,2,4]           After push (actual): [1,2,4]   Returns True
    Input: +,[1,2]              After push (expected): [3]               After push (actual): [3]       Returns True
    Input: *,[1,2,19]           After push (expected): [1,38]            After push (actual): [1,38]    Returns True
    Input: *,[1]                After push (expected): Error!            After push (actual): Error!    Returns False
    Input: as,[1,2]             After push (expected): Error!            After push (actual): Error!    Returns False
    Input: >,[1,22,19]          After push (expected): [1,1]            After push (actual): [1,1]      Returns True
    """
    def push(self,item):
        type = itemType(item)
        #if operator
        if type == 0:
            #If single value operator - i.e. cos(10)
            if self.__len__() >= 1 and item not in ["||","&&","|","^","⨁","xor","&","<<",">>",
                                                "==","!=","<","<=",">=",">",
                                                "+","-","*","/","×","÷","//","%","mod","**","^"]:
                if item == "cos":
                    self.push(math.cos(self.pop()))
                elif item == "sin":
                    self.push(math.sin(self.pop()))
                elif item == "tan":
                    self.push(math.tan(self.pop()))
                elif item == "acos":
                    try:
                        self.push(math.acos(self.pop()))
                    except ValueError:
                        sys.stderr.write("Error: Arccos domain error.\n")
                        return False
                elif item == "asin":
                    try:
                        self.push(math.asin(self.pop()))
                    except ValueError:
                        sys.stderr.write("Error: Arcsine domain error.\n")
                        return False
                elif item == "atan":
                    try:
                        self.push(math.atan(self.pop()))
                    except ValueError:
                        sys.stderr.write("Error: Arctangent domain error.\n")
                #cosec
                elif item == "csc":
                    try:
                        self.push(1/math.sin(self.pop()))
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Cosecant domain error.\n")
                        return False
                #secant
                elif item == "sec":
                    try:
                        self.push(1/math.cos(self.pop()))
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Secant domain error.\n")
                        return False
                #cotangent
                elif item == "cot":
                    try:
                        self.push(1/math.tan(self.pop()))
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Cotangent domain error.\n")
                        return False
                #inverse cosecant
                elif item == "acsc":
                    #csc⁻¹(x) = asin(1/x)
                    try:
                        self.push(math.asin(1/self.pop()))
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Cosecant domain error.\n")
                        return False
                #inverse secant
                elif item == "asec":
                    #sec⁻¹(x) = acos(1/x)
                    try:
                        self.push(math.acos(1/self.pop()))
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Cosecant domain error.\n")
                        return False
                #inverse cotangent
                elif item == "acot":
                    #cot⁻¹ = atan(1/x)      for x >= 0
                    #cot⁻¹ = atan(1/x) + π  for x < 0
                    try:
                        temp = self.pop()
                        if temp >= 0:
                            self.push(math.atan(1/temp))
                        else:
                            self.push(math.atan(1/temp)+math.pi)
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Cotangent domain error.\n")
                        return False
                #cosh
                elif item == "cosh":
                    try:
                        self.push(math.cosh(self.pop()))
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Cosecant domain error.\n")
                        return False
                    except OverflowError:
                        sys.stderr.write("Overflow Error: Result too large.\n")
                        return False
                #sech
                elif item == "sinh":
                    try:
                        self.push(math.sinh(self.pop()))
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Sech domain error.\n")
                        return False
                    except OverflowError:
                        sys.stderr.write("Overflow Error: Result too large.\n")
                        return False
                #tanh
                elif item == "tanh":
                    try:
                        self.push(math.tanh(self.pop()))
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Cosh domain error.\n")
                        return False
                    except OverflowError:
                        sys.stderr.write("Overflow Error: Result too large.\n")
                        return False
                #Inverse cosh
                elif item == "acosh":
                    try:
                        self.push(math.acosh(self.pop()))
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Cosecant domain error.\n")
                        return False
                    except OverflowError:
                        sys.stderr.write("Overflow Error: Result too large.\n")
                        return False
                #Inverse sech
                elif item == "asinh":
                    try:
                        self.push(math.asinh(self.pop()))
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Sech domain error.\n")
                        return False
                    except OverflowError:
                        sys.stderr.write("Overflow Error: Result too large.\n")
                        return False
                #Inverse tanh
                elif item == "atanh":
                    try:
                        self.push(math.atanh(self.pop()))
                    except (ValueError,ZeroDivisionError):
                        sys.stderr.write("Error: Cosh domain error.\n")
                        return False
                    except OverflowError:
                        sys.stderr.write("Overflow Error: Result too large.\n")
                        return False
                elif item in ["sqrt","√"]:
                    if (self.peek() < 0):
                        sys.stderr.write("Error: Cannot raise negative numbers to negative powers.\n")
                        return False
                    self.push(math.sqrt(self.pop()))
                elif item == "log":
                    if self.peek() <= 0:
                        sys.stderr.write("Error: Log domain error.\n")
                        return False
                    self.push(math.log(self.pop(),10))
                elif item == "log2":
                    if self.peek() <= 0:
                        sys.stderr.write("Error: Log domain error.\n")
                        return False
                    self.push(math.log(self.pop(),2))
                elif item == "ln":
                    if self.peek() <= 0:
                        sys.stderr.write("Error: Log domain error.\n")
                        return False
                    self.push(math.log(self.pop(),math.e))
            #Two value operations - i.e. 2*9
            elif self.__len__() >= 2:
                if item == "+":
                    self.push(self.pop()+self.pop())
                elif item == "-":
                    self.push(-self.pop()+self.pop())
                elif item in ["*","×"]:
                    try:
                        self.push(self.pop()*self.pop())
                    except OverflowError:
                        sys.stderr.write("Error: Overflow error!\n")
                        return False
                elif item in ["/","÷"]:
                    inps = [self.pop() for i in range(2)]
                    try:
                        self.push(inps[1] / inps[0])
                    except ZeroDivisionError:
                        sys.stderr.write("Error: Cannot divide by zero!\n")
                        return False
                    except OverflowError:
                        sys.stderr.write("Error: Overflow error!\n")
                        return False
                elif item == "//":
                    inps = [self.pop() for i in range(2)]
                    try:
                        self.push(inps[1] // inps[0])
                    except ZeroDivisionError:
                        sys.stderr.write("Error: Cannot divide by zero!\n")
                        return False
                elif item in ["%","mod"]:
                    inps = [self.pop() for i in range(2)]
                    try:
                        self.push(inps[1] % inps[0])
                    except ZeroDivisionError:
                        sys.stderr.write("Error: Cannot divide by zero!\n")
                        return False
                elif item in ["**","^"]:
                    inps = [self.pop() for i in range(2)]
                    if inps[1] < 0 and 0 < inps[0] < 1:
                        sys.stderr.write("Error: Cannot take the root of a negative number.\n")
                        return False
                    try:
                        self.push(inps[1]**inps[0])
                    except OverflowError:
                        sys.stderr.write("Overflow Error: Result too large.\n")
                        return False
                    except ZeroDivisionError:
                        sys.stderr.write("Error: 0 cannot raise to be raised to a negative power.\n")
                        return False
                elif item == "==":
                    inps = [self.pop() for i in range(2)]
                    self.push(int(inps[1]==inps[0]))
                elif item == "!=":
                    inps = [self.pop() for i in range(2)]
                    self.push(int(inps[1]!=inps[0]))
                elif item == ">":
                    inps = [self.pop() for i in range(2)]
                    self.push(int(inps[1]>inps[0]))
                elif item == "<":
                    inps = [self.pop() for i in range(2)]
                    self.push(int(inps[1]<inps[0]))
                elif item == ">=":
                    inps = [self.pop() for i in range(2)]
                    self.push(int(inps[1]>=inps[0]))
                elif item == "<=":
                    inps = [self.pop() for i in range(2)]
                    self.push(int(inps[1]<=inps[0]))
                elif item == "&&":
                    inps = [self.pop() for i in range(2)]
                    self.push(int(inps[1] and inps[0]))
                elif item == "||":
                    inps = [self.pop() for i in range(2)]
                    self.push(int(inps[1] or inps[0]))
                elif item == ">>":
                    inps = [int(self.pop()) for i in range(2)]
                    if inps[0] < 0:
                        sys.stderr.write("Error, can't shift by negative amount.\n")
                        return False
                    self.push(inps[1] >> inps[0])
                elif item == "<<":
                    inps = [int(self.pop()) for i in range(2)]
                    if inps[0] < 0:
                        sys.stderr.write("Error, can't shift by negative amount.\n")
                        return False
                    try:
                        self.push(inps[1] << inps[0])
                    except OverflowError:
                        sys.stderr.write("Overflow Error: Result too large.\n")
                        return False
                elif item == "&":
                    self.push(int(self.pop()) & int(self.pop()))
                elif item == "|":
                    self.push(int(self.pop()) | int(self.pop()))
                elif item.lower() in ["xor","⨁"]:
                    self.push(int(self.pop()) ^ int(self.pop()))
            else:
                sys.stderr.write("Error: Invalid input. Not enough values/too many operators.\n")
                return False
        #if number push onto stack
        elif type in [1,2]:
            self.stack.append(item)
        else:
            sys.stderr.write("Error: Invalid input.\n")
            return False
        return True

"""
int/float revPolResult(list equation)
@:param list equation: a list representation of the equation in reverse polish form.
@:returns: int/float of the result.

@description: takes a list of terms as input and prints each term and its corresponding description.
                That is: operator, integer or invalid string.
@preconditions: The list provided is in reverse polish notation.
@postconditions: The result is returned as an int/float
@complexity Best & worst: O(N) where N is the number of items.

TESTING:
---------------------------------------------------------
Input: ['54', '9', '*']
Expected output: 486.0
Actual output:   486.0
---------------------------------------------------------
Input: ['100', '3', '*', '4', '-', '17', '3', '/', '+']
Expected output: 301.6666666666667
Actual output:   301.6666666666667
---------------------------------------------------------
Input: ['7', '*']
Expected output: None
Actual output: None
---------------------------------------------------------
Input: ['7', '5', '+']
Expected output: Error: Invalid input.
Actual output: Error: Invalid input.
---------------------------------------------------------
"""
def revPolResult(equation):
    stack = RevPolStack()
    for item in equation:
        #push all equation items onto stack. Exits if push returns false
        if stack.push(item) == False: return None
    #If there are left over numbers, then there weren't enough operations. Error.
    if stack.__len__() > 1:
        sys.stderr.write("Error: Too many values.\n")
        return None
    else:
        #if there is no decimal part to the value, return integer, else return float
        if stack.getStack() == []: return ""
        elif float(stack.__str__()).is_integer(): return int(float(stack.__str__()))
        else: return float(stack.__str__())
"""
int itemType(object item, list operators)
@:param object item: the item of which the type is to be determined
@:param list operators: the defined operators
@:returns: 0 if it is an operator
            1 if it is a float
            2 if it is an integer
            3 if it is invalid

@description: itemType takes an item and determines its type. Returning
an integer to represent it.
@preconditions: An item has been provided.
@postconditions: The type of that item is returned.
@complexity:Best & Worst: O(1) Single item, no loops.

TESTING:
Input: 324              Expected output: 2                    Actual output: 2
Input: 1.2              Expected output: 1                    Actual output: 1
Input: *                Expected output: 0                     Actual output: 0
Input: -                Expected output: 0                     Actual output: 0
Input: 2.12             Expected output: 1                     Actual output: 1
"""
def itemType(item,operators=
            ["||","&&","|","⨁","xor","&","<<",">>",
            "==","!=","<","<=",">=",">",
            "+","-","*","/","×","÷","//","%","mod","**","^","sqrt","√",
            "sin","cos","tan","csc","sec","cot","cosh","sinh","tanh"
            ,"acos","asin","atan","acsc","asec","acot","acosh","asinh","atanh",
            "log","log2","ln"]):
    if item in operators:
        return 0
    else:
        try:
            float(item)
            if float(item).is_integer():
                return 2
            return 1
        except ValueError:
            return 3
"""
Bool popFromOperatorStack(string input, string operatorOnStack)
@:param string input: The operator from the input stack
@:param string operatorOnStack: The operator from the on the top of the operator stack
@:returns Bool: returns true if the operator on the top of the stack is to be removed.

@description: determine if the operator on the operator stack is to be removed and placed in the output stack.
@preconditions: The stack has been initialized. Two operators have been provided.
@postconditions: A boolean is returned indicating whether the next item should be popped off the stack.
@complexity Best & Worst: O(1)

TESTING:
Input: +,-          Expected output: True      Actual output: True
Input: -,/          Expected output: True      Actual output: True
Input: *,-          Expected output: False     Actual output: False
"""
def popFromOperatorStack(input,operatorOnStack):
    prec = precedence(input,operatorOnStack)
    rightAssociativeOperators = ["**","^"]
    if prec == 0 or (prec == 1 and input not in rightAssociativeOperators):
        return True
    return False
"""
int precedence(string operator1, string operator2)
@:param string operator1: the first operator in the precedence comparison
@:param string operator2: the second operator in the precedence comparison
@:returns integer: returns -1 if there is an error
                   returns 0 if operator1 has lower precedence
                   returns 1 if operator1 has same precedence
                   returns 2 if operator1 has higher precedence

#Note that single value operations (i.e. cos,log,etc) have the highest precedence as they
#operate on the immediate value.

@description: Determines which operator (of the given two) has higher precedence.
@preconditions: The stack has been initialized. Two operators are provided.
@postconditions: The precedence of operator1 in comparison to operator2 is returned.
@complexity: O(1) The number of operators is looped through 2 times, which is constant.

TESTING:
Input: *,/          Expected output: 1      Actual output: 1
Input: -,/          Expected output: 0      Actual output: 0
Input: ||,&&        Expected output: 1      Actual output: 1
Input: a,b          Expected output: -1     Actual output: -1
Input: xor,*        Expected output: 0      Actual output: 0
Input: *,^          Expected output: 2      Actual output: 2
"""
def precedence(operator1,operator2):
    precedenceList = [["||"],["&&"],["==","!=","<","<=",">=",">"],["|"],["⨁","xor"],["&"],["<<",">>"],["+","-"],["*","/","×","÷","//","%","mod"],["**","^"],["sin","cos","tan","csc","sec","cot","cosh","sinh","tanh","acos","asin","atan","acsc","asec","acot","acosh","asinh","atanh","log","log2","ln","sqrt","√"]]
    prec = [-1,-1]
    for i in range(len(precedenceList)):
        if operator1 in precedenceList[i]:
            prec[0] = i
            break
    for i in range(len(precedenceList)):
        if operator2 in precedenceList[i]:
            prec[1] = i
            break
    if prec[0] == -1 or prec[1] == -1: return -1
    if prec[0] < prec[1]: return 0
    if prec[0] == prec[1]: return 1
    if prec[0] > prec[1]: return 2

"""
float infixToRevPol(list list)
@:param list list: converts the list (which is in infix) to reverse polish form.
@:returns list: Returns the list of items in Reverse Polish form
                None if there is an error.

@description: Takes an equation (in infix) as input, and converts it to Reverse Polish
@preconditions: The input list is in infix notation.
@postconditions: The item is pushed onto the stack and if it is an operator a result is calculated.
@complexity Best O(N) When the expression is in the correct form. I.e. the operators are in descending order.
@complexity Worst O(N^2) When the operations in the input list are in ascending order
            in terms of precedence.

TESTING:
---------------------------------------------------------
Input: ['3', '*', '5', '+', '9']
Expected output: ['3', '5', '*', '9', '+']
Actual output:   ['3', '5', '*', '9', '+']
---------------------------------------------------------
Input: ['2', '+', '4', '+', '7', '/', '3']
Expected output: ['2', '4', '+', '7', '3', '/', '+']
Actual output:   ['2', '4', '+', '7', '3', '/', '+']
---------------------------------------------------------
Input: ['7', '*', '9', '*', '31']
Expected output: ['7', '9', '*', '31', '*']
Actual output: ['7', '9', '*', '31', '*']
---------------------------------------------------------
Input: ['7', '5', '+']
Expected output: Error: Invalid input.
Actual output: Error: Invalid input.
---------------------------------------------------------
"""
def infixToRevPol(list):
    outputStack = Stack()
    operatorStack = Stack()
    for item in list:
        #if number
        if itemType(item) in [1,2]:
            outputStack.push(float(item))
        #if operator
        elif itemType(item) == 0:
            while operatorStack.__len__() > 0 and operatorStack.peek() != "(" and popFromOperatorStack(item,operatorStack.peek()):
                outputStack.push(operatorStack.pop())
            operatorStack.push(item)
        elif item in ["("]:
            operatorStack.push(item)
        elif item == ")":
            while True:
                if operatorStack.__len__() == 0:
                    sys.stderr.write("Error: Not enough closing brackets.")
                    return -1
                item = operatorStack.pop()
                if item == "(":
                    break
                outputStack.push(item)
    while operatorStack.__len__() > 0:
        outputStack.push(operatorStack.pop())
    return outputStack.getStack()
