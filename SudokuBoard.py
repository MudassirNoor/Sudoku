#!/usr/bin/env python3
import Solver

class SudokuBoard:
    DIMENSION = 9
    SUBMATRIXDIMENSION = 3
    def __init__(self):
        self._grid = [[0] * self.DIMENSION for i in range(self.DIMENSION)]

    def GetPositionValue(self, row, column):
        return self._grid[row][column]

    def UpdatePosition(self, row, column, digit):
        self._grid[row][column] = digit

    def ValidRow(self, digit, row):
        for column in range(SudokuBoard.DIMENSION):
            if self._grid[row][column] == digit:
                return False
        return True

    def ValidColumn(self, digit, column):
        for row in range(SudokuBoard.DIMENSION):
            if self._grid[row][column] == digit:
                return False
        return True

    def ValidSubmatrix(self, digit, row, column):
        subMatrix = Solver.CreateSubMatrix(self._grid, row, column)
        for row in range(SudokuBoard.SUBMATRIXDIMENSION):
            for column in range(SudokuBoard.SUBMATRIXDIMENSION):
                if subMatrix[row][column] == digit:
                    return False
        return True

    def ValidDigit(self, digit, row, column):
        if digit < 1 or digit > 9:
            return False
        if not self.ValidRow(digit, row):
            return False
        if not self.ValidColumn(digit, column):
            return False
        if not self.ValidSubmatrix(digit, row, column):
            return False

        return True
