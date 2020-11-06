import copy
import numpy as np
import constant_variable as cv
import individual as ind
import laminate_multiple_component as lmc
import lamina_mass_and_cost as lmac
import constant_variable as cv


def get_fitness(ind):
    fitness = ind.length
    return fitness

"""
the length here is half of the laminate
"""
def get_angle_height_material_list(length, angle_type_list, length_list):
    angle_list = []; height_list = []; material_list = [];
    # generate the angle list
    for i in range(len(angle_type_list)):
        angle_list = angle_list + [angle_type_list[i]] * length_list[i]

    for k in range(length):
        random_material_pos = int(np.random.randint(low=0,high=len(cv.MATERIAL),size=1))
        material_list.append(cv.MATERIAL[random_material_pos])
        height_list.append(cv.LAYER_HEIGHT)
    return(angle_list, height_list, material_list)

def get_individual_and_set_individual_property(angle_list, height_list, material_list):
        temp_ind = ind.Individual(angle_list,height_list,material_list)
        temp_ind.strength_raito =  lmc.get_strength_ratio(angle_list, height_list, material_list, cv.LOAD)
        temp_ind.mass = lmac.get_laminate_mass(height_list,material_list)
        temp_ind.cost = lmac.get_laminate_cost(material_list)
        temp_ind.fitness = get_fitness(temp_ind)
        return temp_ind

"""
the lenght here is the full length of the laminate
"""
def get_laminate_individual(length, angle_type_list, length_list):
    # set material, angle, and height
    if(np.mod(length,2) == 0):
        angle_height_material = get_angle_height_material_list(int(length/2),\
                                angle_type_list, length_list)
        angle_list =  get_symmetry_list(angle_height_material[0])
        height_list = get_symmetry_list(angle_height_material[1])
        material_list = get_symmetry_list(angle_height_material[2])
        temp_ind = get_individual_and_set_individual_property(angle_list, height_list, material_list)
    if(np.mod(length, 2) == 1):
        mid = int((length - 1) /2)
        angle_height_material = get_angle_height_material_list(mid, \
                                       angle_type_list, length_list)
        angle_list = get_symmetry_list(angle_height_material[0])
        height_list = get_symmetry_list(angle_height_material[1])
        material_list = get_symmetry_list(angle_height_material[2])
        # insert middle layer
        random_material_pos = int(np.random.randint(low=0,high=len(cv.MATERIAL),size=1))
        random_angle_pos = int(np.random.randint(low=0,   high=len(angle_type_list),size=1))
        angle_list.insert(mid, angle_type_list[random_angle_pos])
        height_list.insert(mid, cv.LAYER_HEIGHT)
        material_list.insert(mid, cv.MATERIAL[random_material_pos])
        temp_ind = get_individual_and_set_individual_property(angle_list, height_list, material_list)
    return temp_ind



"""
argument: [1,3,2]
return  : [1,3,2,2,3,1]
"""
def get_symmetry_list(half_list):
    upper_half = copy.deepcopy(half_list)
    half_list.reverse()
    return upper_half + half_list

def get_safety_factor_pos_flag(population):
    safety_factor_pos_flag = -1
    max_strength_ratio = -1
    max_strength_ratio_pos = -1000
    for i in range(len(population)):
        if(population[i].strength_raito > max_strength_ratio):
            max_strength_ratio = population[i].strength_raito
            max_strength_ratio_pos = i

        if(population[i].strength_raito > cv.SAFETY_FACTOR):
            safety_factor_pos_flag = i
            break

    if(safety_factor_pos_flag == -1):
        print("no strength_raito is great then specified safety factor")
        safety_factor_pos_flag = max_strength_ratio_pos
    return safety_factor_pos_flag

def get_positive(a_list):
    pos = 0
    neg = 0
    for i in range(len(a_list)):
        if a_list[i] > 0:
            pos = pos + 1
        if a_list[i] < 0:
            neg = neg + 1
    print("neg: " + str(neg))
    print("pos: " + str(pos))



if __name__ == '__main__':

    #ma=[-45{gr_9} 45{gr_9}     -45 {ca_2}    45 {ca_2}
                 

    get_positive(angle)



