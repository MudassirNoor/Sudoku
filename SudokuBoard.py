#!/usr/bin/env python3
import Solver

class SudokuBoard:
    DIMENSION = 9
    SUBMATRIXDIMENSION = 3
    def __init__(self):
        self._grid = [[0] * self.DIMENSION for i in range(self.DIMENSION)]

    def getPositionValue(self, row, column):
        return self._grid[row][column]

    def updatePosition(self, row, column, digit):
        self._grid[row][column] = digit

    def validRow(self, digit, row):
        for column in range(SudokuBoard.DIMENSION):
            if self._grid[row][column] == digit:
                return False
        return True

    def validColumn(self, digit, column):
        for row in range(SudokuBoard.DIMENSION):
            if self._grid[row][column] == digit:
                return False
        return True

    def validSubmatrix(self, digit, row, column):
        subMatrix = Solver.CreateSubMatrix(self._grid, row, column)
        for row in range(SudokuBoard.SUBMATRIXDIMENSION):
            for column in range(SudokuBoard.SUBMATRIXDIMENSION):
                if subMatrix[row][column] == digit:
                    return False
        return True

    def validDigit(self, digit, row, column):
        if digit < 1 or digit > 9:
            return False
        if not self.validRow(digit, row):
            return False
        if not self.validColumn(digit, column):
            return False
        if not self.validSubmatrix(digit, row, column):
            return False

        return True
