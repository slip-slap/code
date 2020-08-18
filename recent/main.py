import individual as ind
import tool
import copy
import numpy as np
import laminate_multiple_component as lmc
import genetic_algorithm as my_ga
import lamina_mass_and_cost as lmac
import constant_variable as cv


# GA
POPULATION_NUMBER = 100
MUTATION_PROBABILITY=0.8
CROSSOVER_PROBABLITY=0.8
ELITIST_PERCENT=0.10
BEST_OUTPUS=[]
# Material
ANGLE = [0]#np.pi/4, -np.pi/4, np.pi/2] #, np.pi/2, np.pi/3, np.pi/4, np.pi/6, -np.pi/2, -np.pi/3, -np.pi/4, -np.pi/6]
MATERIAL = [cv.CARBON_EPOXY,cv.GLASS_EPOXY,cv.GRAPHITE_EPOXY] 
LAYER_HEIGHT = 0.000165


def get_fitness(ind):
    #fitness = ind.mass
    #fitness = ind.cost
    fitness = np.divide(ind.mass,0.31778) + np.divide(ind.cost,12)
    return fitness

def get_angle_height_material_list(length):
    angle_list = []; height_list = []; material_list = [];
    for k in range(length):
        random_angle_pos = int(np.random.randint(low=0,high=len(ANGLE),size=1))
        random_material_pos = int(np.random.randint(low=0,high=len(MATERIAL),size=1))
        angle_list.append(ANGLE[random_angle_pos])
        height_list.append(LAYER_HEIGHT)
        material_list.append(MATERIAL[random_material_pos])
    return(angle_list, height_list, material_list)


def get_laminate_individual(length):
    # set material, angle, and height
    if(np.mod(length,2) == 0):
        angle_height_material = get_angle_height_material_list(int(length/2))
        angle_list = tool.get_symmetry_list(angle_height_material[0])
        height_list = tool.get_symmetry_list(angle_height_material[1])
        material_list = tool.get_symmetry_list(angle_height_material[2])

        temp_ind = ind.Individual(angle_list,height_list,material_list)
        temp_ind.strength_raito =  lmc.get_strength_ratio(angle_list, height_list, material_list, cv.LOAD)
        temp_ind.mass = lmac.get_laminate_mass(height_list,material_list)
        temp_ind.cost = lmac.get_laminate_cost(material_list)
        temp_ind.fitness = get_fitness(temp_ind)
    if(np.mod(length, 2) == 1):
        mid = int((length - 1) /2)
        angle_height_material = get_angle_height_material_list(mid)
        angle_list = tool.get_symmetry_list(angle_height_material[0])
        height_list = tool.get_symmetry_list(angle_height_material[1])
        material_list = tool.get_symmetry_list(angle_height_material[2])

        random_angle_pos = int(np.random.randint(low=0,high=len(ANGLE),size=1))
        random_material_pos = int(np.random.randint(low=0,high=len(MATERIAL),size=1))
        angle_list.insert(mid, ANGLE[random_angle_pos])
        height_list.insert(mid, LAYER_HEIGHT)
        material_list.insert(mid,MATERIAL[random_material_pos])

        temp_ind = ind.Individual(angle_list,height_list,material_list)
        temp_ind.strength_raito =  lmc.get_strength_ratio(angle_list, height_list, material_list, cv.LOAD)
        temp_ind.mass = lmac.get_laminate_mass(height_list,material_list)
        temp_ind.cost = lmac.get_laminate_cost(material_list)
        temp_ind.fitness = get_fitness(temp_ind)
    return temp_ind

def get_initial_population():
    initial_population = []
    while(len(initial_population)<100):

        length = int(np.random.randint(low=5, high=13,size=1))
        temp_ind = get_laminate_individual(length)

        if(temp_ind.strength_raito > cv.SAFETY_FACTOR):
            initial_population.append(temp_ind)
    return initial_population


if __name__ == "__main__":
    print("#######################")
    population = get_initial_population()
    population.sort(key = lambda c:c.fitness)
    for i in range(len(population)):
        pass
    current_fitness = population[0].fitness
    previous_fitness = -1

    print("fitness: " + str(current_fitness))
    ga = my_ga.Genetic_Algorithm()
    while(np.abs(current_fitness - previous_fitness) > 0.0001):
        parents = ga.select_parents(population,20)
        offspring = ga.crossover(parents, 80)
        ga.mutation(offspring)
        for i in range(len(offspring)):
            material_list = offspring[i].material_list
            height_list = offspring[i].height_list
            offspring[i].mass = \
                lmac.get_laminate_mass(tool.get_symmetry_list(height_list),tool.get_symmetry_list(material_list))
            offspring[i].cost = lmac.get_laminate_cost(tool.get_symmetry_list(material_list))
            offspring[i].fitness = get_fitness(offspring[i])
        population[0:20] = parents
        population[20:] = offspring
        population.sort(key = lambda c: c.fitness)

        previous_fitness = current_fitness
        current_fitness = population[0].fitness
        print("curent fitness: " + str(current_fitness))
        #print("current material "+ str(population[0].material_list))
        angle_list_copy = copy.deepcopy(population[0].angle_list)
        for i in range(len(angle_list_copy)):
            angle_list_copy[i] = str(angle_list_copy[i])[0:4]
        print("current angel: "+ str(angle_list_copy))
        print("strength ratio: "+ str(population[0].strength_raito))
        print("mass: "+ str(population[0].mass))
        print("cost: "+ str(population[0].cost))
        print("length: " + str(len(population[0].material_list)))
        print("material: " + str(population[0].material_list))



"""
print("Best solution : ", new_population[best_match_idx, :])
print("Best solution fitness : ", fitness[best_match_idx])

import matplotlib.pyplot
matplotlib.pyplot.plot(BEST_OUTPUS)
matplotlib.pyplot.xlabel("Iteration")
matplotlib.pyplot.ylabel("Fitness")
matplotlib.pyplot.show()
"""
