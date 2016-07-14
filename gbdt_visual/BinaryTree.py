#coding=gbk

import sys
import os
import pygraphviz as pgv


'''
Ilustrate the create binary tree with user input
inorder travel 
'''
class Node():
    '''
    node will be used in BinaryTree
    '''
    def __init__(self, left = None, right = None):
        self.atrr = {}
        self.leftEdgeAttr = {}
        self.rightEdgeAttr = {}
        self.left = left
        self.right = right
    
    def __str__(self):
        return str(self.elem)

class BinaryTree():
    def __init__(self,root = None):
        self.root = root
    
    def createTree(self, endMark = -1):
        '''create a binary tree with user input'''
        def createTreeHelp(endMark = -1):
            elem = raw_input();
            if (elem == str(endMark)):
                return None
            root = Node(elem)
            root.left = createTreeHelp(endMark)
            root.right = createTreeHelp(endMark)
            return root        
        #print('Please input the binary tree data wit ' + str(endMark) +' as endmark')        
        elem = raw_input()
        self.root = Node(elem)
        self.root.left = createTreeHelp(endMark)
        self.root.right = createTreeHelp(endMark)
        
    def inorderTravel(self):
        def inorderTravelHelp(root):
            if not root:
                return 
            inorderTravelHelp(root.left)
            print(root)
            inorderTravelHelp(root.right)        
        inorderTravelHelp(self.root)




class TreeWriter():

    def __init__(self, tree):

        self.num = 1 #mark each visible node as its key
        self.num2 = -1 #makk each invisible node as its key
        self.tree = tree
        self.use_invisable_node = False

    def Write(self, outfile = 'tree.png'):
        
        def writeHelp(root, A):
            if not root:
                return
            p = str(self.num)
            self.num += 1
            A.add_node(p, **root.attr)
            q = None
            r = None
            if root.left:
                q = writeHelp(root.left, A)
                A.add_edge(p, q, **root.leftEdgeAttr)
            if root.right:
                r = writeHelp(root.right, A)
                A.add_edge(p, r, **root.rightEdgeAttr)
   
            if not self.use_invisable_node:
                return p

            if q or r:
                if not q:
                    q = str(self.num2)
                    self.num2 -= 1
                    A.add_node(q, style = 'invis')
                    A.add_edge(p, q, style = 'invis')
                if not r:
                    r = str(self.num2)
                    self.num2 -= 1
                    A.add_node(r, style = 'invis')
                    A.add_edge(p, r, style = 'invis')
                l = str(self.num2)
                self.num2 -= 1
                A.add_node(l, style = 'invis')
                A.add_edge(p, l, style = 'invis')
                B = A.add_subgraph([q, l, r], rank = 'same')
                B.add_edge(q, l, style = 'invis')
                B.add_edge(l, r, style = 'invis')

            return p #return key root node
        self.A = pgv.AGraph(directed=True,strict=True)
        writeHelp(self.tree.root, self.A)
        self.A.graph_attr['epsilon']='0.001'
        #self.A.layout(prog='dot')
        #print self.A.string() # print dot file to standard output
            
        self.A.layout('dot') # layout with dot
        self.A.draw(outfile) # write to file

