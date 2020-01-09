#!/usr/bin/env python3
import Solver

def calculate3x3Position(v):
    return v % 3

class SudokuBoard:
    DIMENSION = 9
    SUBMATRIXDIMENSION = 3
    def __init__(self):
        self._grid = [[0] * self.DIMENSION for i in range(self.DIMENSION)]

    def getPositionValue(self, row, column):
        return self._grid[row][column]

    def updatePosition(self, row, column, digit):
        self._grid[row][column] = digit

    def validRow(self, digit, row, column):
        for c in range(SudokuBoard.DIMENSION):
            if c != column:
                if self._grid[row][c] == digit:
                    return False
        return True

    def validColumn(self, digit, row, column):
        for r in range(SudokuBoard.DIMENSION):
            if r != row:
                if self._grid[r][column] == digit:
                    return False
        return True

    def validSubmatrix(self, digit, row, column):
        subMatrix = self.createSubMatrix(row, column)
        currentRowInSubmatrix = calculate3x3Position(row)
        currentColumnInSubmatrix = calculate3x3Position(column)

        for r in range(SudokuBoard.SUBMATRIXDIMENSION):
            for c in range(SudokuBoard.SUBMATRIXDIMENSION):
                if r != currentRowInSubmatrix and c != currentColumnInSubmatrix:
                    if subMatrix[r][c] == digit:
                        return False
        return True

    def validDigit(self, digit, row, column):
        if digit < 1 or digit > 9:
            return False
        if not self.validRow(digit, row, column):
            return False
        if not self.validColumn(digit, row, column):
            return False
        if not self.validSubmatrix(digit, row, column):
            return False

        return True

    def createSubMatrix(self, row, column):
        currentRowPosition = calculate3x3Position(row)
        currentColumnPosition = calculate3x3Position(column)

        upperRowRange, lowerRowRange = self.getMainGridRange(currentRowPosition, row)
        upperColumnRange, lowerColumnRange = self.getMainGridRange(currentColumnPosition, column)

        subMatrix = []
        subRow = 0
        for r in range(lowerRowRange, upperRowRange):
            subMatrix.append([])
            for c in range(lowerColumnRange, upperColumnRange):
                subMatrix[subRow].append(self._grid[r][c])
            subRow += 1

        return subMatrix

    def getMainGridRange(self, remainder, givenPosition):
        upperBound = 1
        if remainder == 2:
            upperBound += givenPosition
            lowerBound = givenPosition - 2
        elif remainder == 0:
            upperBound += givenPosition + 2
            lowerBound = givenPosition
        else:
            upperBound += givenPosition + 1
            lowerBound = givenPosition - 1

        return upperBound, lowerBound

    def checkFinishedBoard(self):
        existsUnassigned = Solver.UnassignedPosition(self._grid)[0]
        if existsUnassigned:
            return False

        for row in self.DIMENSION:
            for column in self.DIMENSION:
                valid = self.validDigit(self._grid[row][column], row, column)
                if not valid:
                    return False

        return True
