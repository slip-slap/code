import numpy as np
import copy
import individual
import tool
import laminate_multiple_component as lmc
import constant_variable as cv


#PARENTS_BY_FITNESS_PERCENT = 0.4
#PARENTS_BY_FITNESS_PERCENT = 0.0
#PROPER_PARENTS_PERCENT = 0.3

def get_combine_offspring_list(a_list, b_list,random_number):

    a_quarter_pos = int(len(a_list)/4 + 1) 
    a_half_pos    = int(len(a_list)/2 + 1)
    b_quarter_pos = int(len(b_list)/4 + 1)
    b_half_pos    = int(len(b_list)/2+ 1)
    if(random_number == 0):
        result = a_list[0:a_quarter_pos] + b_list[0:b_quarter_pos]
    if(random_number == 1):
        result = a_list[0:a_quarter_pos] + b_list[b_quarter_pos:b_half_pos]
    if(random_number == 2):
        result = a_list[a_quarter_pos:a_half_pos] + b_list[0:b_quarter_pos]
    if(random_number == 3):
        result = a_list[a_quarter_pos:a_half_pos] + b_list[b_quarter_pos:b_half_pos]

    if(np.mod(random_number, 2)== 0):
        return tool.get_symmetry_list(result)
    if(np.mod(random_number, 2)== 1):
        mid_element = result[-1]
        rest = tool.get_symmetry_list(result[0:len(result)-1])
        rest.insert(len(result)-1,mid_element)
        return rest


    return tool.get_symmetry_list(result)

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
            p1_pos = int(np.random.randint(0, len(parents), 1))
            p2_pos = int(np.random.randint(0, len(parents), 1))
            p1_angle_list    = parents[p1_pos].angle_list
            p2_angle_list    = parents[p2_pos].angle_list
            p1_height_list   = parents[p1_pos].height_list
            p2_height_list   = parents[p2_pos].height_list
            p1_material_list = parents[p1_pos].material_list
            p2_material_list = parents[p2_pos].material_list

            child = copy.deepcopy(parents[0])
            random_number = int(np.random.randint(0,4,1))
            child.angle_list  = get_combine_offspring_list(p1_angle_list, \
                    p2_angle_list,random_number)
            child.height_list = \
            get_combine_offspring_list(p1_height_list,p2_height_list,random_number)
            child.material_list = get_combine_offspring_list(p1_material_list, \
                    p2_material_list,random_number)
            child.fitness = -1
            offspring.append(child)
        return offspring
            

    def mutation(self, offspring, mutation_percent=0.5):
        for i in range(len(offspring)):
            if(np.random.rand() > 1 - mutation_percent):
                get_chromosome_mutation(offspring[i].angle_list,cv.ANGLE)
                get_chromosome_mutation(offspring[i].material_list,cv.MATERIAL)
        return

def get_chromosome_mutation(chromosome, values_set):
    value_after_muation = values_set[int(np.random.randint(0,len(values_set),1))]
    mutation_pos = int(np.random.randint(0,len(chromosome),1))
    chromosome[mutation_pos] = value_after_muation 
    chromosome[len(chromosome) - 1 - mutation_pos] = value_after_muation


if __name__ == "__main__":
    get_chromosome_mutation([0,0,0,0,0],[12, 3])
    a = [4,2.7,1,6,8]
    a.sort(key = lambda c: np.abs(c-3))
    print(a)

