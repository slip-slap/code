import numpy as np
import copy
import individual
import tool
import laminate_multiple_component as lmc
import constant_variable as cv

def get_combine_offspring_list(a_list, b_list):
    a_length = int(len(a_list)/2)
    b_length = int(len(b_list)/2)
    return a_list[0:a_length] + b_list[0:b_length]
    

class Genetic_Algorithm(object):

    """Docstring for Genetic_Algorithm. """

    def __init__(self):
        """TODO: to be defined. """
        pass

    def select_parents(self, population,  num_parents):
        parents = population[0:num_parents]
        return parents

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
            child.angle_list  = get_combine_offspring_list(p1_angle_list, p2_angle_list)
            child.height_list = get_combine_offspring_list(p1_height_list,p2_height_list)
            child.material_list = get_combine_offspring_list(p1_material_list,  p2_material_list)
            child.fitness = -1
            if(lmc.get_strength_ratio(child.angle_list, child.height_list, child.material_list, cv.LOAD) > 2):
                offspring.append(child)
        return offspring
            

    def mutation(self, offspring):
        for i in range(len(offspring)):
            pass
        return


