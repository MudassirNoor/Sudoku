#!/usr/bin/env python3
import Solver
import PuzzleGenerator

def main():
    gameBoard = PuzzleGenerator.GenerateRandomBoard()
    Solver.printGrid(gameBoard.Grid)
    print("After solving: \n")
    Solver.BackTrackSolver(gameBoard)
    Solver.printGrid(gameBoard.Grid)

    return 0

if __name__ == '__main__': main()