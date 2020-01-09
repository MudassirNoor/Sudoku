#!/usr/bin/env python3
import copy
import random
from SudokuBoard import SudokuBoard
import Solver

def GenerateRandomBoard(unfilledPositions):
    newGameBoard = SudokuBoard()
    Solver.BackTrackSolver(newGameBoard, True)
    RandomlyRemoveNumbersFromBoard(newGameBoard, unfilledPositions)
    return newGameBoard

def RandomlyRemoveNumbersFromBoard(gameBoard, unfilledPositions):
    copiedGameBoard = copy.deepcopy(gameBoard)
    for i in range(1, unfilledPositions):
        row = random.randrange(0, SudokuBoard.DIMENSION)
        column = random.randrange(0, SudokuBoard.DIMENSION)
        copiedGameBoard.updatePosition(row, column, 0)

        solved = Solver.BackTrackSolver(copiedGameBoard)
        if solved:
            gameBoard.updatePosition(row, column, 0)

    del copiedGameBoard