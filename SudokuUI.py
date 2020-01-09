#!/usr/bin/env python3
from tkinter import *
import PuzzleGenerator
import Solver

difficulty = {"Easy" : 40, "Medium" : 70, "Hard" : 80}
gameFrameDimension = 450
gridDimension = 50

def CreateUI():
    root = Tk()
    Sudoku(root)
    root.mainloop()

def makeGridTag(row, column):
    return 'G' + str(row) + str(column)

def makeTextTag(xCoord, yCoord):
    return 'T' + str(xCoord) + str(yCoord)

def getTextPosition(xFinal, xInitial, yFinal, yInitial):
   xCoord = (xFinal - xInitial) / 2 + xInitial
   yCoord = (yFinal - yInitial) / 2 + yInitial

   return xCoord, yCoord

class GridInfo:
    def __init__(self, gridInfo, textPosition):
        self._gridPosition = gridInfo
        self._textPosition = textPosition
        self._rewritable = False
        self._selected = False

    def getGridTag(self):
        return makeGridTag(self._gridPosition[0], self._gridPosition[1])

    def getTextTag(self):
        return makeTextTag(self._textPosition[0], self._textPosition[1])

class Sudoku(object):

    def __init__(self, parent):
        self._root = parent
        self._root.title("Sudoku")
        self._frame = Frame(parent)
        self._frame.pack()

        newGameButton = Button(self._frame, text="New Game", command=self.openGameFrame)
        newGameButton.pack()

        self._difficulty = StringVar(self._frame)
        self._difficulty.set(list(difficulty.keys())[0])
        self.createDifficultyMenu()

    def createDifficultyMenu(self):
        options = OptionMenu(self._frame, self._difficulty, *tuple(list(difficulty.keys())))
        options.pack()

    def hide(self):
        self._root.withdraw()

    def openGameFrame(self):
        self.hide()
        subFrame = GameWindow(self, self.getDifficulty())

    def getDifficulty(self):
        selectedDifficulty = self._difficulty.get()
        return difficulty.get(str(selectedDifficulty))

    def makeVisible(self):
        self._root.update()
        self._root.deiconify()

