"""
Author: Shervin Tafreshipour
Date: 2021-12-31
"""

import random as randm
from typing import List, Tuple, Set
from copy import deepcopy

"""
Fields representing the unsolved sudoku grid
The grid is a 9x9 matrix of numbers
each sub-matrix is a 3x3 matrix of numbers
The grid is represented as a 2D array of numbers 
"""

grid_1 = [[0,2,0],[8,0,0],[0,3,0]]
grid_2 = [[5,0,1],[2,0,3],[0,6,0]]
grid_3 = [[0,9,0],[0,0,6],[0,7,0]]
grid_4 = [[0,0,1],[5,4,0],[0,0,2]]
grid_5 = [[0,0,0],[0,0,0],[0,0,0]]
grid_6 = [[6,0,0],[0,1,9],[7,0,0]]
grid_7 = [[0,9,0],[2,0,0],[0,1,0]]
grid_8 = [[0,3,0],[8,0,4],[9,0,7]]
grid_9 = [[0,8,0],[0,0,7],[0,6,0]]

sudoku_grid = [
         grid_1,
         grid_2,
         grid_3,
         grid_4,
         grid_5,
         grid_6,
         grid_7,
         grid_8,
         grid_9]

""" 

Steps to create solving the sudoku grid:

1. Solve for the centre grid
2. then start rotating around clockwise for each sub-grid
   and solving them
3. if end of grid reached, restart with process

Steps to solving a sub-grid:
1. Check if grid is solved, move to next one defined in set * Could try randomized
2. Start from top right check if filled:
   2.1 move to the next right-most single square
   else:
   2.1 check what other numbers occupy the sub-grid
   2.2 choose one that is not occupied using a randomized method
   2.3 check the corresponding row/column
   if value is fine:
       move to next square in sub-grid
   else:
       repeat steps 2.1-2.3
 
"""

def solve_sub_grid(grid: List[List[List[int]]], index: int) -> Tuple[List[List[int]], bool]:
    """
       1. Check 3 Values, update the set.
                          A. the available numbers in the grid. func
                          B. the available numbers in the column. func 
                          C. the available numbers in the row. func
       2. Use randomizer function to select random value from available list
       3. Update the list in the board
    """
    print("*solving sub-grid...")
    solved_state = True
    solved_sub_grid = []
    sub_grid = grid[index]

    for row_index, number_list in enumerate(sub_grid):
        
        solved_sub_row = number_list
        occupied_digits = set()
        
        i = 0 
        for i in range(0, len(number_list)):
            if number_list[i] == 0:
                #Clear the set from previous iteration
                occupied_digits.clear()
                
                # Check occupied Digits
                occupied_digits.update(determine_occupied_digits_sub_grid(sub_grid))
                occupied_digits.update(determine_occupied_digits_in_column(grid, index, i))
                occupied_digits.update(determine_occupied_digits_in_row(grid, index, row_index))
                
                # Determine usable digits
                usable_digits = determine_usable_digits(occupied_digits)
                print(f"*Here are the usable digits: {usable_digits}")

                # If no digits found
                if len(usable_digits) > 0:
                    random_digit = find_random_square_value(usable_digits)
                    solved_sub_row[i] = random_digit
                    print("*Solved Square Value...")
                    print(solved_sub_row)
                else:
                    print("*Could not find value...")
                    solved_state = False
                    break
        if solved_state is False:
            break
        else:
            solved_sub_grid.append(solved_sub_row)
                    
    return solved_sub_grid, solved_state            


def determine_usable_digits(occupied_digits: Set[int]) -> List[int]:
    print("*Producing usable digits list...")
    usable_digits = []

    for i in range(1,10):
        if i not in occupied_digits:
            usable_digits.append(i)

    return usable_digits
                
def determine_occupied_digits_sub_grid(sub_grid: List[List[int]]) -> List[int]:
    print("*Determining occupied digits in sub-grid...")
    occupied_digits = []
    print(f"Showing sub-grid: {sub_grid}")

    for number_row in sub_grid:
        for number in number_row:
            if number > 0:
                occupied_digits.append(number)
    print(f"Determined Subgrid in 'determine_occupied_digits_sub_grid ':{occupied_digits}")
    return occupied_digits
                

