#!/usr/bin/env python3
from tkinter import *

difficulty = {"Easy" : 40, "Medium" : 70, "Hard" : 80}

def CreateUI():
    root = Tk()
    app = Sudoku(root)

    root.mainloop()


    return 0

class GameWindow(Toplevel):

    def __init__(self, original):
        self.original_frame = original
        Toplevel.__init__(self)
        self.geometry("500x500")
        self.sideBar = Frame(self, bg = "red", bd = 3)
        self.gameFrame = Frame(self, bg = "blue", bd = 3)

        self.makeSideBar()
        self.makeGameFrame()


    def makeSideBar(self):
        self.sideBar.grid(row = 8, column = 0, columnspan = 9)
        resetButton = Button(self.sideBar, text = "Reset") #TODO: add reset functionality to recreate board
        quitGameButton = Button(self.sideBar, text = "Quit Game", command= self.close)
        resetButton.grid(column = 4, row = 0)
        quitGameButton.grid(column = 2, row = 0)
        #TODO: perhaps add a timer window

    def makeGameFrame(self):
        self.gameFrame.grid(row = 0, rowspan = 8, columnspan = 8)
        selectedDifficulty = self.original_frame.difficulty

    def close(self):
        self.destroy()
        self.original_frame.makeVisible()


class Sudoku(object):

    def __init__(self, parent):
        self.root = parent
        self.root.title("Sudoku")
        self.frame = Frame(parent)
        self.frame.pack()

        newGameButton = Button(self.frame, text="New Game", command=self.openGameFrame)
        newGameButton.pack()

        self.difficulty = StringVar(self.frame)
        self.difficulty.set(list(difficulty.keys())[0])
        self.createDifficultyMenu()

    def createDifficultyMenu(self):
        options = OptionMenu(self.frame, self.difficulty, *tuple(list(difficulty.keys())))
        options.pack()

    def hide(self):
        self.root.withdraw()

    def openGameFrame(self):
        self.hide()
        subFrame = GameWindow(self)

    def makeVisible(self):
        self.root.update()
        self.root.deiconify()
