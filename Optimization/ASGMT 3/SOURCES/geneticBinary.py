import random
import numpy as np
from numpy import linalg as LA

random.seed(a=0)

def real(b):
    zb = 0
    for i in range(len(b)):
        zb += b[i]*2**i
    xb = -1 + zb*(5/((2**len(b))-1))
    return xb

def in_U(b):
    xb = real(b)
    if xb >= -2.5 and xb <= 2.5:
        return True
    else:
        return False

def vij(atom_i, atom_j):
    atom_i = np.array(atom_i)
    atom_j = np.array(atom_j)
    rij = LA.norm(atom_i-atom_j)+10**(-8)
    return ((1/rij)**12) - ((1/rij)**6)

def real_population_f(population, N):
    real_population = []
    for i in range(0, len(population)):
        p = []
        for j in range(0, N*13*3, 13):
            p.append(real(population[i][j:j+13]))
        real_population.append(p)
    for i in range(0, len(population)):
        atom = []
        for j in range(0, N*3, 3):
            atom.append(real_population[i][j:j+3])
        real_population[i] = atom[:]
    return real_population

def energy_f(individual):
    energy = 0
    for i in range(len(individual)-1):
        for j in range(i+1, len(individual)):
            energy += vij(individual[i], individual[j])
    energy = 4*energy
    return energy

def fitness_f(population, N):
    fitness = []
    real_population = real_population_f(population, N)
    for i in range(len(population)):
        energy = energy_f(real_population[i])
        fitness.append(energy)
    return fitness

def rouletteCompareWorst(population, fitness):
    fworst = fitness[np.argmax(fitness)]
    fitness_value = []
    fi = 0
    for i in range(len(fitness)):
        fitness_value.append(fworst-fitness[i])
        fi += fitness_value[i]
    ps = []
    for i in range(len(fitness)):
        ps.append(fitness_value[i]/fi)
    lim = []
    for i in range(len(ps)):
        a = 0
        for j in range(0, i+1):
            a += ps[j]
        lim.append(a)
    S = []
    Ns = len(population) # or Ns = len(population)*2
    for i in range(Ns):
        r = random.uniform(0, 1)
        for j in range(len(lim)):
            if r <= lim[j]:
                S.append(population[j])
                break
    return S

def rouletteLinearFitness(population, fitness):
    s = 1.5
    indexes = np.argsort(fitness)[::-1]
    rho = [0]*len(fitness)
    for i in range(len(fitness)):
        rho[i] = np.where(indexes == i)[0][0]
    fitness_value = [0]*len(population)
    fi = 0
    for i in range(len(population)):
        fitness_value[i] = 2 - s + 2*(s-1)*((rho[i]-1)/len(population)-1)
        fi += fitness_value[i]
    ps = [0]*len(fitness)
    for i in range(len(fitness)):
        ps[i] = fitness_value[i]/fi
    lim = [0]*len(ps)
    for i in range(len(ps)):
        a = 0
        for j in range(0, i+1):
            a += ps[j]
        lim[i] = a
    S = []
    Ns = len(population) # or Ns = len(population)*2
    for i in range(Ns):
        r = random.uniform(0, 1)
        for j in range(len(lim)):
            if r <= lim[j]:
                S.append(population[j])
                break
    return S

def tournament(population, fitness, N):
    Ntour = int(len(population)/2)
    S = [0]*len(population)
    Ns = len(population) # or Ns = len(population)*2
    ls = [0]*len(population)
    for i in range(len(population)):
        ls[i] = i
    for i in range(Ns):
        Ntour_population = [0]*Ntour
        Ntour_fitness = [0]*Ntour
        chosen = random.sample(ls, Ntour)
        for j in range(Ntour):
            Ntour_population[j] = population[chosen[j]]
            Ntour_fitness[j] = fitness[chosen[j]]
        S[i] = Ntour_population[np.argmin(Ntour_fitness)]
    return S

def selection(population, fitness, selectionMethod, N):
    if selectionMethod == "rouletteCompareWorst":
        S = rouletteCompareWorst(population, fitness)
    elif selectionMethod == "rouletteLinearFitness":
        S = rouletteLinearFitness(population, fitness)
    elif selectionMethod == "tournament":
        S = tournament(population, fitness, N)
    return S

