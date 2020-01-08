
# Sudoku


import copy # importing copy module


# Part A: Get Grid
# Input: a file name file name, where the file contains n lines, and each line contains n entries separated by commas. Each entry will either be a positive integer, or the letter ‘x’.
# Output: a table represented as a nested list, where each entry in the orignal file is an element in the table, and all numbers have been converted to integers.

def grid_from_file(file_name):
    f = open(file_name)
    contents = f.readlines()
    outfile = []
    for line in contents:  # reading each line as string
        example_list = [k for k in line.rstrip().split(',')]  # converting each element in the each line to integer
        outfile.append(example_list)
    f.close()

    for i in range(len(outfile)):
        for j in range(len(outfile)):
            element = outfile[i][j]
            if element.isnumeric() == True:
                outfile[i][j] = int(element)

    return outfile



# Part B: Valid Entry (1 Mark)
# Function subgrid_values was implemented in answering tackling this problem.
# This function was implemented  for returning sub grids of the grids.

# Input: a nested list grid, that represents an n × n sudoku grid; each item in the inner list is either an integer (example 13), or the string ‘x’; a positive integer num, where 0 < num ≤ n; and two non-negative integers r and c that represent the row and column that num will be inserted, where 0 ≤ r, c < n. You may assume grid[r][c]==‘x’.
# Output: a boolean True if the insertion is valid; otherwise False. For the insertion to be valid, it must result in a grid that does not contain duplicate numbers in any row, any column, or any subgrid.

def subgrid_values(grid, row, col):
    val = []
    n = int(len(grid)**(0.5))   # get dimension of inner box
    r = (row//n)*n   # get starting row
    c = (col//n)*n   # get starting col
    for i in range(r, r+n):
        for j in range(c, c+n):
            val.append(grid[i][j])
    return val


def validate_subgrid(grid, num, row, col):
    subGrid = subgrid_values(grid, row, col)
    for i in range(len(subGrid)):
        if subGrid[i] == num:
            return True
    return False


def validate_row(grid, num, row):
    for i in range(len(grid)):
        if(grid[row][i] == num):
            return True
    return False


def validate_col(grid, num, col):
    for i in range(len(grid)):
        if(grid[i][col] == num):
            return True
    return False


def valid_entry(grid, num, r, c):
    row, col = r, c
    if grid[r][c] == 'x':
        if (validate_row(grid, num, row) == False) and (validate_col(grid, num, col) == False) and (validate_subgrid(grid, num, row, col) == False):
            return True
        else:
            return False
    else:
        return False



# Part C: The function implementation below returns the complete list of valid augmented grids, where each grid contains num in row r.
# Input: a nested list grid, that represents a valid n × n sudoku grid; each item in the inner list is either an integer (example 27), or the string ‘x’; a positive integer num, where 0 < num ≤ n; and a non-negative integer r, where 0 ≤ r < n.
# Output: a nested list containing all augmented sudoku grids such that each grid is valid, and each grid contains num in row r. If num is in row r in the original grid, return a list containing the original grid. If there is no way to augment the given grid to create a valid grid where num is in row r, return an empty list.

def grids_augmented_in_row(grid, num, r):
    output = []
    if num not in grid[r]:
        for c in range(len(grid)):
            if grid[r][c] == 'x':
                if(valid_entry(grid, num, r, c)):
                    gridCopy = copy.deepcopy(grid)
                    gridCopy[r][c] = num
                    output.append(gridCopy)

    else:
        output.append(grid)

    return output




# Part D: This function returns a list of valid n × n grids, where each grid contains n nums. (I.e. if given a 9 ∗ 9 grid, and num = 3, each grid returned must contain nine 3’s.)
# Input: a nested list grid, that represents a valid n × n sudoku grid; each item in the inner list is either an integer (example 13), or the string ‘x’; and a positive integer num, where 0 < num ≤ n.
# Output: a nested list containing all valid sudoku grids where each grid contains n nums. If there is no way to augment the given grid to create a valid sudoku grid containing n nums, return an empty list.

def fill_in(grid, num):
    for r in range(len(grid)):
        for c in range(len(grid)):
            if grid[r][c] == 'x'and (valid_entry(grid, num, r, c)):
                grid[r][c] = num
    return grid


# checking if num is in all rows of the grid
def check_num_in_all_rows(grid, num):
    for r in range(len(grid)):
        if num not in grid[r]:
            return False
    return True


# Generate grids with nums in grid
def generate_grids_with_num(grid, num):
    listOfGrids = []
    for r in range(len(grid)):
        for c in range(len(grid)):
            if grid[r][c] == 'x'and (valid_entry(grid, num, r, c)):
                gridCopy = copy.deepcopy(grid)
                gridCopy[r][c] = num
                matrix = fill_in(gridCopy, num)
                if(check_num_in_all_rows(matrix, num)):
                    listOfGrids.append(matrix)
    return listOfGrids

# Main function
def grids_augmented_with_number(grid, num):
    output = []
    listOfMatrix = generate_grids_with_num(grid, num)
    if len(listOfMatrix) > 0:
        for i in range(len(listOfMatrix)):
            if listOfMatrix[i] not in output:
                output.append(listOfMatrix[i])

    return output




# Part E: Function below finds the solution for the given sudoku. This has been implemented using brute force.
# Input: a file name file name, where the file contains n lines, and each line contains n entries separated by
# commas. Each entry will either be a positive integer, or the letter ‘x’.
# Output: a nested list representing a completed sudoku grid. You may assume the file given will always contain exactly one valid solution.

# Return a list containing possible numbers in a cell.
def count_num(grid, r, c):
    poss = []
    for num in range(1, len(grid)+1):
        if grid[r][c] == 'x' and valid_entry(grid, num, r, c):
            poss.append(num)
    return poss

# Checking if the grid is filled or not
def find_empty_location(grid):
    for r in range(len(grid)):
        for c in range(len(grid)):
            if(grid[r][c] == 'x'):
                return True
    return False

# solver function
def solve(grid):
    while find_empty_location(grid):  # Loop as long as theres an empty cell or a cell with 'x'
        for r in range(len(grid)):
            for c in range(len(grid)):
                size = count_num(grid, r, c)
                if (grid[r][c] == 'x' and len(size) == 1):
                    grid[r][c] = size[0]
    return grid

# Main function
def solve_sudoku(file_name):
    grid = grid_from_file(file_name)
    return solve(grid)
