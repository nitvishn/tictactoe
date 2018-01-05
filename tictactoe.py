#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 17:06:31 2017

@author: vishnuvnittoor
"""
#import os
#import subprocess as sp
#from termcolor import colored
import random
from copy import deepcopy
import os
import time
import math
import pygame

random.seed()

red = (255,0,0)
green = (197,234,124)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
grey=(0, 0, 0)
light_grey=(58, 58, 58)

size=450
import numpy as np
letterDict={'A':0, 'B':1, 'C':2}

def cls():
    for i in range(100):
        print("\n")
    screen.fill(white)
def printBoard(board):

    cls()

    #VERTICAL LINES
    pygame.draw.line(screen, black, (size/3, 0), (size/3, size))
    pygame.draw.line(screen, black, ((size/3)*2, 0), ((size/3)*2, size))

    #HORIZHENTAL LINES
    pygame.draw.line(screen, black, (0, size/3), (size, size/3))
    pygame.draw.line(screen, black, (0, (size/3)*2), (size, (size/3)*2))

    for rownum in range(len(board)):
        for itemnum in range(len(board[rownum])):
            item=board[rownum][itemnum]
            x=int((((itemnum+1)/3)*size)-(size/6))
            y = int((((rownum + 1) / 3) * size) - (size / 6))
            if(item=='O'):
                pygame.draw.circle(screen, red, (x, y), int(size/12), 10)
            elif(item=='X'):
                diag_len=math.sqrt(2*((size/3)*(size/3)))/4
                pygame.draw.line(screen, blue, (x - diag_len, y - diag_len), (x, y), 4)
                pygame.draw.line(screen, blue, (x - diag_len, y + diag_len), (x, y), 4)
                pygame.draw.line(screen, blue, (x + diag_len, y - diag_len), (x, y), 4)
                pygame.draw.line(screen, blue, (x + diag_len, y + diag_len), (x, y), 4)

    # print('   ----------------')
    # for i in range(len(board)):
    #     row=board[i]
    #     print(i+1, end='  ')
    #     print('|', end='')
    #     for mark in row:
    #         if(mark==None):
    #             print('   ', end = ' ')
    #         elif(mark=='X'):
    #             print(' '+'X'+' ', end=' ')
    #         else:
    #             print(' '+'O'+' ', end=' ')
    #         print('|', end='')
    #     print()
    #     print('   ----------------')
    # print('     A    B    C')
def homogenous(myList):
    if(myList==None):
        return False
    L=myList[:]
    item=L.pop()
    if(item==None):
        return False
    for thing in L:
        if(thing!=item):
            return False
    return item
def getColumns(matrix):
    columns=[]
    for i in range(len(matrix)):
        column=[]
        for row in matrix:
            column.append(row[i])
        columns.append(column)
    return columns
def getDiagonals(matrix):
    a = np.array(matrix)
    diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
    return [n.tolist() for n in diags]
def hasWon(board):
    for row in board:
        if(homogenous(row)!=False and len(row)==3):
            return (True, homogenous(row))
    
    for column in getColumns(board):
        if(homogenous(column)!=False and len(column)==3):
            return (True, homogenous(column))

    for diag in getDiagonals(board):
        if(len(diag)==3 and homogenous(diag)):
            return (True, homogenous(diag))
    
    for i in range(len(board)):
        for j in range(len(board[i])):   
            if(board[i][j]==None):
                return (False, None)
    
    return (True, None)
def getEmptySquares(board):
    empty=[]
    if(hasWon(board)[0]):
        return empty
    for i in range(len(board)):
        for j in range(len(board[i])):            
            if(board[i][j]==None):
                empty.append((i, j))
    return empty
def validInput(string, board):
    empty=getEmptySquares(board)
    if(len(string)!=2):
        print("length error")
        return False
    elif(string[0]!='A' and string[0]!='B' and string[0]!='C'):
        print ("Alpha aerror")
        return False
    elif(not(string[1]=='1' or string[1]=='2' or string[1]=='3')):
        print ("numerror")
        return False
    j=letterDict[string[0]]
    i=int(string[1])-1
    if((i, j) not in empty):
        return False
    return True
def getInputAndUpdate(board):
    cls()
    printBoard(board)
    inpt = input('\n\nCoordinates of square: ')
    inpt=inpt.upper()
    while(not(validInput(inpt, board))):
        cls()
        print("Invalid Input")
        printBoard(board)
        inpt = input('Coordinates of square: ')
        inpt = inpt.upper()
    j=letterDict[inpt[0]]
    i=int(inpt[1])-1
    board[i][j]='X'
def boardIsUntouched(board):
    for row in board:
        for item in row:
            if(item!=None):
                return False
    return True
def writeSequence(boardThen, boardNow):
    def getStringOfBoard(board):
        string = ""
        for line in board:
            for item in line:
                if (item == None):
                    string += '_'
                else:
                    string += item
        return string

    file=open("memo.txt", 'a')
    file.write(getStringOfBoard(boardThen))
    file.write(" ")
    file.write(getStringOfBoard(boardNow))
    file.write("\n")

class Node(object):
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn
        self.childs = self.getChilds()
        self.points = None
        self.boardChoice = None
        self.isleaf = False

        if (hasWon(board)[0] == True):
            self.isleaf = True
            if (hasWon(board)[1] == 'O'):
                self.points = 10
            elif (hasWon(board)[1] == 'X'):
                self.points = -10
            else:
                self.points = 0
        else:
            maxPoints = -10
            maxChild = None
            minChild = None
            minPoints = 10
            for child in self.childs:
                if (child.points <= minPoints):
                    minChild = child
                    minPoints = child.points
                if (child.points >= maxPoints):
                    maxChild = child
                    maxPoints = child.points
            if (turn == 'X'):
                self.points = maxPoints
                self.boardChoice = maxChild.board
            else:
                self.points = minPoints
                self.boardChoice = minChild.board

    def isLeaf(self):
        return self.isleaf

    def getChilds(self):
        turn = self.turn
        if (turn == 'O'):
            nextTurn = 'X'
        else:
            nextTurn = 'O'

        def getNextBoards():
            pos = deepcopy(self.board)
            empty = getEmptySquares(pos)
            boards = []
            currentBoard = deepcopy(pos)
            for square in empty:
                currentBoard[square[0]][square[1]] = nextTurn
                boards.append(currentBoard)
                currentBoard = deepcopy(pos)
            return boards

        childs = []
        for board in getNextBoards():
            childs.append(Node(board, nextTurn))
        return childs

    def __str__(self):
        return str(self.board)

    def childs(self):
        return self.childs

def makeMove(board):
    def getSequences():
        file=open("memo.txt", "r")
        seqs={}
        for line in file:
            seq_key=""
            seq_choice=""
            isFirst=True
            for char in line:
                if(char==' '):
                    isFirst=False
                    continue
                elif(char=='\n'):
                    break
                if(isFirst):
                    seq_key+=char
                else:
                    seq_choice+=char
            seqs[seq_key]=seq_choice
        return seqs
    def getBoardFromSequence(seq):
        seq_board = []
        row1 = seq[0:3]
        # row1, @kinson.
        row2 = seq[3:6]
        row3 = seq[6:9]
        list1 = []
        for item in row1:
            if (item == '_'):
                list1.append(None)
                continue
            list1.append(item)
        list2 = []
        for item in row2:
            if (item == '_'):
                list2.append(None)
                continue
            list2.append(item)
        list3 = []
        for item in row3:
            if (item == '_'):
                list3.append(None)
                continue
            list3.append(item)
        seq_board.append(list1)
        seq_board.append(list2)
        seq_board.append(list3)
        return seq_board

    valid_ones=[]
    sequences=getSequences()
    for key in sequences.keys():
        if(getBoardFromSequence(key)==board):
            valid_ones.append(getBoardFromSequence(sequences[key]))
    if(len(valid_ones)!=0):
        return random.choice(valid_ones)
    root=Node(board, 'X')
    writeSequence(board, root.boardChoice)
    return root.boardChoice

random.seed()
board=[[None, None, None], [None, None, None], [None, None, None]]

choice=input("Does computer start?\nY/N : ")
pygame.init()
screen = pygame.display.set_mode((size, size))

if(choice.upper()[0]=='Y'):
    cls()
    print('Thinking...')
    board=deepcopy(makeMove(board))

crashed=False

while not crashed:
    cls()
    printBoard(board)
    pygame.display.update()
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            crashed=True

        if(event.type==pygame.MOUSEBUTTONDOWN):
            x, y=pygame.mouse.get_pos()
            i=None
            if(x>0 and x<size/3):
                i=0
            elif(x>size/3 and x<2*(size/3)):
                i=1
            elif(x>(2*size)/3 and x<size):
                i=2

            j=None
            if (y > 0 and y < size / 3):
                j = 0
            elif (y > size / 3 and y < 2 * (size / 3)):
                j = 1
            elif (y > (2 * size) / 3 and y < size):
                j = 2
            print(i, j)
            if(board[j][i]!=None):
                continue
            board[j][i]='X'
            printBoard(board)
            pygame.display.update()
            if(hasWon(board)[0]==True):
                crashed=True
            else:
                board=deepcopy(makeMove(board))

    if(hasWon(board)[0]!=False):
        crashed=True


printBoard(board)
pygame.display.update()
crashed=False
if(hasWon(board)[1]=='X'):
    #This line is technically unreachable, since you will never win.
    print("YOU'VE JUST WON!")
elif(hasWon(board)[1]=='O'):
    print("LOL YOU LOST HAHA LOL")
else:
    print("DRAW. GOOD JOB.")
while not crashed:
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            crashed=True
