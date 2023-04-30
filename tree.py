# Assignment: PA4
# Author: Zander Dumont
# Date: 3/3/2023
# File: tree.py
# input: 
# output: 

from stack import Stack

class BinaryTree:

    def __init__(self,rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self,newNodeVal):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNodeVal)
        else:
            t = BinaryTree(newNodeVal)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self,newNodeVal):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNodeVal)
        else:
            t = BinaryTree(newNodeVal)
            t.rightChild = self.rightChild
            self.rightChild = t
    
    def getRootVal(self):
        return self.key

    def setRootVal(self, newVal):
        self.key = newVal

    def getLeftChild(self):
        return self.leftChild

    def getRightChild(self):
        return self.rightChild

    def __str__(self):
        if self.leftChild == None:
            self.leftChild = ''
        if self.rightChild == None:
            self.rightChild = ''
        return f"{self.key}({self.leftChild})({self.rightChild})"
    
class ExpTree (BinaryTree):
    
    def make_tree(postfix):
        s = Stack()
        a = '+-*/^'
        for i in postfix:
            if i not in a:
                s.push(ExpTree(i))
            else:
                t = ExpTree(i)
                t1 = s.pop()
                t2 = s.pop()
                t.rightChild = t1
                t.leftChild = t2
                s.push(t)
        return s.pop()
        
    def __str__(self):
        return ExpTree.inorder(self)

    def preorder(tree):
        s = ""
        if tree != None:
            s += tree.getRootVal()
            s += ExpTree.preorder(tree.getLeftChild())
            s += ExpTree.preorder(tree.getRightChild())
        return s
    
    def postorder(tree):
        s = ""
        if tree != None:
            s += ExpTree.postorder(tree.getLeftChild())
            s += ExpTree.postorder(tree.getRightChild())
            s += tree.getRootVal()
        return s
    
    def inorder2(tree):
        s = ''
        left = tree.getLeftChild()
        if left != None:
            if left.leftChild == None and left.rightChild == None: # if left is leaf node
                s += ExpTree.inorder2(left)
            else:
                s += '(' + ExpTree.inorder2(left) + ')'
        
        s += tree.getRootVal()
        right = tree.getRightChild()
        if right != None:
            if right.leftChild == None and right.rightChild == None: # if right is leaf node
                s += ExpTree.inorder2(right)
            else:
                s += '(' + ExpTree.inorder2(right) + ')'

        return s
    
    def inorder(tree):
        return "(" + ExpTree.inorder2(tree) + ")" # return the output string with outer parenthesis
    
        
    
    def evaluate(tree):
        if tree.rightChild is None and tree.leftChild is None: # check if leaf node
            return tree.getRootVal()
        else:
            op1 = float(ExpTree.evaluate(tree.getLeftChild()))
            op2 = float(ExpTree.evaluate(tree.getRightChild()))
            op = str(tree.getRootVal())
            # check which operation to apply
            if op == '+':
                return op1 + op2
            elif op == '-':
                return op1 - op2
            elif op == '*':
                return op1 * op2
            elif op == '/':
                return op1 / op2
            elif op == '^':
                return op1 ** op2
            else:
                return None

# a driver for testing BinaryTree and ExpTree
if __name__ == '__main__':
    # test a BinaryTree
    
    r = BinaryTree('a')
    assert r.getRootVal() == 'a'
    assert r.getLeftChild()== None
    assert r.getRightChild()== None
    assert str(r) == 'a()()'
    
    r.insertLeft('b')
    assert r.getLeftChild().getRootVal() == 'b'
    assert str(r) == 'a(b()())()'
    
    r.insertRight('c')
    assert r.getRightChild().getRootVal() == 'c'
    assert str(r) == 'a(b()())(c()())'
    
    r.getLeftChild().insertLeft('d')
    r.getLeftChild().insertRight('e')
    r.getRightChild().insertLeft('f')
    assert str(r) == 'a(b(d()())(e()()))(c(f()())())'
    assert str(r.getRightChild()) == 'c(f()())()'
    assert r.getRightChild().getLeftChild().getRootVal() == 'f'
    
    # test an ExpTree
    
    postfix = '5 2 3 * +'.split()
    tree = ExpTree.make_tree(postfix)
    assert str(tree) == '(5+(2*3))'
    assert ExpTree.inorder(tree) == '(5+(2*3))'
    assert ExpTree.postorder(tree) == '523*+'
    assert ExpTree.preorder(tree) == '+5*23'
    assert ExpTree.evaluate(tree) == 11.0
    postfix = '5 2 + 3 *'.split()
    tree = ExpTree.make_tree(postfix)
    assert str(tree) == '((5+2)*3)'
    assert ExpTree.inorder(tree) == '((5+2)*3)'
    assert ExpTree.postorder(tree) == '52+3*'
    assert ExpTree.preorder(tree) == '*+523'
    assert ExpTree.evaluate(tree) == 21.0