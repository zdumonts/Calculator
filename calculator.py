# Assignment: PA4
# Author: Zander Dumont
# Date: 3/3/2023
# File: calculator.py, contains the main calculate method and the infix_to_postfix method
# input: calculator method: string infix expression
# output: calculator method: float value of the expression

from stack import Stack
from tree import ExpTree
import re

global a; a = {'^': 4,'*': 3, '/': 3, '+': 2, '-': 2, '(': 1} # precedence

def is_float(value):
    # helper function for infix_to_postfix
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def infix_to_postfix(infix):
    # removes spaces from infix
    uList = re.findall(r"(\b\w*[\.]?\w+\b|[\(\)\^\+\*\-\/])", infix)
    s = []
    # output string
    postfix = []

    # loop through the tokens
    for u in uList:
        if is_float(u):
            postfix.append(u)
        elif u == '(':
            s.append(u)
        elif u == ')':
            top = s.pop()
            while top != '(':
                postfix.append(top)
                top = s.pop()
        else:
            while s and (a[s[-1]] >= a[u]):
                postfix.append(s.pop())
            s.append(u)
    # pop all the remaining operators from the stack
    while s:
        postfix.append(s.pop())
    # return the postfix expression
    return ' '.join(postfix)

def calculate(infix):
    postfix = infix_to_postfix(infix)
    postfix = postfix.split()
    exp = ExpTree.make_tree(postfix) # make tree
    return ExpTree.evaluate(exp) # evaluate tree


# a driver to test calculate module
if __name__ == '__main__':
    print('Welcome to Calculator Program!')
    while True:
        user_input = input("Please enter your expression here. To quit enter 'quit' or 'q':\n")
        if user_input.lower() == 'quit' or user_input.lower() == 'q':
            print('Goodbye!')
            break
        else:
            print(str(calculate(user_input)))   

    # test infix_to_postfix function
    assert infix_to_postfix('(5+2)*3') == '5 2 + 3 *'
    assert infix_to_postfix('5+2*3') == '5 2 3 * +'
    # test calculate function
    assert calculate('(5+2)*3') == 21.0
    assert calculate('5+2*3') == 11.0