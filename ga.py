import sys
import random
import time
import sudoku as s
import numpy as np
import winsound
Locmin_stcount = 0


def rFF(x):
    func = {"s1": s.s1(), "s2": s.s2(), "s3": s.s3(), "s4": s.s4(), "s5": s.s5(),
    "s6": s.s6(), "s7": s.s7(), "s8": s.s8(), "s9": s.s9(), "s10": s.s10(), "s11": s.s11(),
    "s12": s.s12(), "s13": s.s13(), "s14": s.s14(), "s15": s.s15(), "s16": s.s16(), "s17": s.s17(),
    "s18": s.s18(), "s19": s.s19(), "s20": s.s20(), "s21": s.s21(), "s22": s.s22(), "s23": s.s23(),
    "s24": s.s24(), "s25": s.s25(), "s26": s.s26(), "s27": s.s27(), "s28": s.s28(), "s29": s.s29(),
    "s30": s.s30()}
    return func[x]


def popln_initialize(sudoku_board, popNumber):
    return [indexAssign(sudoku_board) for _ in range(popNumber)]


def indexAssign(sudoku_board):
    L = []
    for i in range(9):
        integerset = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        L.append(list(sudoku_board[i]))
        for j in range(9):
            if (L[i][j] == 0):
                hasFoundInt = False
                while(hasFoundInt == False):
                    pickedInt = random.choice(integerset)
                    if(pickedInt not in L[i]):
                        L[i][j] = pickedInt
                        integerset.remove(pickedInt)
                        hasFoundInt = True
                    else:
                        integerset.remove(pickedInt)
    return L


def poplnselecn(population, fitness_population, populn_num):
    sortedPopulation = sorted(
        zip(population, fitness_population), key=lambda ind_fit: ind_fit[1])
    return [individual for individual, fitness in sortedPopulation[int(populn_num * 0.2):]]


def crossover(population, populn_num):
    a = []
    for i in range(populn_num):
        a.append(crossoverInd(random.choice(population), random.choice(population)))
    return a


def crossoverInd(individual1, individual2):
    a = []
    for ch_pair in zip(individual1, individual2):
        a.append(list(random.choice(ch_pair)))
    return a


def mutatePop(population, sudoku_board):
    return [mutateInd(individual, sudoku_board) for individual in population]


def mutateInd(individual, sudoku_board):
    for i in range(9):
        if (random.random() < 0.1):
            flag = False
            while(flag == False):
                rand1 = random.randint(0, 8)
                rand2 = random.randint(0, 8)
                if (sudoku_board[i][rand1] == 0 and sudoku_board[i][rand2] == 0):
                    individual[i][rand1], individual[i][rand2] = individual[i][rand2], individual[i][rand1]
                    flag = True
    return list(individual)


def fitnesscalc(population, generation=0):

    f = 0
    x = []
    fit = []
    for sudoku_board in population:
        fitness = 0
        for i in range(9):  # column wise fitness
            L = []
            for j in range(9):
                L.append(sudoku_board[j][i])
            for item in range(9):
                if (L[item] in L[item+1:]) == False:
                    fitness += 1

        L = []  # Box wise fitness
        for i in range(3):
            for j in range(3):
                L.append(sudoku_board[i][j])
        for item in range(9):
                if (L[item] in L[item+1:]) == False:
                    fitness += 1
        L = []
        for i in range(3, 6):
            for j in range(3):
                L.append(sudoku_board[i][j])
        for item in range(9):
                if (L[item] in L[item+1:]) == False:
                    fitness += 1
        L = []
        for i in range(6, 9):
            for j in range(3):
                L.append(sudoku_board[i][j])
        for item in range(9):
                if (L[item] in L[item+1:]) == False:
                    fitness += 1
        L = []
        for i in range(3):
            for j in range(3, 6):
                L.append(sudoku_board[i][j])
        for item in range(9):
                if (L[item] in L[item+1:]) == False:
                    fitness += 1
        L = []
        for i in range(3, 6):
            for j in range(3, 6):
                L.append(sudoku_board[i][j])
        for item in range(9):
                if (L[item] in L[item+1:]) == False:
                    fitness += 1
        L = []
        for i in range(6, 9):
            for j in range(3, 6):
                L.append(sudoku_board[i][j])
        for item in range(9):
                if (L[item] in L[item+1:]) == False:
                    fitness += 1
        L = []
        for i in range(3):
            for j in range(6, 9):
                L.append(sudoku_board[i][j])
        for item in range(9):
                if (L[item] in L[item+1:]) == False:
                    fitness += 1
        L = []
        for i in range(3, 6):
            for j in range(6, 9):
                L.append(sudoku_board[i][j])
        for item in range(9):
                if (L[item] in L[item+1:]) == False:
                    fitness += 1
        L = []
        for i in range(6, 9):
            for j in range(6, 9):
                L.append(sudoku_board[i][j])
        for item in range(9):
                if (L[item] in L[item+1:]) == False:
                    fitness += 1

        if Locmin_stcount == 99:
            if fitness > f:
                f = fitness
                x = sudoku_board
        if (fitness == 162):  # for final solution
            print("")
            print("Max current fitness:", fitness)
            print("")
            print("Solution Is: ")
            board_print(sudoku_board)
            print("Gen:", generation)
            print("Generation Resets:", resets)
            D.stop()
            #play a sound when solution is found
            duration = 1000  # milliseconds
            freq = 440  # Hz
            winsound.Beep(freq, duration)
            sys.exit()

        fit.append(fitness)
    if Locmin_stcount==99:
        print("Current Fitness:",f)
        print("")
        board_print(x)		
    return fit


def board_print(sudoku_board):
    iteration = 0
    print("\n")
    for i in sudoku_board:

        print(" ", i[0]," ", i[1]," ", i[2], " | ", i[3]," ", i[4]," ", i[5], " | ", i[6]," ", i[7]," ", i[8])
        iteration += 1
        if (iteration == 3 or iteration == 6):
            print("><><><><><><><><><><><><><><><><><><><><><")
    print("\n")
class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class Timer:
    def __init__(self,startTime):
        self.starTime = startTime
   
    def start(self):
        self.startTime = time.perf_counter()

    def stop(self):
        if self.startTime is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self.startTime
        self.startTime = None
        print(f"Elapsed time = {elapsed_time :0.4f} seconds")
if __name__ == "__main__":
    K = input("Which board would you like? (format('s10')?")
sudoku_board = rFF(K)
print("Input Sudoku Board:")
board_print(sudoku_board)
D=Timer(None)
D.start()
zoo=True
resets = 0
while zoo==True:
    populn_num=200
    iteration = 0
    population = popln_initialize(sudoku_board, populn_num)
    fitnessPop = fitnesscalc(population)
    resets += 1
    while (iteration < 1000):
        iteration += 1
        poplnparents = poplnselecn(population, fitnessPop, populn_num)
        poplnchild = crossover(poplnparents, populn_num)
        population = mutatePop(poplnchild, sudoku_board)
        lastFitness = sorted(fitnessPop)[-1]
        fitnessPop = fitnesscalc(population, iteration)
        if (lastFitness == sorted(fitnessPop)[-1]):
            Locmin_stcount += 1
            if Locmin_stcount == 100:
                print("Local Minima detected")
                zoo==False
                break
        else:
            Locmin_stcount = 0
        print("Gen:", iteration, "& Max fit %.1f" % sorted(fitnessPop)[-1])
