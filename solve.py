import numpy as np
import sys

# Opening file to get the sudoku matrix
def open_file(filename):
    with open(filename) as file:
        for line in file.readlines():
            grid.append(line.strip().split(" "))


# Sudoku Solver function
def solve():
    for x in range(9):
        for y in range(9):
            if grid[x][y] == '0':
                for n in range(1,10):
                    if check(x,y,n):
                        grid[x][y] = str(n)
                        solve()
                        grid[x][y] = '0'
                return

    print(np.matrix(grid))
    input("More?")


# Check for an existing number in row column or inner square
def check(x,y,n):
    for i in range(9):
        if grid[x][i] == str(n):
            return False
        if grid[i][y] == str(n):
            return False
        
    x0 = (x//3) * 3
    y0 = (y//3) * 3

    for i in range(0,3):
        for j in range(0,3):
            if grid[x0+i][y0+j] == str(n):
                return False

    return True

# Main function()
if __name__ == "__main__":
    grid=list()
    filename = sys.argv[1]
    open_file(filename)
    solve()