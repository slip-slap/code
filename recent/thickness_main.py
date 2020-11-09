import tool
import numpy as np
import constant_variable as cv
import genetic_algorithm_thickness as my_ga
import copy


def get_angle_list(angle_type_length, half_chromosome_length):
    angle_type_list = []
    length_type_list = []
    while(len(angle_type_list) == 0):
        for i in range(angle_type_length - 1):
            temp_angle = int(np.random.randint(-90,90,size=1))
            while(temp_angle in angle_type_list):
                temp_angle = int(np.random.randint(-90,90,size=1))
            angle_type_list.append(temp_angle)
            temp_length =int(np.random.randint(1,int(half_chromosome_length/angle_type_length) + 1 ,size=1)) 
            length_type_list.append(temp_length)
        if(sum(length_type_list) >= half_chromosome_length):
            angle_type_list= []
            length_type_list= []

    last_angle = int(np.random.randint(-90,90,size=1))
    while(last_angle in  angle_type_list):
        last_angle = int(np.random.randint(-90,90,size=1))
    angle_type_list.append(last_angle)
    last_length = half_chromosome_length - sum(length_type_list)
    length_type_list.append(last_length)

    return [angle_type_list, length_type_list]

def get_initial_population():
    #np.random.seed(0)
    initial_population = []
    while(len(initial_population)<cv.POPULATION_NUMBER):
        length = int(np.random.randint(low=cv.CHROMOSOME_LENGTH_LOWER_BOUND , \
            high=cv.CHROMOSOME_LENGTH_UPPER_BOUND, size=1)) 

        result = get_angle_list(cv.ANGLE_TYPE, int(length/2))
        temp_ind = tool.get_laminate_individual(length, result[0], result[1])
        print(set(temp_ind.angle_list))
        initial_population.append(temp_ind)
    return initial_population

def save_current_state_to_log(ind, result_times, result_fitness, result_strength_ratio, \
                              result_angle1, result_angle2):
    result_times.append(len(result_times) + 1)
    result_fitness.append(ind.fitness)
    result_strength_ratio.append(ind.strength_raito)
    angle_list = list(set(ind.angle_list))
    angle_list.sort()
    result_angle1.append(int(angle_list[0] * 180 /np.pi))
    result_angle2.append(int(angle_list[1] * 180 /np.pi))

def save_ga(result_times, result_fitness, result_strength_ratio, result_angle1, result_angle2):

    with open("thickness_result.py","a") as result_handler:
        result_handler.write("result_times=" + str(result_times))
        result_handler.write("\n")
        result_handler.write("result_fitness=" + str(result_fitness))
        result_handler.write("\n")
        result_handler.write("result_strength_ratio=" + str(result_strength_ratio))
        result_handler.write("\n")
        result_handler.write("result_angle1=" + str(result_angle1))
        result_handler.write("\n")
        result_handler.write("result_angle2=" + str(result_angle2))
        result_handler.write("\n")

if __name__ == "__main__":
    result_times = []
    result_fitness  = []
    result_strength_ratio = []
    result_angle1 = []
    result_angle2 = []
    print("###load: "+str(cv.LOAD))
    population = get_initial_population()
    population.sort(key = lambda c: c.fitness)

    best_individual_pos = tool.get_safety_factor_pos_flag(population)
    current_fitness = population[best_individual_pos].fitness
    save_current_state_to_log(population[best_individual_pos], result_times, \
                              result_fitness, result_strength_ratio, result_angle1, result_angle2)

    print("initial fitness: " + str(current_fitness) + " strength_raito " + \
                str(population[best_individual_pos].strength_raito))
    ga = my_ga.Genetic_Algorithm()
    current_run_time = 0
    while(current_run_time < cv.GA_RUNTIMES ):
        current_run_time = current_run_time + 1 
        parents = ga.select_parents(population,int(cv.POPULATION_NUMBER * cv.ELITIST_PERCENT))
        offspring = ga.crossover(parents, int(cv.POPULATION_NUMBER*(1 - cv.ELITIST_PERCENT)))
        ga.mutation(offspring)

        population[0:int(cv.POPULATION_NUMBER * cv.ELITIST_PERCENT)] = parents
        population[int(cv.POPULATION_NUMBER * cv.ELITIST_PERCENT):] = offspring
        population.sort(key = lambda c: c.fitness)

        best_individual = tool.get_safety_factor_pos_flag(population)
        current_fitness = population[best_individual].fitness
        save_current_state_to_log(population[best_individual], result_times, \
                              result_fitness, result_strength_ratio, result_angle1, result_angle2)


        print("curent fitness: " + str(current_fitness) + " strength_raito " + \
                str(population[best_individual].strength_raito))
        my_temp_angle = copy.deepcopy(population[best_individual].angle_list)
        for i in range(len(my_temp_angle)):
            my_temp_angle[i] = int(my_temp_angle[i]*180/np.pi)
        print(my_temp_angle)

    #save_to_output(result_fitness, result_strength_ratio, population[best_individual])
    save_ga(result_times, result_fitness, result_strength_ratio, result_angle1, result_angle2)

