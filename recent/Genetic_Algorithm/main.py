import individual as ind
import numpy as np
import laminate_multiple_component as lmc
import copy
import genetic_algorithm as my_ga


POPULATION_NUMBER = 100
MUTATION_PROBABILITY=0.8
CROSSOVER_PROBABLITY=0.8
ELITIST_PERCENT=0.10
BEST_OUTPUS=[]
#ANGLE = [0, np.pi/2, np.pi/3, np.pi/4, np.pi/6, -np.pi/2, -np.pi/3, -np.pi/4, -np.pi/6]
ANGLE = [np.pi/4] 
#MATERIAL = ['glass_epoxy', 'graphite_epoxy', 'boron_epoxy']
MATERIAL = ['glass_epoxy', 'graphite_epoxy']
COST = {'glass_epoxy':1, 'graphite_epoxy':2.5}

def get_initial_population():
    initial_population = []
    for i in range(POPULATION_NUMBER):
        length = int(np.random.randint(low=8, high=40,size=1))
        angle_list = []
        height_list = []
        material_list = []
        # set material, angle, and height
        for k in range(length):
            random_angle_pos = int(np.random.randint(low=0,high=len(ANGLE),size=1))
            random_material_pos = int(np.random.randint(low=0,high=len(MATERIAL),size=1))
            angle_list.append(ANGLE[random_angle_pos])
            angle_list.append(-np.pi/4)
            height_list.append(0.000165)
            height_list.append(0.000165)
            material_list.append(MATERIAL[random_material_pos])
            material_list.append(MATERIAL[random_material_pos])

        temp_ind = ind.Individual(angle_list,height_list,material_list)
        strength_and_ratio  = get_fitness(temp_ind)
        temp_ind.strength_raito = strength_and_ratio['SR']
        temp_ind.mass = strength_and_ratio['mass']
        temp_ind.cost = 0
        for i in range(length):
            if(temp_ind.material_list[i] == 'glass_epoxy'):
                temp_ind.cost = temp_ind.cost + 1*2 
            if(temp_ind.material_list[i] == 'graphite_epoxy'):
                temp_ind.cost = temp_ind.cost + 2.5*2

        initial_population.append(temp_ind)

    return initial_population

def get_symmetry_list(half_list):
    upper_half = copy.deepcopy(half_list)
    half_list.reverse()
    return upper_half + half_list


def get_fitness(ind):
    load = [0,0,1,0,0,0]
    angle = get_symmetry_list(ind.angle_list)
    height = get_symmetry_list(ind.height_list)
    material = get_symmetry_list(ind.material_list)
    result = lmc.get_strength_ratio_and_weight(angle, height, material, load)
    return result


population = get_initial_population()
survive_individual = []
for i in range(len(population)):
    if(population[i].strength_raito > 2):
        survive_individual.append(population[i])
        #print(population[i])
        #print(population[i].material_list)


survive_individual.sort(key = lambda c:c.mass)
for i in range(len(survive_individual)):
    print("ha")
    print(survive_individual[i])
    print(survive_individual[i].material_list)
    print(2*len(survive_individual[i].material_list)*0.165)
#population.sort(key = lambda c: c.fitness['SR'] + c.fitness['mass'], reverse=True)

#for i in range(len(population)):
#    print(population[i])

"""
while(current_fitness-previous_fitness>0.001):
    parents = my_ga.select_parents(population,4)
    offspring = my_ga.crossover(parents, 6)
    my_ga.mutation(offspring)
    for i in range(len(offspring)):
        offspring[i].fitness = offspring[i].calculate_individual_fitness()
    population[0:4] = parents
    population[6:] = offspring
    population.sort(key = lambda c: c.fitness,reverse=True)

    previous_fitness = current_fitness
    current_fitness = population[0].fitness
"""




# Getting the best solution after iterating finishing all generations.
#At first, the fitness is calculated for each solution in the final generation.
#fitness = GA.cal_pop_fitness(equation_inputs, new_population)
# Then return the index of that solution corresponding to the best fitness.
#best_match_idx = numpy.where(fitness == numpy.max(fitness))

"""
print("Best solution : ", new_population[best_match_idx, :])
print("Best solution fitness : ", fitness[best_match_idx])

import matplotlib.pyplot
matplotlib.pyplot.plot(BEST_OUTPUS)
matplotlib.pyplot.xlabel("Iteration")
matplotlib.pyplot.ylabel("Fitness")
matplotlib.pyplot.show()
"""
