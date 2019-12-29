#!/usr/bin/env python3
DIMENSION = 9
SUBMATRIXDIMENSION = 3
GRID = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]]

def printGrid(grid):
    for row in grid:
        for column in row:
            print(column, end = " ")
        print()

def UnassignedPosition():
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            if GRID[row][column] == 0:
                return True, row, column
    return False, 0, 0

def IsRowValid(digit, row):
    for column in range(DIMENSION):
        if GRID[row][column] == digit:
            return False
    return True

def IsColumnValid(digit, column):
    for row in range(DIMENSION):
        if GRID[row][column] == digit:
            return False
    return True

def IsSubMatrixValid(digit, row, column):
    subMatrix = CreateSubMatrix(row, column)
    for row in range(SUBMATRIXDIMENSION):
        for column in range(SUBMATRIXDIMENSION):
            if subMatrix[row][column] == digit:
                return False
    return True

def Get3x3ConvertedPositions(remainder, givenPosition):
    upperBound = 1
    lowerBound = 0
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

def CreateSubMatrix(row, column):
    #Convert current row and column into a position in 3x3 submatrix
    currentRowPosition = row % 3
    currentColumnPosition = column % 3

    upperRowRange, lowerRowRange = Get3x3ConvertedPositions(currentRowPosition, row)
    upperColumnRange, lowerColumnRange = Get3x3ConvertedPositions(currentColumnPosition, column)

    subMatrix = []
    subRow = 0
    for r in range(lowerRowRange, upperRowRange):
        subMatrix.append([])
        for c in range(lowerColumnRange, upperColumnRange):
            subMatrix[subRow].append(GRID[r][c])
        subRow +=1

    return subMatrix

def isDigitValid(digit, row, column):
    if digit < 1 or digit > 9:
        return False
    if not IsRowValid(digit, row):
        return False
    if not IsColumnValid(digit, column):
        return False
    if not IsSubMatrixValid(digit, row, column):
        return False

    return True

def BackTrackSolver():
    isSolved = False
    isUnassigned, row, column = UnassignedPosition()

    if not isUnassigned:
        return True

    for digit in range(1, 10):
        if not isDigitValid(digit, row, column):
            continue

        GRID[row][column] = digit
        isSolved = BackTrackSolver()

        if not isSolved:
            GRID[row][column] = 0
        else:
            break

    return isSolved

def main():
    printGrid(GRID)
    print("After solving: \n")
    BackTrackSolver()
    printGrid(GRID)

    # sub = CreateSubMatrix(3, 3)
    # printGrid(sub)

    return 0

if __name__ == '__main__':main()



