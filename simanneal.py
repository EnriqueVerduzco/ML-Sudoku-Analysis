import copy
import random
from simanneal import Annealer
from sudoku import *
import time

def print_sudoku(state):
    border = "------+-------+------"
    rows = [state[i:i+9] for i in range(0,81,9)]
    for i,row in enumerate(rows):
        if i % 3 == 0:
            print(border)
        three = [row[i:i+3] for i in range(0,9,3)]
        print(" | ".join(
            " ".join(str(x or "_") for x in one)
            for one in three
        ))
    print(border)

def coord(row, col):
    return row*9+col

def block_indices(block_num):
    """return linear array indices corresp to the sq block, row major, 0-indexed.
    block:
       0 1 2     (0,0) (0,3) (0,6)
       3 4 5 --> (3,0) (3,3) (3,6)
       6 7 8     (6,0) (6,3) (6,6)
    """
    firstrow = (block_num // 3) * 3
    firstcol = (block_num % 3) * 3
    indices = [coord(firstrow+i, firstcol+j) for i in range(3) for j in range(3)]
    return indices

def initial_solution(problem):
    """provide sudoku problem, generate an init solution by randomly filling
    each sq block without considering row/col consistency"""
    solution = problem.copy()
    for block in range(9):
        indices = block_indices(block)
        block = problem[indices]
        zeros = [i for i in indices if problem[i] == 0]
        to_fill = [i for i in range(1, 10) if i not in block]
        random.shuffle(to_fill)
        for index, value in zip(zeros, to_fill):
            solution[index] = value
    return solution

class Sudoku_Sq(Annealer):
    def __init__(self, problem):
        self.problem = problem
        state = initial_solution(problem)
        #same as Annealer.__init__(state)
        super().__init__(state)
    def move(self):
        """randomly swap two cells in a random square"""
        block = random.randrange(9)
        indices = [i for i in block_indices(block) if self.problem[i] == 0]
        m, n = random.sample(indices, 2)
        self.state[m], self.state[n] = self.state[n], self.state[m]
    def energy(self):
        """calculate the number of violations: assume all rows are OK"""
        column_score = lambda n: -len(set(self.state[coord(i, n)] for i in range(9)))
        row_score = lambda n: -len(set(self.state[coord(n, i)] for i in range(9)))
        score = sum(column_score(n)+row_score(n) for n in range(9))
        if score == -162:
            self.user_exit = True # early quit, we found a solution
        return score

def main():
    #list to view sum of fully solved sudoku puzzles
    completedPuzzles = []
    #timer to view total time for ALL puzzles
    start = time.perf_counter()
    for count, sudopuzzle in enumerate(sudoLst):
        #create array of our current sudoku puzzle from "sudoku.py"
        currentPuzzle = np.array([item for sublist in sudopuzzle for item in sublist])

        #starts Simmulated Annealing process using current Sudoku Puzzle
        sudoku = Sudoku_Sq(currentPuzzle)

        #Sim Anneal code here
        # 3 different copy_strategy methods: deepcopy, method, slice
        #https://github.com/perrygeo/simanneal/blob/master/simanneal/anneal.py
        sudoku.copy_strategy = "method"

        #print out sudoku puzzle with initial random values
        print('---------------------------\n')
        print('Initial Sudoku Puzzle\n')
        print_sudoku(sudoku.state)

        #Uses automatic selection of temperature to minimize energy
        # auto_schedule = sudoku.auto(minutes=1)
        # print(auto_schedule)
        # sudoku.set_schedule(auto_schedule)
        # print('Auto Schedule for Sim Annealing Done')

        #Set Sim Annealing schedule manually here
        #Annealer parameters can be seen in "anneal.py" from github link above
        #Tmax = Initial Temperature 
        #Tmin = Low Temperature
        sudoku.Tmax = .5
        sudoku.Tmin = .05
        sudoku.steps = 10000
        sudoku.updates = 100

        print('\n')
        print('Starting Anneal Process:')
        print('\n')
        #returns finished sudoku puzzle
        state, e = sudoku.anneal()
        print('\n')
        #prints out finished sudoku puzzle, if solution was found
        print_sudoku(state)

        #prints out Energy of puzzle, -162 == puzzle solution found
        print("E=%f (expect -162)" % e, '\n')
        #add completed puzzles to list, for comparision to view sum of total completed puzzles
        if e == -162:
            completedPuzzles.append(count)

    #timer to view total time for 30 puzzles
    end = time.perf_counter()
    final_time = end - start

    print('Total amount of completed Puzzles:', len(completedPuzzles), end="\n")
    print('Puzzles that were completed:', completedPuzzles, end='\n')
    print("Time in Seconds: %f" %final_time)
if __name__ == "__main__":
    main()