class GameWindow(Toplevel):

    def __init__(self, original, difficulty):
        Toplevel.__init__(self)
        self._originalframe = original
        self._optionsBar = Frame(self, bd = 3)
        self._canvas = Canvas(self, height = gameFrameDimension, width = gameFrameDimension, bg ="white")
        self._canvas.grid(row = 0, column = 0, rowspan = 8, columnspan = 8)
        self._board = PuzzleGenerator.GenerateRandomBoard(difficulty)
        self._gridInfos = []

        self.createWindow()

    def createWindow(self):
        self.makeSideBar()
        self.drawGrid()
        self.displayGameObject()
        self._canvas.bind('<Button-1>', self._canvas.focus_set())
        key = lambda event: self.keyPress(event)
        self._canvas.bind('<Key>', key)

    def makeSideBar(self):
        self._optionsBar.grid(row = 8, column = 0, columnspan = 9)

        clearButton = Button(self._optionsBar, text ="Clear", command = self.clearEntries)

        quitGameButton = Button(self._optionsBar, text ="Quit Game", command= self.close)

        hintButton = Button(self._optionsBar, text ='Hint')
        hintButton.bind('<ButtonPress-1>', self.hint)
        hintButton.bind('<ButtonRelease-1>', self.unHint)

        solveButton = Button(self._optionsBar, text="Solve Yourself", command= self.solve)

        solveButton.grid(column = 4, row = 0)
        clearButton.grid(column = 3, row = 0)
        quitGameButton.grid(column = 1, row = 0)
        hintButton.grid(column =2, row = 0)

    def drawGrid(self):
        yFinal = 0
        matrixRow = 0
        for yInitial in range(0, gameFrameDimension, gridDimension):
            xFinal = gameFrameDimension / 9
            yFinal += gridDimension
            matrixColumn = 0

            for xInitial in range(0, gameFrameDimension, gridDimension):
                tag = makeGridTag(matrixRow, matrixColumn)
                gridPosition = (matrixRow, matrixColumn)
                textPosition = getTextPosition(xFinal, xInitial, yFinal, yInitial)
                newGrid = GridInfo(gridPosition, textPosition)
                self._gridInfos.append(newGrid)

                self._canvas.create_rectangle(xInitial, yInitial, xFinal, yFinal, tag = tag)
                matrixColumn += 1
                xFinal += gridDimension

            matrixRow += 1

        for xInitial in (150, 300):
            self._canvas.create_line(0, xInitial, gameFrameDimension, xInitial, fill ="magenta", width = 3)
            self._canvas.create_line(xInitial, 0, xInitial, gameFrameDimension, fill ="magenta", width = 3)

    def displayGameObject(self):
        for gridInfo in self._gridInfos:
            row = gridInfo._gridPosition[0]
            column = gridInfo._gridPosition[1]
            value = self._board.getPositionValue(row, column)

            if value != 0:
                self._canvas.create_text(gridInfo._textPosition[0], gridInfo._textPosition[1], text = value)
            else:
                gridInfo._rewritable = True
                textTag = gridInfo.getTextTag()
                self._canvas.itemconfig(gridInfo.getGridTag(), fill = 'yellow')

                self._canvas.create_text(gridInfo._textPosition[0], gridInfo._textPosition[1], text="_", tag = textTag)
                selectionCall = lambda event, object = gridInfo: self.select(event, object)
                self._canvas.tag_bind(textTag, '<Button-1>', selectionCall)
                self._canvas.tag_bind(gridInfo.getGridTag(), '<Button-1>', selectionCall)

    def select(self, event,object):
        object : GridInfo
        element = self._canvas.find_withtag(object.getGridTag())
        self.unselect(object.getGridTag())
        if not object._selected:
            self._canvas.itemconfig(element, fill ='blue')
            object._selected = True
        else:
            self._canvas.itemconfig(element, fill ='yellow')
            object._selected = False

    def unselect(self, currentTag):
        for gridInfo in self._gridInfos:
            if gridInfo._selected and gridInfo.getGridTag() != currentTag:
                element = self._canvas.find_withtag(gridInfo.getGridTag())
                self._canvas.itemconfig(element, fill='yellow')
                gridInfo._selected = False

    def keyPress(self, event):
        grid = self.getSelectedGrid()
        grid : GridInfo
        if grid == None:
            return
        if event.keysym == 'BackSpace':
            element = self._canvas.find_withtag(grid.getTextTag())
            self._canvas.delete(element)
            self._canvas.create_text(grid._textPosition[0], grid._textPosition[1], text = "_", tag = grid.getTextTag())
            self._board.updatePosition(grid._gridPosition[0], grid._gridPosition[1], 0)

        if event.char in "123456789" and event.char != '':
            element = self._canvas.find_withtag(grid.getTextTag())
            self._canvas.delete(element)
            self._canvas.create_text(grid._textPosition[0], grid._textPosition[1], text = event.char, tag = grid.getTextTag())
            self._board.updatePosition(grid._gridPosition[0], grid._gridPosition[1], int(event.char))
            #TODO: add check win entry

    def getSelectedGrid(self):
        for gridInfo in self._gridInfos:
            if gridInfo._selected:
                return gridInfo

    def clearEntries(self):
        for gridInfo in self._gridInfos:
            if not gridInfo._rewritable:
                continue
            self._board.updatePosition(gridInfo._gridPosition[0], gridInfo._gridPosition[1], 0)
            element = self._canvas.find_withtag(gridInfo.getTextTag())
            self._canvas.delete(element)
            self._canvas.create_text(gridInfo._textPosition[0], gridInfo._textPosition[1], text= "_", tag=gridInfo.getTextTag())

    def hint(self, event):
        for gridInfo in self._gridInfos:
            gridInfo : GridInfo
            value = self._board.getPositionValue(gridInfo._gridPosition[0], gridInfo._gridPosition[1])

            if gridInfo._rewritable and value != 0:
                valid = self._board.validDigit(value, gridInfo._gridPosition[0], gridInfo._gridPosition[1])
                element = self._canvas.find_withtag(gridInfo.getGridTag())
                if not valid:
                    self._canvas.itemconfig(element, fill='red')
                else:
                    self._canvas.itemconfig(element, fill='cyan')

    def unHint(self, event):
        for gridInfo in self._gridInfos:
            gridInfo : GridInfo
            if gridInfo._rewritable:
                element = self._canvas.find_withtag(gridInfo.getGridTag())
                self._canvas.itemconfig(element, fill='yellow')

    def solve(self):
        Solver.BackTrackSolver(self._board)
        for gridInfo in self._gridInfos:
            gridInfo : GridInfo
            if gridInfo._rewritable:
                value = self._board.getPositionValue(gridInfo._gridPosition[0], gridInfo._gridPosition[1])
                element = self._canvas.find_withtag(gridInfo.getTextTag())
                self._canvas.delete(element)
                self._canvas.create_text(gridInfo._textPosition[0], gridInfo._textPosition[1], text= str(value),
                                         tag=gridInfo.getTextTag(), fill = 'red')


    def close(self):
        self.destroy()
        self._originalframe.makeVisible()
