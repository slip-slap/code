import numpy as np
import copy
import individual
import tool
import laminate_multiple_component as lmc
import constant_variable as cv


#PARENTS_BY_FITNESS_PERCENT = 0.4
#PARENTS_BY_FITNESS_PERCENT = 0.0
#PROPER_PARENTS_PERCENT = 0.3

"""
assuming all the angles are different in one angle type
"""
def get_child(p1_angle_type, p2_angle_type, half_child_length):

    if(len(p1_angle_type) != len(p2_angle_type)):
        print("the number of angle type of parent1 and parents2 are different")


    angle_list  = []
    length_list = []

    while(len(angle_list) == 0):
        for i in range(len(p1_angle_type) - 1):
            temp_angle = int(np.multiply((p1_angle_type[i] + p2_angle_type[i])/2, 180/np.pi)) + int(np.random.randint(-4,4,1)) 
            while(temp_angle in angle_list):
                temp_angle = int(np.multiply((p1_angle_type[i] + p2_angle_type[i])/2, 180/np.pi)) + int(np.random.randint(-4,4,1)) 
            angle_list.append(temp_angle)
            temp_length = int(np.random.randint(1,half_child_length,size=1))
            length_list.append(temp_length)
        if(sum(length_list) >= half_child_length):
            angle_list = []
            length_list = []

    while(len(angle_list) < len(p1_angle_type)):
        last_angle = int(np.multiply((p1_angle_type[-1] + p2_angle_type[-1])/2  \
                     , 180/np.pi)) + int(np.random.randint(-4,4,1))
        if last_angle not in angle_list:
            angle_list.append(last_angle)
            last_length = half_child_length - sum(length_list)
            length_list.append(last_length)

    return [angle_list, length_list]


class Genetic_Algorithm(object):

    """Docstring for Genetic_Algorithm. """

    def __init__(self):
        """TODO: to be defined. """
        pass

    def select_parents(self, population,  num_parents):
        # select parents according to fitness
        parents_by_fitness = population[0:int(num_parents * cv.PARENTS_BY_FITNESS_PERCENT)]
        # select parents according to fitness
        proper_parents = [x for x in population if x.strength_raito >cv.SAFETY_FACTOR][\
                0:int(num_parents * cv.PROPER_PARENTS_PERCENT)]
        
        # select parents according to distance to 
        population_copy = copy.deepcopy(population)
        population_copy.sort(key = lambda c: np.abs(c.strength_raito - cv.SAFETY_FACTOR))
        remain_number = num_parents - len(parents_by_fitness) - len(proper_parents)
        parents_by_constraint = population_copy[0:remain_number]
        """
        print("parents begin")
        for i in range(len(parents_by_constraint)):
            print("fitness: " + str(parents_by_constraint[i].fitness) + " strength_raito " + \
                str(parents_by_constraint[i].strength_raito))
        print("parents end")
        """
        return parents_by_fitness + proper_parents + parents_by_constraint

    def crossover(self, parents, offspring_number):

        offspring = []
        while(len(offspring) < offspring_number):
        #for i in range(offspring_number):
            child_length = -1
            while(child_length < cv.ANGLE_TYPE * 2):
                p1_pos = int(np.random.randint(0, len(parents), 1))
                p2_pos = int(np.random.randint(0, len(parents), 1))
                p1_angle = list(set(parents[p1_pos].angle_list))
                p1_angle.sort()
                p2_angle = list(set(parents[p2_pos].angle_list))
                p2_angle.sort()
                child_length = int(np.divide(parents[p1_pos].length + parents[p2_pos].length,2))+\
                                         int(np.random.randint(-4,4,1))  
                if(int(child_length/2) > cv.ANGLE_TYPE):
                    child_angle_and_length = get_child(p1_angle, p2_angle, int(child_length/2))
                    child = tool.get_laminate_individual(child_length, child_angle_and_length[0], \
                         child_angle_and_length[1])
                    offspring.append(child)
        return offspring
            
    def mutation(self, offspring, mutation_percent=0.5):
        for i in range(len(offspring)):
            evu_dir= cv.SAFETY_FACTOR - offspring[i].strength_raito
            child_angle = list(set(offspring[i].angle_list))
            child_total_length = offspring[i].length + int(evu_dir*40)
            random_number_list = get_random_number_list(int(evu_dir*20), len(child_angle))
            length_list = []
            for k in range(len(child_angle)):
                length_list.append(int(offspring[i].angle_list.count(child_angle[k])/2) + \
                                                                              random_number_list[k])
                child_angle[k] = child_angle[k] + \
                                            np.random.randint(0,np.abs(10*evu_dir)+1)*np.pi/180

            if(child_total_length % 2 == 0 and child_total_length != sum(length_list)*2):
                remain = int(child_total_length/2) - sum(length_list)
                length_list[0] = length_list[0] + remain
            
            if(child_total_length < sum(length_list) * 2):
                length_list[0] = length_list[0] - 1 
            for i in range(len(child_angle)):
                child_angle[i] = child_angle[i] * 180/np.pi
            offspring[i] = tool.get_laminate_individual(child_total_length, child_angle, length_list)




def get_random_number_list(the_sum, individual_number):
    if(the_sum == 0):
        return [0] * individual_number

    random_number_list = []
    while(len(random_number_list) == 0):
        for i in range(individual_number - 1):
            if(the_sum < 0):
                temp = int(np.random.randint(the_sum, 1, 1))
            else:
                temp = int(np.random.randint(0, the_sum, 1))
            random_number_list.append(temp)
        if(np.abs(sum(random_number_list)) > np.abs(the_sum)):
            random_number_list = []

    last = the_sum - sum(random_number_list)
    random_number_list.append(last)
    return random_number_list



def get_chromosome_mutation(chromosome, values_set):
    value_after_muation = values_set[int(np.random.randint(0,len(values_set),1))]
    mutation_pos = int(np.random.randint(0,len(chromosome),1))
    chromosome[mutation_pos] = value_after_muation 
    chromosome[len(chromosome) - 1 - mutation_pos] = value_after_muation


if __name__ == "__main__":
    a = get_random_number_list(5, 4)
    print(a)



