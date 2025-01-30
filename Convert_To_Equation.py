#!/bin/python3

import re
import math
import sys

operators = ["||","&&","|","⨁","xor","&","<<",">>",                                    #bitwise
            "==","!=","<","<=",">=",">",                                                #comparison
            "+","-","*","/","×","÷","//","%","mod","**","^","sqrt","√",                 #arithmetic
            "sin","cos","tan","csc","sec","cot","cosh","sinh","tanh"                    #base trig
            ,"acos","asin","atan","acsc","asec","acot","acosh","asinh","atanh",         #inverse trig
            "log","log2","log₂","ln"]                                                   #log

"""
string expandComparisons(str string)
@:param str string: The string that we want to alter
@:returns str: returns the input string with the comparison operators expanded.

@description: Expands the comparison operators of a given string.
@preconditions: A string is provided which is in the form of an equation.
@postconditions: The string is outputted with the comparison operators expanded.
@complexity Best: O(N) When there are no comparisons. N, the length of the string.
@complexity Worst: O(N*M) Where N is the length of the string and
                    M is the number of comparison operators in the string.

TESTING:
--------------------------------------------------
Input: 1<2+5+3*2
Expected Output: 1<2+5+3*2 (no change)
Actual Output:   1<2+5+3*2
--------------------------------------------------
Input: 1<2<3
Expected Output: 1<2 && (2<3) (spaced out for readability)
Actual Output:   1<2 && (2<3)
--------------------------------------------------
Input: 1<500*3<=40!= 9
Expected Output: 1<500*3 && (500*3<=40 &&(40!=9)) (spaced out for readability)
Actual Output:   1<500*3 && (500*3<=40 &&(40!=9))
--------------------------------------------------
Input: (5>4) && (5<100) && 2!=1
Expected Output: (5>4) && (5<100) && 2!=1 (no change) (spaced out for readability)
Actual Output:   (5>4) && (5<100) && 2!=1
--------------------------------------------------
Input: 5<4 && 5<6
Expected Output: 5<4 && 5<6 (no change) (spaced out for readability)
Actual Output:   5<4 && 5<6
--------------------------------------------------
Input: 1<= (2<5) <4
Expected Output: 1 <= (2<5) && ((2<5) < 4) (spaced out for readability)
Actual Output:   1 <= (2<5) && ((2<5) < 4)
--------------------------------------------------
"""
def expandComparisons(string):
    #list location of comparison operators
    comparisonOperators = ["<",">","<=",">=","==","!="]
    comparisonLoc = []
    for item in comparisonOperators:
        comparisonLoc += [x.start() for x in re.finditer(item, string)]
    #list location of bitshift operators
    shiftLocs = []
    for item in ["<<",">>"]:
        shiftLocs += [x.start() for x in re.finditer(item, string)]
    shiftLocs += [x+1 for x in shiftLocs]
    #Remove duplicates location of bitshift operators
    comparisonLoc = list(set(sorted(set(list(comparisonLoc))))-set(shiftLocs))
    for i in range(len(comparisonLoc)-1):
        #list location of comparison operators
        comparisonLoc = []
        for item in comparisonOperators:
            comparisonLoc += [x.start() for x in re.finditer(item, string)]
        #list location of bitshift operators
        shiftLocs = []
        for item in ["<<",">>"]:
            shiftLocs += [x.start() for x in re.finditer(item, string)]
        shiftLocs += [x+1 for x in shiftLocs]
        #Remove duplicates location of bitshift operators
        comparisonLoc = sorted(set(sorted(set(list(comparisonLoc))))-set(shiftLocs))
        #get size of comparison operator - 1 or 2
        opSize = 2 if string[comparisonLoc[i]+1] == "=" else 1
        compLoop = iter(range(comparisonLoc[i]+opSize,len(string)))
        brackets = 0
        for j in compLoop:
            if string[j] == "(": brackets += 1
            elif string[j] == ")": brackets -= 1
            #if and/or is incountered break - i.e. 5<4 and 6<7
            elif j < len(string)-1 and string[j:j+2] in ["&&","||"]: break
            #if there is a closing bracket after comparison operator, then break = i.e. (5<4) and (3<2)
            if brackets < 0: break
            if string[j] in comparisonOperators+["=","!"] and brackets == 0:
                mid = string[comparisonLoc[i]+opSize:j]
                string = string[:j]+"&&("+mid+string[j:]+")"
                break
    return string
