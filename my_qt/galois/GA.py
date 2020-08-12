import numpy as np
# genetic algorithm
def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = np.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        # return data type is tuple
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents

def crossover(parents, offspring_size):
    offspring = np.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually, it is at the center.
    crossover_point = np.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring
def mutation(offspring_crossover):
    for idx in range(offspring_crossover.shape[0]):
        # The random value to be added to the gene.
        weight_max = 2
        weight_min = -2
        mutation_constant = 0.8
        for i in range(offspring_crossover.shape[1]):
            pos = np.random.randint(0,100,1)%2
            if np.random.randint(0,4,1)%2 == 0:
                offspring_crossover[idx,pos]=offspring_crossover[idx,pos]+mutation_constant*(weight_max-offspring_crossover[idx,pos])*np.random.random()
            else:
                offspring_crossover[idx,pos]=offspring_crossover[idx,pos]-mutation_constant*(offspring_crossover[idx,pos]-weight_min)*np.random.random()
    return offspring_crossover
def get_individual_fitness(individual):
    fitness = (1 - np.sin(individual[0]))*(2 - np.cos(2*individual[1])) + (2 + np.sin(individual[0]))*(1 + np.cos(2*individual[1]))
    return fitness
def get_population_fitness(population):
    fitness = []
    for i in range(population.shape[0]):
        temp = get_individual_fitness(population[i])
        fitness.append(temp)
    return fitness
