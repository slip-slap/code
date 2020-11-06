import individual as ind
import tool
import copy
import numpy as np
import laminate_multiple_component as lmc
import lamina_mass_and_cost as lmac
import constant_variable as cv
import genetic_algorithm as my_ga


# GA
#POPULATION_NUMBER = 10 
#MUTATION_PROBABILITY=0.8
#CROSSOVER_PROBABLITY=0.8
#ELITIST_PERCENT=0.40


def get_fitness(ind):
    #fitness = ind.mass
    #fitness = ind.cost
    fitness = np.divide(ind.mass, 0.636) + np.divide(ind.cost, 23)
    #fitness = np.divide(ind.mass, 1.377) + np.divide(ind.cost, 80)
    #fitness = np.divide(ind.mass, 0.318) + np.divide(ind.cost, 12)
    #fitness = np.divide(ind.mass, 1.271) + np.divide(ind.cost, 105)
    return fitness

def get_angle_height_material_list(length):
    angle_list = []; height_list = []; material_list = [];
    for k in range(length):
        random_angle_pos = int(np.random.randint(low=0,high=len(cv.ANGLE),size=1))
        random_material_pos = int(np.random.randint(low=0,high=len(cv.MATERIAL),size=1))
        angle_list.append(cv.ANGLE[random_angle_pos])
        material_list.append(cv.MATERIAL[random_material_pos])
        height_list.append(cv.LAYER_HEIGHT)
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

        random_angle_pos = int(np.random.randint(low=0,high=len(cv.ANGLE),size=1))
        random_material_pos = int(np.random.randint(low=0,high=len(cv.MATERIAL),size=1))
        angle_list.insert(mid, cv.ANGLE[random_angle_pos])
        height_list.insert(mid, cv.LAYER_HEIGHT)
        material_list.insert(mid, cv.MATERIAL[random_material_pos])

        temp_ind = ind.Individual(angle_list,height_list,material_list)
        temp_ind.strength_raito =  lmc.get_strength_ratio(angle_list, height_list, material_list, cv.LOAD)
        temp_ind.mass = lmac.get_laminate_mass(height_list,material_list)
        temp_ind.cost = lmac.get_laminate_cost(material_list)
        temp_ind.fitness = get_fitness(temp_ind)
    return temp_ind

def get_initial_population():
    np.random.seed(0)
    initial_population = []
    while(len(initial_population)<cv.POPULATION_NUMBER):
        length = int(np.random.randint(low=cv.CHROMOSOME_LENGTH_LOWER_BOUND, \
            high=cv.CHROMOSOME_LENGTH_UPPER_BOUND, size=1))
        temp_ind = get_laminate_individual(length)
        initial_population.append(temp_ind)
    return initial_population

def get_concerter_angle(angle):
    if(angle < 0 and np.abs(angle + np.pi/2) < 0.1):
        return -90
    if(angle < 0 and np.abs(angle + np.pi/4) < 0.1):
        return -45
    if(np.abs(angle - 0) < 0.001):
        return 0
    if(angle > 0 and np.abs(angle - np.pi/2) < 0.1):
        return 90
    if(angle > 0 and np.abs(angle - np.pi/4) < 0.1):
        return 45

def save_to_output(result_fitness, result_strength_ratio, my_best_individual):
    with open("seed_test.py","a") as result_handler:
        result_handler.write("##################################")
        result_handler.write("\n")
        result_handler.write(cv.prefix + "load=  " + str(cv.LOAD))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "material=  " + str(cv.MATERIAL))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "angle=  " + str(cv.ANGLE))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "fitness_ =  " + str(result_fitness))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "strength_ratio_= "+ str(result_strength_ratio))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "cost= "+ str(my_best_individual.cost))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "mass= "+ str(my_best_individual.mass))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "strength_raito= "+ str(my_best_individual.strength_raito))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "number_of_layer= "+ str(len(my_best_individual.material_list)))
        result_handler.write("\n")

        stacking_sequence = []
        angle_list_copy = copy.deepcopy(my_best_individual.angle_list)
        for i in range(len(angle_list_copy)):
            angle_list_copy[i] = get_concerter_angle(angle_list_copy[i])
        for i in range(len(angle_list_copy)):
            stacking_sequence.append(angle_list_copy[i])
            stacking_sequence.append(my_best_individual.material_list[i])
        result_handler.write("#stacking sequence= "+ str(stacking_sequence))
        result_handler.write("\n")
        result_handler.write("##################################")
        result_handler.write("\n")


if __name__ == "__main__":
    result_fitness  = []
    result_times = []
    result_strength_ratio = []
    print("###load: "+str(cv.LOAD))
    population = get_initial_population()
    population.sort(key = lambda c: c.fitness)

    best_individual_pos = tool.get_safety_factor_pos_flag(population)
    current_fitness = population[best_individual_pos].fitness
    previous_fitness = 150

    print("initial fitness: " + str(current_fitness) + " strength_raito " + \
                str(population[best_individual_pos].strength_raito))

    result_fitness.append(current_fitness)
    result_times.append(1)
    result_strength_ratio.append(population[best_individual_pos].strength_raito)
    
    ga = my_ga.Genetic_Algorithm()
    d = 0
    while( d<cv.GA_RUNTIMES ):#np.abs(previous_fitness - current_fitness) > 0.0001):
        d = d+1 
        parents = ga.select_parents(population,int(cv.POPULATION_NUMBER * cv.ELITIST_PERCENT))
        offspring = ga.crossover(parents, int(cv.POPULATION_NUMBER*(1 - cv.ELITIST_PERCENT)))
        ga.mutation(offspring)
        for i in range(len(offspring)):
            material_list = offspring[i].material_list
            height_list = offspring[i].height_list
            angle_list = offspring[i].angle_list
            offspring[i].mass = \
                lmac.get_laminate_mass(height_list,material_list)
            offspring[i].cost = lmac.get_laminate_cost(material_list)
            offspring[i].fitness = get_fitness(offspring[i])
            offspring[i].strength_raito =  lmc.get_strength_ratio(angle_list, height_list, material_list, cv.LOAD)

        population[0:int(cv.POPULATION_NUMBER * cv.ELITIST_PERCENT)] = parents
        population[int(cv.POPULATION_NUMBER * cv.ELITIST_PERCENT):] = offspring
        population.sort(key = lambda c: c.fitness)

        best_individual = tool.get_safety_factor_pos_flag(population)
        previous_fitness = current_fitness
        current_fitness = population[best_individual].fitness

        result_fitness.append(current_fitness)
        result_strength_ratio.append(population[best_individual].strength_raito)

        print("curent fitness: " + str(current_fitness) + " strength_raito " + \
                str(population[best_individual].strength_raito))

    save_to_output(result_fitness, result_strength_ratio, population[best_individual])