"""
string bracketAmbiguousExp(str string)
@:param str string: The string that we want to alter.
@:returns str: The bracketed string.

@description: Brackets ambiguous terms in string. Namely (int and regular) division and
                modulo expressions with a negative denominator. As well as expressions
                with a negative exponent.
@preconditions: A string is provided which is in the form of an equation.
@postconditions: The string is outputted with the ambiguous expressions bracketed.
@complexity Best: O(N) When there is no div/mod or exponent of negative numbers. N, the length of the string.
@complexity Worst: O(N*M) Where N is the length of the string and
                    M is the number of comparison operators in the string.

TESTING:
--------------------------------------------------
Input: 5**-4
Expected Output: 5**(-4)
Actual Output:   5**(-4)
--------------------------------------------------
Input: 2**-4**4
Expected Output: 2**(-4**4)
Actual Output:   2**(-4**4)
--------------------------------------------------
Input: 2%-15**2+4
Expected Output: 2%(-15**2)+4
Actual Output:   2%(-15**2)+4
--------------------------------------------------
Input: 4**-2%-5+4/-4*2 ########
Expected Output: 4**(-2)%(-5)+4/(-4)*2 (spaced out for readability)
Actual Output:   4**(-2)%(-5)+4/(-4)*2
--------------------------------------------------
Input: 4**-4**-1**1**-3
Expected Output: 4**(-4**(-1**1**(-3)))
Actual Output:   4**(-4**(-1**1**(-3)))
--------------------------------------------------
Input: 2**-1**-2**-3**-4**-5**-6**-7*5%3/-3**2%5
Expected Output: 2**(-1**(-2**(-3**(-4**(-5**(-6**(-7)))))))*5%3/(-3**2)%5
Actual Output:   2**(-1**(-2**(-3**(-4**(-5**(-6**(-7)))))))*5%3/(-3**2)%5
--------------------------------------------------
"""
def bracketAmbiguousExp(string):
    #bracket expressions with a negative exponent
    pos = string.find("**-")
    while pos != -1:
        fin = len(string)
        i = pos+3
        bracketCount = 0
        while i <len(string):
            try:
                #if char is number, pass.
                int(string[i])
            except ValueError:
                try:
                    if string[i:i+2] == "**":
                        i += 2
                        continue
                    elif string[i] == "-" and (string[i-1] in ["-","+"] or string[i-2:i] == "**"): pass
                    elif string[i] == "+" and (string[i-1] in ["-","+"] or string[i-2:i] == "**"): pass
                    elif string[i] == ".": pass
                    elif bracketCount == 0:
                        fin = i
                        break
                    elif string[i] == "(": bracketCount += 1
                    elif string[i] == ")": bracketCount -= 1
                except IndexError:
                    fin = i
                    break
            if i == len(string)-1: fin = i+1
            i += 1
        string = string[:pos+2]+"("+string[pos+2:fin]+")"+string[fin:]
        pos = string.find("**-")
    #bracket modulo expressions with a negative denominator
    pos = string.find("%-")
    while pos != -1:
        fin = len(string)
        i = pos+2
        bracketCount = 0
        while i <len(string):
            try:
                int(string[i])
            except ValueError:
                try:
                    if string[i:i+2] == "**":
                        i += 1
                    elif string[i] == "-" and (string[i-1] in ["-","+"] or string[i-2:i] == "**"): pass
                    elif string[i] == "+" and (string[i-1] in ["-","+"] or string[i-2:i] == "**"): pass
                    elif bracketCount == 0:
                        fin = i
                        break
                    elif string[i] == "(": bracketCount += 1
                    elif string[i] == ")": bracketCount -= 1
                except IndexError:
                    fin = i
                    break
            i += 1
        string = string[:pos+1]+"("+string[pos+1:fin]+")"+string[fin:]
        pos = string.find("%-")
    #bracket division (or integer division) expressions with a negative denominator
    pos = string.find("/-")
    while pos != -1:
        fin = len(string)
        i = pos+3
        bracketCount = 0
        while i <len(string):
            try:
                int(string[i])
            except ValueError:
                try:
                    if string[i:i+2] == "**":
                        i += 1
                    elif string[i] == "-" and (string[i-1] in ["-","+"] or string[i-2:i] == "**"): pass
                    elif string[i] == "+" and (string[i-1] in ["-","+"] or string[i-2:i] == "**"): pass
                    elif bracketCount == 0:
                        fin = i
                        break
                    elif string[i] == "(": bracketCount += 1
                    elif string[i] == ")": bracketCount -= 1
                except IndexError:
                    fin = i
                    break
                if i == len(string)-1: fin = i+1
            i += 1
        string = string[:pos+1]+"("+string[pos+1:fin]+")"+string[fin:]
        pos = string.find("/-")
    return string
