import copy, random, time
from simanneal import Annealer
from sudoku import sudoLst
import numpy as np
import pandas as pd

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
        #quit searching if score hits -162, solution was found
        if score == -162:
            self.user_exit = True
        return score

def main():
    #list of step iterations to test
    stepsToRun = [10000, 25000, 50000, 75000, 100000, 200000, 300000, 400000,
                    500000, 750000, 1000000]
    
    #total_time = 0
    for stepCount in stepsToRun:
        #list to view sum of fully solved sudoku puzzles
        completedPuzzles = []

        #list to view times
        completedTimes = []
        for i in range(100):
            for count, sudopuzzle in enumerate(sudoLst,1):
                start = time.perf_counter()
                #create array of our current sudoku puzzle from "sudoku.py"
                currentPuzzle = np.array([item for sublist in sudopuzzle for item in sublist])

                #initialized Sudoku_sq class as sudoku
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
                sudoku.steps = stepCount
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
                print("E=%f (-162 means a solution was found)" % e, '\n')
                #add completed puzzles to list, for comparision to view sum of total completed puzzles
                if e == -162:
                    #timer to view time to complete 1 puzzle
                    end = time.perf_counter()
                    final_time = end - start
                    #total_time += final_time
                    completedPuzzles.append(count)
                    completedTimes.append(final_time)

        #print('Total completed Puzzles out of 30:', len(completedPuzzles), end="\n")
        #print('Puzzles that were completed:', completedPuzzles, end='\n')
        #print('Times of Puzzles that were completed (Seconds):', completedTimes, end='\n')
        #print("Total Time (Seconds): %f" %total_time)

        #save completed puzzles and times to a CSV file
        df = pd.DataFrame(list(zip(completedPuzzles,completedTimes)), columns =['Puzzles', 'Avg_Times'])
        
        #create new dataframe with count of how many times each puzzle was solved
        duplicates = df.groupby(df.Puzzles.tolist(), as_index=False).size()

        #create new dataframe with average time to solve each puzzle
        df1 = df.groupby('Puzzles', as_index=False).mean()
        
        #combine count of solutions found per puzzle to dataframe for saving
        df1['Count of Solutions Found'] =duplicates['size']

        #save to csv with no index values, just columns of puzzles + times
        df1.to_csv('./Sim_Anneal_CSVs/SudokuPuzzles_100Trials_' + str(sudoku.steps) + '_Steps.csv', index=False)


if __name__ == "__main__":
    start1 = time.perf_counter()
    main()
    end1 = time.perf_counter()
    final_time1 = end1 - start1
    #print out total time to run all 100 trials 
    print(final_time1)