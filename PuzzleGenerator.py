#!/usr/bin/env python3
import copy
import random
from SudokuBoard import SudokuBoard
import Solver

def GenerateRandomBoard():
    newGameBoard = SudokuBoard()
    Solver.BackTrackSolver(newGameBoard, True)
    RandomlyRemoveNumbersFromBoard(newGameBoard)
    return newGameBoard

def RandomlyRemoveNumbersFromBoard(gameBoard):
    copiedGameBoard = copy.deepcopy(gameBoard)
    for i in range(1, 30):
        row = random.randrange(0, SudokuBoard.DIMENSION)
        column = random.randrange(0, SudokuBoard.DIMENSION)
        copiedGameBoard.UpdatePosition(row, column, 0)

        solved = Solver.BackTrackSolver(copiedGameBoard)
        if solved:
            gameBoard.UpdatePosition(row, column, 0)

    del copiedGameBoard