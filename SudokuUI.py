#!/usr/bin/env python3
from tkinter import *
import PuzzleGenerator

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

        self.difficulty = StringVar(self._frame)
        self.difficulty.set(list(difficulty.keys())[0])
        self.createDifficultyMenu()

    def createDifficultyMenu(self):
        options = OptionMenu(self._frame, self.difficulty, *tuple(list(difficulty.keys())))
        options.pack()

    def hide(self):
        self._root.withdraw()

    def openGameFrame(self):
        self.hide()
        subFrame = GameWindow(self)

    def makeVisible(self):
        self._root.update()
        self._root.deiconify()

class GameWindow(Toplevel):

    def __init__(self, original):
        Toplevel.__init__(self)
        self._originalframe = original
        self._optionsBar = Frame(self, bd = 3)
        self._canvas = Canvas(self, height = gameFrameDimension, width = gameFrameDimension, bg ="white")
        self._canvas.grid(row = 0, column = 0, rowspan = 8, columnspan = 8)
        self._board = PuzzleGenerator.GenerateRandomBoard()
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
        clear = Button(self._optionsBar, text ="Clear", command = self.clearEntries)
        quitGameButton = Button(self._optionsBar, text ="Quit Game", command= self.close)
        clear.grid(column = 4, row = 0)
        quitGameButton.grid(column = 2, row = 0)
        #TODO: add a timer window
        #TODO: add hint option

    def drawGrid(self):
        yFinal = 0
        matrixRow = 0
        for yInitial in range(0, gameFrameDimension, gridDimension):
            xFinal = 50
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
            self._canvas.create_line(0, xInitial, gameFrameDimension, xInitial, fill ="red", width = 2)
            self._canvas.create_line(xInitial, 0, xInitial, gameFrameDimension, fill ="red", width = 2)

    def displayGameObject(self):
        for gridInfo in self._gridInfos:
            row = gridInfo._gridPosition[0]
            column = gridInfo._gridPosition[1]
            value = self._board.GetPositionValue(row, column)

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
            self._canvas.itemconfig(element, fill ='white')
            object._selected = False

    def unselect(self, currentTag):
        for gridInfo in self._gridInfos:
            if gridInfo._selected and gridInfo.getGridTag() != currentTag:
                element = self._canvas.find_withtag(gridInfo.getGridTag())
                self._canvas.itemconfig(element, fill='white')
                gridInfo._selected = False

    def keyPress(self, event):
        grid = self.getSelectedGrid()
        grid : GridInfo
        try:
            if event.char in "123456789":
                element = self._canvas.find_withtag(grid.getTextTag())
                self._canvas.delete(element)
                self._canvas.create_text(grid._textPosition[0], grid._textPosition[1], text = event.char, tag = grid.getTextTag())
                self._board.UpdatePosition(grid._gridPosition[0], grid._gridPosition[1], int(event.char))
        except:
            pass

    def getSelectedGrid(self):
        for gridInfo in self._gridInfos:
            if gridInfo._selected:
                return gridInfo

    def clearEntries(self):
        for gridInfo in self._gridInfos:
            if not gridInfo._rewritable:
                continue
            self._board.UpdatePosition(gridInfo._gridPosition[0], gridInfo._gridPosition[1], 0)
            element = self._canvas.find_withtag(gridInfo.getTextTag())
            self._canvas.delete(element)
            self._canvas.create_text(gridInfo._textPosition[0], gridInfo._textPosition[1], text= "_", tag=gridInfo.getTextTag())

    def close(self):
        self.destroy()
        self._originalframe.makeVisible()
