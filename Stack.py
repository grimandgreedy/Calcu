#!/bin/python3

"""
Implementation of a stack (ADT).

class Stack
"""
class Stack:
    """
    void __init__(self)

    @complexity: O(1)
    @description: Initializes the stack for use
    @preconditions: N/A
    @postconditions: The stack is ready for use
    """
    def __init__(self):
        self.stack = []
    """
    int __len__(self)
    @returns integer: the size of the stack

    @description: Returns the length of the stack
    @complexity: Best & worst case: O(N) has to go through the stack to count each item
    """
    def __len__(self):
        return len(self.stack)
    """
    int __str__(self)
    @returns string: a list of items separated by a single space, top of stack first

    @description: Returns a string containing the items separated by a space.
                  The items in the stack are printed in descending order.
                  i.e the top of the stack is printed first.
    @complexity: Best & worst case: O(N) has to convert each in the stack to a string.
    """
    def __str__(self):
        return ' '.join(reversed([str(item) for item in self.stack]))
    """
    void push(self, object item)
    @param: object item: The item to append to the list. Not limited to a single data type.
    @returns: N/A

    @description: Pushes 'item' onto the stack.
    @complexity: Best & worst case: O(1) A single item is pushed onto the stack
    """
    def push(self,item):
        self.stack.append(item)
    """
    object pop(self)
    @returns object: The item on the top of the stack

    @description: The item on the top of the stack is removed and returned.
                    If the stack is empty, then None is returned.
    @complexity: Best & worst case: O(1) A single item is popped off the stack
    """
    def pop(self):
        if self.__len__() != 0:
            temp = self.stack[-1]
            del self.stack[-1]
            return temp
        return None
    """
    object peek(self)
    @returns object: The item on the top of the stack

    @description: The item on the top of the stack is returned without being
                    popped off the stack.
    @complexity: Best & worst case: O(1) A single item is returned
    """
    def peek(self):
        if self.__len__() != 0: return self.stack[-1]
        else: return None
    """
    list getStack(self)
    @returns list: the stack is returned as a list

    @description: The stack is returned as a list.
    @complexity: Best & worst case: O(1) The stack is returned
    """
    def getStack(self):
        return self.stack