def crossover(S, crossoverMethod, pairMethod, kPoints=10):
    crossoverProbability = 0.5
    C = [0]*len(S)
    parentIndexes = [0]*len(S)
    j = 0
    for i in range(len(S)):
        C[i] = S[i][:]
        r = random.uniform(0, 1)
        if r <= crossoverProbability:
            parentIndexes[j] = i
            j += 1
    if len(parentIndexes)%2 != 0:
        while True:
            r = random.randint(0, len(S)-1)
            if r not in parentIndexes:
                parentIndexes[len(parentIndexes)] = r
                break
    points = [0]*(len(S[i])-1)
    for i in range(len(points)):
        points[i] = i
    if pairMethod == "random":
        random.shuffle(parentIndexes)
        
    #if pairMethod is random then the population is shuffled and we continue by taking pairs by order, else we just take pairs by order
    parents = []
    for i in range(len(parentIndexes)):
        parents.append(S[parentIndexes[i]])
    for i in range(0, len(parents), 2):
        if crossoverMethod == "kPointCrossover":
            crossover_points = random.sample(points, kPoints)
            crossover_points.sort()
        elif crossoverMethod == "uniformCrossover":
            crossover_points = []
            for j in range(len(points)):
                rand = random.randint(0, 1)
                if rand == 1:
                    crossover_points.append(j)
        child1 = parents[i][:]
        child2 = parents[i+1][:]
        for j in range(len(crossover_points)):
            child1[crossover_points[j]:], child2[crossover_points[j]:] = child2[crossover_points[j]:], child1[crossover_points[j]:]
        C[parentIndexes[i]] = child1[:]
        C[parentIndexes[i+1]] = child2[:]
    return C

def mutation(population):
    M = population[:]
    mutationProbability = 0.1
    for i in range(len(population)):
        for j in range(len(population[i])):
            r = random.uniform(0, 1)
            if r < mutationProbability:
                M[i][j] = 1 - population[i][j]
    return M 

def newPopulation(population, fitness, population_mutation, fitness_mutation, newPopulationMethod):
    if newPopulationMethod == "replace":
        return population_mutation, fitness_mutation
    elif newPopulationMethod == "merge":
        size = len(population)
        population.extend(population_mutation)
        fitness = np.append(fitness, fitness_mutation)
        indexes = np.argsort(fitness)
        fitness = fitness[indexes]
        populationCopy = population[:]
        for i in range(len(indexes)):
            population[i] = populationCopy[indexes[i]][:]
        return population[:size], fitness[:size]
    
def updateBest(population, fitness, x_best_pop, x_best_fit):
    newBestPosition = np.argmin(fitness)
    if fitness[newBestPosition] < x_best_fit:
        x_best_pop = population[newBestPosition]
        x_best_fit = fitness[newBestPosition]
    return x_best_pop, x_best_fit

def restartNewPopulation(pop_size, N):
    population = []
    for i in range(pop_size):
        p = []
        for j in range(N):
            atom = []
            for k in range(3):
                while True:
                    b = []
                    for l in range(13):
                        a = random.randint(0, 1)
                        b.append(a)
                    if in_U(b):
                        break
                atom.extend(b)
            p.extend(atom)
        population.append(p)
    return population

def geneticBinary(population, solutionQuality, N, experimentID):

    selectionMethod = "rouletteCompareWorst"
    # selectionMethod = "rouletteLinearFitness"
    # selectionMethod = "tournament"
    
    # crossoverMethod = "kPointCrossover"
    crossoverMethod = "uniformCrossover"

    # kPoints = 10
    # kPoints = 5
    # kPoints = 2
    
    pairMethod = "random"
    # pairMethod = "order"
    
    # newPopulationMethod = "replace"
    newPopulationMethod = "merge"

    Tmax = N*(10**5)
    restart = int(0.10 * Tmax) # restart after 10% of total iterations without improvement
    restart_iterations = 0
    numberOfRestarts = 0
    
    k = 0
    
    # Evaluate the fitness of the initial population
    fitness = fitness_f(population, N)
    fitness = np.array(fitness)
    x_best_pos = np.argmin(fitness)
    x_best_pop = population[x_best_pos]
    x_best_fit = fitness[x_best_pos]
    k_best = "initial"
    
    # Main loop
    while k < Tmax/10: 
        
        # Selction process
        S = selection(population, fitness, selectionMethod, N)
        
        # Crossover process
        C = crossover(S, crossoverMethod, pairMethod)
        
        # Mutation process
        M = mutation(C)
        
        # Evaluate the fitness of the mutated population
        fitness_mutation = fitness_f(M, N)
        fitness_mutation = np.array(fitness_mutation)
        
        # New population
        population, fitness = newPopulation(population, fitness, M, fitness_mutation, newPopulationMethod)
        
        # Update best point
        new_x_best_pop, new_x_best_fit = updateBest(population, fitness, x_best_pop, x_best_fit)
        if new_x_best_fit < x_best_fit:
            x_best_fit = new_x_best_fit
            x_best_pop = new_x_best_pop
            k_best = k
            restart_iterations = 0
        else:
            restart_iterations += 1
            if restart_iterations == restart:
                population = restartNewPopulation(len(population), N)
                restart_iterations = 0
                numberOfRestarts += 1
        
        # Update iterations parameter
        k +=1

    path = "results/binary/" + str(N) + "/" + selectionMethod + "_" + str(N) + "_" + crossoverMethod + "_" + pairMethod + "_" + newPopulationMethod + ".txt"
    with open(path, "a") as file:
        file.write("Experiment\t" + str(experimentID) + "\t" + str(x_best_fit) + "\t" + str(abs(x_best_fit - solutionQuality)) + "\t" + str(k_best) + "\t" + str(numberOfRestarts) + "\t" + str(x_best_pop) + "\n")