def determine_occupied_digits_in_column(grid: List[List[List[int]]], index_subgrid: int, index_y: int) -> List[int]:
    print("*Determining occupied digits in column...")
    """ 
    Based on the index subgrid we can determine which other sub-grids are affected 
    in terms of coinciding with the column at hand

    grid 1 -> 4, 7
    grid 2 -> 5, 8
    grid 3 -> 6, 9

    """
    occupied_digits = []

    if index_subgrid in (0,3,6):
        for sub_grid_number in (0,3,6):
            for sub_grid_row in grid[sub_grid_number]:
                if sub_grid_row[index_y] > 0:
                    occupied_digits.append(sub_grid_row[index_y]) 

    elif index_subgrid in (1,4,7):
        for sub_grid_number in (1,4,7):
            for sub_grid_row in grid[sub_grid_number]:
                if sub_grid_row[index_y] > 0:
                    occupied_digits.append(sub_grid_row[index_y])

    elif index_subgrid in (2,5,8):
        for sub_grid_number in (2,5,8):
            for sub_grid_row in grid[sub_grid_number]:
                if sub_grid_row[index_y] > 0:
                    occupied_digits.append(sub_grid_row[index_y])

    print(f"Determined Subgrid in 'determine_occupied_digits_in_column ':{occupied_digits}")
    return occupied_digits

def determine_occupied_digits_in_row(grid: List[List[List[int]]], index_subgrid: int, index_x: int) -> List[int]:
    print("*Determining occupied digits in row...")

    """ 
    Based on the index subgrid we can determine which other sub-grids are affected 
    in terms of coinciding with the row at hand

    grid 1 -> 2, 3
    grid 4 -> 5, 6
    grid 7 -> 8, 9

    """
    occupied_digits = []
    for index, sub_grid in enumerate(grid):
        print(f'Subgrid #{index} - {sub_grid} \n')

    if index_subgrid in (0,1,2):
        for sub_grid_number in (0,1,2):
            for square_value in grid[sub_grid_number][index_x]:
                if square_value > 0:
                    occupied_digits.append(square_value)

    elif index_subgrid in (3,4,5):
        for sub_grid_number in (3,4,5):
            for square_value in grid[sub_grid_number][index_x]:
                if square_value > 0:
                    occupied_digits.append(square_value)

    elif index_subgrid in (6,7,8):
        for sub_grid_number in (6,7,8):
            for square_value in grid[sub_grid_number][index_x]:
                if square_value > 0:
                    occupied_digits.append(square_value)
    print(f"Determined Subgrid in 'determine_occupied_digits_in_row ':{occupied_digits}")
    return occupied_digits

def find_random_square_value(potential_numbers: List[int]) -> int:
    print("*Finding Random Square Value...")
    """
    call random selection function from lib
    """
    seed = randm.randint(0, 500)
    random = randm.Random(seed)
    choice = random.choice(potential_numbers)
    print(f"*Random number selected: {seed}")
    return choice

def check_grid_correctness(grid: List[List[List[int]]]) -> bool:
    """
    Check the grid for zero values and zero-length rows(working grid reset)
    """
    solved = True
    # Check for empty lists
    for sub_grid in grid:
        if len(sub_grid) == 0:
            solved = False
    # Check for unsolved squares
    if solved != False:
        for sub_grid in grid:
            for number_list in sub_grid:
                for number in number_list:
                    if number == 0:
                        solved = False
                        break
    return solved

""" 
Improvements:

1. Some sort of in-program memory system that keeps track of 
earlier attempts
"""

"""* Main program to test grid-solving ability *"""

if __name__ == "__main__":

    # Declare program-wide variables
    sub_grid_index_order = [0,1,2,3,4,5,6,7,8]
    solved = False
    solved_sub_grid = []
    workable_grid = [[],[],[],[],[],[],[],[],[]]

    # Epoch iterator
    i = 0
    
    while solved is False:        

        # Number of Epochs to run the solving algorithm
        i += 1
        # Reset current working grid After 50 attempts
        if i % 15 == 0:
            print("*Resetting current workable grid...")
            workable_grid = [[],[],[],[],[],[],[],[],[]]
            print("*Current Workable Board: ")
            for index, sub_grid in enumerate(workable_grid):
                print(f'Subgrid #{index} - {sub_grid} \n')

        # Print the attempt number
        print(f'Attempt Number: {i}')
 
        # Construct the current grid
        current_grid = deepcopy(sudoku_grid)
        for index, sub_grid in enumerate(workable_grid):
            if len(sub_grid) > 0:
                print("Replacing resolved sub_grid")
                current_grid[index] = sub_grid 

        # Solve for each sub-grid
        for index in sub_grid_index_order:
            solved_sub_grid, solved = solve_sub_grid(current_grid, index)
            if solved is False:
                print('*** Board could not be solved! Retrying!')
                break
            else:
                workable_grid[index] = solved_sub_grid
        
        # Verify correctness of current workable grid
        if check_grid_correctness(workable_grid):
            solved = True
            break

    # Failure condition - for set iterations
    if solved is False:
        print('*** Board Could Not Be Solved! See The Current Grid Values Below!')
        for index, sub_grid in enumerate(workable_grid):
            print(f'Subgrid #{index} - {sub_grid} \n')

    # Success condition
    elif solved is True:
        print('*** Board Solved!, See Solved Grid Values Below!')
        for index, sub_grid in enumerate(workable_grid):
            print(f'Subgrid #{index} - {sub_grid} \n')


