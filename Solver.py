#!/usr/bin/env python3
import random
from SudokuBoard import SudokuBoard

def printGrid(grid):
    for row in grid:
        for column in row:
            print(column, end = " ")
        print()

def BackTrackSolver(sudokuBoard, generate=False):
    isSolved = False
    assigned, row, column = UnassignedPosition(sudokuBoard.Grid)

    if not assigned:
        return True

    for digit in range(1, 10):
        if generate:
            value = random.randrange(1, 10)
        else:
            value = digit

        if not sudokuBoard.ValidDigit(value, row, column):
            continue

        sudokuBoard.UpdatePosition(row, column, value)
        isSolved = BackTrackSolver(sudokuBoard, generate)

        if not isSolved:
            sudokuBoard.UpdatePosition(row, column, 0)
        else:
            break

    return isSolved

def CreateSubMatrix(grid, row, column):
    # Convert current row and column into a position in 3x3 submatrix
    currentRowPosition = row % 3
    currentColumnPosition = column % 3

    upperRowRange, lowerRowRange = Get3x3ConvertedPositions(currentRowPosition, row)
    upperColumnRange, lowerColumnRange = Get3x3ConvertedPositions(currentColumnPosition, column)

    subMatrix = []
    subRow = 0
    for r in range(lowerRowRange, upperRowRange):
        subMatrix.append([])
        for c in range(lowerColumnRange, upperColumnRange):
            subMatrix[subRow].append(grid[r][c])
        subRow += 1

    return subMatrix

def Get3x3ConvertedPositions(remainder, givenPosition):
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

def UnassignedPosition(grid):
    for row in range(SudokuBoard.DIMENSION):
        for column in range(SudokuBoard.DIMENSION):
            if grid[row][column] == 0:
                    return True, row, column
    return False, 0, 0
