import individual as ind
import numpy as np
import laminate_multiple_component as lmc
import copy


LAMINATELAYER=12
POPULATION=50
MUTATION_PROBABILITY=0.8
CROSSOVER_PROBABLITY=0.8
ELITIST_PERCENT=0.10
BEST_OUTPUS=[]
ANGLE = [0, np.pi/2, np.pi/3, np.pi/4, np.pi/6, -np.pi/2, -np.pi/3, -np.pi/4, -np.pi/6]
MATERIAL = ['glass_epoxy', 'graphite_epoxy', 'boron_epoxy']


# Defining the population size.
pop_size = (POPULATION,LAMINATELAYER) # The population will have POPULATION chromosome where each chromosome has LAMINATELAYER genes.
#Creating the initial population.
#parent_population = numpy.random.randint(low=0, high=3, size=pop_size)

def get_initial_population():
    initial_population = []
    for i in range(POPULATION):
        length = int(np.random.randint(low=3,high=30,size=1))
        angle_list = []
        height_list = []
        material_list = []
        for k in range(length):
            random_angle_pos = int(np.random.randint(low=0,high=len(ANGLE),size=1))
            angle_list.append(ANGLE[random_angle_pos])
            height_list.append(0.000165)
            material_list.append(MATERIAL[1])
        temp_ind = ind.Individual(angle_list,height_list,material_list)
        temp_ind.fitness = get_fitness(temp_ind)
        initial_population.append(temp_ind)
        print(temp_ind.fitness)

    return initial_population

def get_symmetry_list(half_list):
    upper_half = copy.deepcopy(half_list)
    half_list.reverse()
    return upper_half + half_list


def get_fitness(ind):
    load = [1,0,0,0,0,0]
    angle = get_symmetry_list(ind.angle_list)
    height = get_symmetry_list(ind.height_list)
    material = get_symmetry_list(ind.material_list)
    result = lmc.get_strength_ratio_and_weight(angle, height, material, load)
    return result


pop = get_initial_population()


"""
new_population[0, :] = [2.4,  0.7, 8, -2,   5,   1.1]
new_population[1, :] = [-0.4, 2.7, 5, -1,   7,   0.1]


num_generations = 100
for generation in range(num_generations):
    # Measuring the fitness of each chromosome in the population.
    fitness = composite.get_population_fitness(parent_population)
    BEST_OUTPUS.append(max(fitness))
    parents = GA.select_mating_pool(parent_population, fitness,
                                      int(ELITIST_PERCENT*POPULATION))

    offspring_crossover = GA.crossover(parents,
                                       offspring_size=(pop_size[0]-parents.shape[0], LAMINATELAYER))
    offspring_mutation = GA.mutation(offspring_crossover)
    parent_population[0:parents.shape[0], :] = parents
    parent_population[parents.shape[0]:, :] = offspring_mutation

    best_outputs.append(numpy.max(numpy.sum(new_population*equation_inputs, axis=1)))
    # The best result in the current iteration.
    print("Best result : ", numpy.max(numpy.sum(new_population*equation_inputs, axis=1)))

# Getting the best solution after iterating finishing all generations.
#At first, the fitness is calculated for each solution in the final generation.
fitness = GA.cal_pop_fitness(equation_inputs, new_population)
# Then return the index of that solution corresponding to the best fitness.
best_match_idx = numpy.where(fitness == numpy.max(fitness))

print("Best solution : ", new_population[best_match_idx, :])
print("Best solution fitness : ", fitness[best_match_idx])

import matplotlib.pyplot
matplotlib.pyplot.plot(BEST_OUTPUS)
matplotlib.pyplot.xlabel("Iteration")
matplotlib.pyplot.ylabel("Fitness")
matplotlib.pyplot.show()
"""
