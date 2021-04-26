#Let p(i,j,n) denote the proposition that is true when the number n is in the cell in the ith row and the jth column. 

#There are 9×9 × 9 = 729 such propositions. 

#In the sample puzzle p(5,1,6) is true, but p(5,j,6) is false for j = 2,3,...9

#For each cell with a given value, assert p(i,j,n), when the cell in row i and column j has the given value. 

#Assert that every row contains every number. ^ i=1 to 9   ^ n=1 to 9   v j=1 to 9    p(i,j,n)

#Assert that every column contains every number. ^ j=1 to 9   ^ n=1 to 9   v i=1 to 9    p(i,j,n)

#Assert that each of the 3 x 3 blocks contain every number. ^ r=0 to 2   ^ s=0 to 2    ^ n=1 to 9    ^ i=1 to 3    v j=1 to 3 p(3r + i, 3s + j, n)

#Assert that no cell contains more than one number. Take the conjunction over all values of n, n’, i, and j,
#where each variable ranges from 1 to 9 and n!=n', of p(i,j,n) -> not(p(i,j,n')).

#To solve a  Sudoku puzzle, we need to find an assignment of truth values to the 729 variables of the form  p(i,j,n) 
#that makes the conjunction of the assertions true. Those variables that are assigned T yield a solution to the puzzle. 

#A truth table can always be used to determine the satisfiability of a compound proposition. 
#But this is too complex even for modern computers for large problems. 

#There has been much work on developing efficient methods for solving satisfiability problems 
#as many practical problems can be translated into satisfiability problems. 
# import pycosat
import sys, getopt, pycosat, time
from pprint import pprint
from sudoku import *
import pandas as pd

def solve_problem(problemset):
    print('Problem:') 
    pprint(problemset)  
    solve(problemset) 
    print('Answer:')
    pprint(problemset)  

def v(i, j, d):
    """
    Return the number of the variable of cell i, j and digit d,
    which is an integer in the range of 1 to 729 (including).
    """
    return 81 * (i - 1) + 9 * (j - 1) + d


def sudoku_clauses():
    """
    Create the (11745) Sudoku clauses, and return them as a list.
    Note that these clauses are *independent* of the particular
    Sudoku puzzle at hand.
    """
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, 10):
        for j in range(1, 10):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d) for d in range(1, 10)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, 10):
                for dp in range(d + 1, 10):
                    res.append([-v(i, j, d), -v(i, j, dp)])

    def valid(cells):
        # Append 324 clauses, corresponding to 9 cells, to the result.
        # The 9 cells are represented by a list tuples.  The new clauses
        # ensure that the cells contain distinct values.
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, 10):
                        res.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])

    # ensure rows and columns have distinct values
    for i in range(1, 10):
        valid([(i, j) for j in range(1, 10)])
        valid([(j, i) for j in range(1, 10)])
    # ensure 3x3 sub-grids "regions" have distinct values
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            valid([(i + k % 3, j + k // 3) for k in range(9)])

    assert len(res) == 81 * (1 + 36) + 27 * 324
    return res

def solve(grid):
    #solve a Sudoku problem
    clauses = sudoku_clauses()
    for i in range(1, 10):
        for j in range(1, 10):
            d = grid[i - 1][j - 1]
            # For each digit already known, a clause (with one literal). 
            if d:
                clauses.append([v(i, j, d)])

    # Print number SAT clause  
    numclause = len(clauses)
    print ("P CNF " + str(numclause) +"(number of clauses)")

    # solve the SAT problem
#     start = time.time()
    sol = set(pycosat.solve(clauses))
#     end = time.time()
#     print("Time: "+str(end - start))

    def read_cell(i, j):
        # return the digit of cell i, j according to the solution
        for d in range(1, 10):
            if v(i, j, d) in sol:
                return d

    for i in range(1, 10):
        for j in range(1, 10):
            grid[i - 1][j - 1] = read_cell(i, j)

 #list to view sum of fully solved sudoku puzzles
completedPuzzles = []

#list to view times
completedTimes = []

#for loop to run 100 trials
for i in range(100):
    #reset list of Sudoku Puzzles before they are solved again
    sudokuList = copy.deepcopy(copy_sudoku_lists)
    for count, sudopuzzle in enumerate(sudokuList, 1):
        currentPuzzle = np.array([item for sublist in sudopuzzle for item in sublist])
        start = time.perf_counter()
        solve_problem(sudopuzzle)
        end = time.perf_counter()
        final_time = end - start
        completedPuzzles.append(count)
        completedTimes.append(final_time)

#save completed puzzles and times to a CSV file
df = pd.DataFrame(list(zip(completedPuzzles,completedTimes)), columns =['Puzzles', 'Avg_Times'])

#create new dataframe with count of how many times each puzzle was solved
duplicates = df.groupby(df.Puzzles.tolist(), as_index=False).size()

#create new dataframe with average time to solve each puzzle
df1 = df.groupby('Puzzles', as_index=False).mean()

#combine count of solutions found per puzzle to dataframe for saving
df1['Count of Solutions Found'] =duplicates['size']

#save to csv with no index values, just columns of puzzles + times
df1.to_csv('./Satisfyability_100Trials.csv', index=False)