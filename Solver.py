#!/usr/bin/env python3
import random
from SudokuBoard import *

def printGrid(grid):
    for row in grid:
        for column in row:
            print(column, end = " ")
        print()

def BackTrackSolver(sudokuBoard, generate=False):
    isSolved = False
    existsUnassigned, row, column = UnassignedPosition(sudokuBoard._grid)

    if not existsUnassigned:
        return True

    for digit in range(1, 10):
        if generate:
            value = random.randrange(1, 10)
        else:
            value = digit

        if not sudokuBoard.validDigit(value, row, column):
            continue

        sudokuBoard.updatePosition(row, column, value)
        isSolved = BackTrackSolver(sudokuBoard, generate)

        if not isSolved:
            sudokuBoard.updatePosition(row, column, 0)
        else:
            break

    return isSolved

def UnassignedPosition(grid):
    for row in range(SudokuBoard.DIMENSION):
        for column in range(SudokuBoard.DIMENSION):
            if grid[row][column] == 0:
                    return True, row, column
    return False, 0, 0
