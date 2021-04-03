import sys
import random
Locmin_stcount=0

def ReadFromFile(flname):
	try:
		f = open(flname,'r')
		text = f.read()
		sudoku_board = text.split('\n')
		f.close()
		L = []
		for i in sudoku_board:
			i = list(i)
			L2 = []
			if not (len(i) == 0 or i[0] == '*'):
				for j in range(11):
					if (i[j] != '|'):
						if (i[j] != '-'):
							L2.append(int(i[j]))
						else:
							L2.append(0)
				L.append(list(L2))
		return L
	except:
		print("Error in file reading")
		sys.exit()	

def popln_initialize(sudoku_board, popNumber):
	return [indexAssign(sudoku_board) for _ in range(popNumber)]

def indexAssign(sudoku_board):
	L = []
	for i in range(9):
		integerset = [1,2,3,4,5,6,7,8,9]
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
	sortedPopulation = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])
	return [ individual for individual, fitness in sortedPopulation[int(populn_num * 0.2):]]

def crossover(population, populn_num):
	a=[]
	for i in range(populn_num):
		a.append(crossoverInd(random.choice(population), random.choice(population)))
	return a

def crossoverInd(individual1, individual2):
	a=[]
	for ch_pair in zip(individual1, individual2):
		a.append(list(random.choice(ch_pair)))
	return a

def mutatePop(population, sudoku_board):
	return [ mutateInd(individual, sudoku_board) for individual in population ]

def mutateInd(individual, sudoku_board):
	for i in range(9):
		if (random.random() < 0.1):
			flag = False
			while(flag == False):
				rand1 = random.randint(0,8)
				rand2 = random.randint(0,8)
				if (sudoku_board[i][rand1] == 0 and sudoku_board[i][rand2] == 0):
					individual[i][rand1], individual[i][rand2] = individual[i][rand2], individual[i][rand1]
					flag = True
	return list(individual)


def fitnesscalc(population, generation=0):
	
	f=0
	x=[]
	fit=[]
	for sudoku_board in population:
		fitness = 0
		for i in range(9):   #column wise fitness
			L = []
			for j in range(9):
				L.append(sudoku_board[j][i])
			for item in range(9):
				if (L[item] in L[item+1:]) == False:
					fitness += 1
		
		L = []              #Box wise fitness
		for i in range(3):
			for j in range(3):
				L.append(sudoku_board[i][j])
		for item in range(9):
				if (L[item] in L[item+1:]) == False:
					fitness += 1
		L = []
		for i in range(3,6):
			for j in range(3):
				L.append(sudoku_board[i][j])
		for item in range(9):
				if (L[item] in L[item+1:]) == False:
					fitness += 1
		L = []
		for i in range(6,9):
			for j in range(3):
				L.append(sudoku_board[i][j])
		for item in range(9):
				if (L[item] in L[item+1:]) == False:
					fitness += 1
		L = []
		for i in range(3):
			for j in range(3,6):
				L.append(sudoku_board[i][j])
		for item in range(9):
				if (L[item] in L[item+1:]) == False:
					fitness += 1
		L = []
		for i in range(3,6):
			for j in range(3,6):
				L.append(sudoku_board[i][j])
		for item in range(9):
				if (L[item] in L[item+1:]) == False:
					fitness += 1
		L = []
		for i in range(6,9):
			for j in range(3,6):
				L.append(sudoku_board[i][j])
		for item in range(9):
				if (L[item] in L[item+1:]) == False:
					fitness += 1
		L = []
		for i in range(3):
			for j in range(6,9):
				L.append(sudoku_board[i][j])
		for item in range(9):
				if (L[item] in L[item+1:]) == False:
					fitness += 1
		L = []
		for i in range(3,6):
			for j in range(6,9):
				L.append(sudoku_board[i][j])
		for item in range(9):
				if (L[item] in L[item+1:]) == False:
					fitness += 1
		L = []
		for i in range(6,9):
			for j in range(6,9):
				L.append(sudoku_board[i][j])
		for item in range(9):
				if (L[item] in L[item+1:]) == False:
					fitness += 1

		if Locmin_stcount==99:
			if fitness>f:
				f=fitness
				x=sudoku_board
		
		if (fitness == 162): # for final solution
			print("")
			print("Max current fitness:",fitness)
			print("")
			print("Soln Is: ")
			board_print(sudoku_board)
			print("Gen:", generation )
			sys.exit()
		fit.append(fitness)
	if Locmin_stcount==99:
		print("Current Fitness:",f)
		print("")
		board_print(x)
	return fit


def board_print(sudoku_board):
	iteration = 0
	for i in sudoku_board:
		print(i[0], i[1], i[2], "", i[3], i[4], i[5], "|", i[6], i[7], i[8])
		iteration += 1
		if (iteration == 3 or iteration == 6):
			print("------------------- -")
	print("")
	

if __name__ == "__main__":
		sudoku_board = ReadFromFile(sys.argv[1])
		print("Input Sudoku Board:")
		board_print(sudoku_board)
		populn_num=200
		iteration = 0
		population = popln_initialize(sudoku_board, populn_num)
		fitnessPop = fitnesscalc(population)
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
					break
			else:
				Locmin_stcount = 0
			print("Gen:", iteration, "& Max fit %.1f" % sorted(fitnessPop)[-1])