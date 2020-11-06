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
        print("wrong happen")

    angle_list  = []
    length_list = []

    while(len(angle_list) == 0):
        for i in range(len(p1_angle_type) - 1):
            temp_angle = int(np.multiply((p1_angle_type[i] + p2_angle_type[i])/2, 180/np.pi)) + int(np.random.randint(-4,4,1)) 
            angle_list.append(temp_angle)
            temp_length = int(np.random.randint(1,half_child_length + 1,size=1))
            length_list.append(temp_length)
        if(sum(length_list) >= half_child_length):
            angle_list = []
            length_list = []

    last_angle = int(np.multiply((p1_angle_type[-1] + p2_angle_type[-1])/2  \
                     , 180/np.pi)) + int(np.random.randint(-4,4,1))
    last_length = half_child_length - sum(length_list)

    angle_list.append(last_angle)
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
            while(child_length < 1):
                p1_pos = int(np.random.randint(0, len(parents), 1))
                p2_pos = int(np.random.randint(0, len(parents), 1))
                p1_angle = list(set(parents[p1_pos].angle_list))
                p1_angle.sort()
                p2_angle = list(set(parents[p2_pos].angle_list))
                p2_angle.sort()
                child_length = int(np.divide(parents[p1_pos].length + parents[p2_pos].length,2))+\
                                         int(np.random.randint(-4,4,1))  
                if(int(child_length/2) > 1):
                    child_angle_and_length = get_child(p1_angle, p2_angle, int(child_length/2))
                    child = tool.get_laminate_individual(child_length, child_angle_and_length[0], \
                         child_angle_and_length[1])
                    offspring.append(child)
        return offspring
            
    def mutation(self, offspring, mutation_percent=0.5):
        pass
        return

def get_chromosome_mutation(chromosome, values_set):
    value_after_muation = values_set[int(np.random.randint(0,len(values_set),1))]
    mutation_pos = int(np.random.randint(0,len(chromosome),1))
    chromosome[mutation_pos] = value_after_muation 
    chromosome[len(chromosome) - 1 - mutation_pos] = value_after_muation


if __name__ == "__main__":
    a = [-7,4]
    b = [-29,5]
    print("###############")
    print(a)
    print(b)
    for i in range(10):
        get_child(a, b, 2)



