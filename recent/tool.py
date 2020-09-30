import copy
import constant_variable as cv

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