"""
object splitToEquation(string string)
@:param string string: The string that we want to split into parts
@:returns int: returns -1 if there is an error, else returns the input string separated into components in list.

@description: Splits the input string into terms and operators.
@preconditions: A string is provided which is in the form of an equation.
@postconditions: The string is outputted in the form of a list, with all ambiguous expressions bracketed and all
                comparison operators expanded.
@complexity Best & Worst: O(N) where N is the number of characters in the string
#Note: Assumes that exponent notation is an E (capital) followed by a + or a negative number - i.e. 3E-45 NOT 3e-45

TESTING:
--------------------------------------------------
Input: 5*4*3*2*1+3
Expected Output: [5, '*', 4, '*', 3, '*', 2, '*', 1, '+', 3]
Actual Output:   [5, '*', 4, '*', 3, '*', 2, '*', 1, '+', 3]
--------------------------------------------------
Input: cos(24**5)  +  9
Expected Output: ['cos', '(', 24, '**', 5, ')', '+', 9]
Actual Output:   ['cos', '(', 24, '**', 5, ')', '+', 9]
--------------------------------------------------
Input: -41//-66**54+67//21/87-83**68/-82/-90
Expected Output: [-1, '*', 41, '//', '(', -1, '*', 66, '**', 54, ')', '+', 67, '//', 21, '/', 87, '-', 83, '**', -68, '/', -82, '/', 90]
Actual Output:   [-1, '*', 41, '//', '(', -1, '*', 66, '**', 54, ')', '+', 67, '//', 21, '/', 87, '-', 83, '**', -68, '/', -82, '/', 90]
--------------------------------------------------
Input: hello there
Expected Output: Error: Invalid input
Actual Output:   Error: Invalid input
"""
def convertToEquation(string):
    equation = []
    if len(string) == 0:
        return [string]
    #remove whitespace and sub int appropriate function names
    string = string.replace("pi","("+str(math.pi)+")")
    string = string.replace("π","("+str(math.pi)+")")
    string = string.replace("degrees",str(math.pi/180))
    string = string.replace("deg","*"+str(math.pi/180))
    string = string.replace("sec","¡¡")
    string = string.replace("e","("+str(math.e)+")")
    string = string.replace("E+","*10**")
    string = string.replace("E-","*10**-")
    string = string.replace("¡¡","sec")
    string = string.replace("^","**")
    string = string.replace("°","*"+str(math.pi/180))
    string = string.replace(" ","")
    string = bracketAmbiguousExp(string)
    string = expandComparisons(string)
    i = 0
    while i < len(string):
        try:
            #if the character is an integer
            int(string[i])
            #if previous character was a digit, multiply it by 10 and add current integer
            if len(equation) > 0 and type(equation[-1]) == type(int()):
                equation[-1] = equation[-1]*10+int(string[i])
            #if previous item in equation is a float
            elif len(equation) > 0 and type(equation[-1]) == type(float()):
                #Find the number of integers after the decimal place and add 1 for the exponent
                exponent = -(string[:i][::-1].find(".")+1)
                equation[-1] = equation[-1]+int(string[i])*pow(10,exponent)
            #if previous character in string was a decimal
            elif len(equation) > 0 and equation[-1] == ".":
                del equation[-1]
                #if character before decimal was an operator or first character is decimal - e.g. 2*.3 or .3*4
                if len(equation) == 0 or equation[-1] in operators:
                    equation.append(float((1/10)*int(string[i])))
                #if the character before the decimal was positive
                elif len(equation) > 0 and equation[-1] >= 0:
                    equation[-1] = float(equation[-1])+(1/10)*int(string[i])
                #else if negative, minus the decimal
                elif len(equation) > 0 and equation[-1] < 0:
                    equation[-1] = float(equation[-1])-(1/10)*int(string[i])
            else: equation.append(int(string[i]))
        except ValueError:
            #if the character is an operator or bracket
            if string[i] in ["(",")","=","a","s","c","t","l","m","x"]+operators:
                if i < len(string)-1:
                    #check for 5 character function
                    if i < len(string)-4 and string[i:i+5] in operators:
                        equation.append(string[i:i+5])
                        i += 5     #skip next four iterations
                        continue
                    #check for 4 character function
                    elif i < len(string)-3 and string[i:i+4] in operators:
                        equation.append(string[i:i+4])
                        i += 4     #skip next three iterations
                        continue
                    #check for 3 character function
                    elif i < len(string)-2 and string[i:i+3] in operators:
                        equation.append(string[i:i+3])
                        i += 3     #skip next two iterations
                        continue
                    #check if it is a two character operator
                    elif string[i:i+2] in operators:
                        equation.append(string[i:i+2])
                        i += 2     #skip next iteration
                        continue
                    #check if first operator is negative or if minus operator proceeds another operator
                    elif string[i] == "-" and (equation==[] or equation[-1] in operators+["(",")"]):
                        if len(equation) > 0 and equation[-1] == ")":
                            equation.append("-")
                        #if the following operation has the same precedence, make the prior number negative
                        elif len(equation)>1 and equation[-1] in ["/","%","//"] and (i<=1 or equation[-2] != ")"):
                            #division is reversible mod is not - i.e. a/-b = -a/b, but a%-b != -a%b
                            equation[-2] *= -1
                        #if previous character was an integer
                        elif i > 0:
                            try:
                                int(string[i-1])
                                equation.append("-")
                            except ValueError:
                                equation.append(-1)
                                equation.append("*")
                        else:
                            equation.append(-1)
                            equation.append("*")
                    #if an addition sign is after an operator and before a number, it is meaningless
                    elif string[i] == "+" and (equation==[] or equation[-1] in operators+["("]):
                        pass
                    elif string[i] in ["=","a","s","c","t","l","x"]:
                        sys.stderr.write("Error: Invalid term.\n")
                        return -1
                    else:
                        equation.append(string[i])
                elif string[i] not in ["=","a","s","c","t","l","m"]:
                    equation.append(string[i])
                else:
                    sys.stderr.write("Error: Invalid input.\n")
                    return -1
            elif string[i] == ".":
                #if first character or previous character was an operator - i.e. 5*.4
                if (len(equation) > 0 and equation[-1] in operators) or len(equation) == 0:
                    equation.append(".")
                elif len(equation) > 0:
                    #see if characters before equation were integers
                    #if type(equation[-1]) == type(float()) or type(equation[-1]) == type(int()):
                    try:
                        int(equation[-1])
                        if float(equation[-1]) == int(equation[-1]):
                            equation.append(".")
                        else:
                            sys.stderr.write("Error: Invalid input.\n")
                            return -1
                    except ValueError:
                        sys.stderr.write("Error: Invalid input\n")
                        return -1
                else:
                    sys.stderr.write("Error: Invalid input\n")
                    return -1
            else:
                sys.stderr.write("Error: Invalid input\n")
                return -1
        i += 1
    return equation
