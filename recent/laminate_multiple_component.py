import numpy as np
import copy
import lamina_failure as lf
import lamina_mass_and_cost as lmac
import constant_variable  as cv
import tool
import csv




"""
argument: material name, for example: glass_epoxy
"""
def calc_lamina_stiffness_matrix_Q(material):
    if(material == cv.GLASS_EPOXY):
        global material_property 
        material_property = cv.GLASS_EPOXY_PROPERTIES
    if(material == cv.GRAPHITE_EPOXY):
        material_property = cv.GRAPHITE_EPOXY_PROPERTIES
    if(material == cv.CARBON_EPOXY):
        material_property = cv.CARBON_EPOXY_PROPERTIES
    if(material == cv.T300_5308):
        material_property = cv.T300_5308_PROPERTIES

    E1 = material_property['E1']
    E2 = material_property['E2']
    v12 = material_property['v12']
    v21 = E2 * v12 / E1
    G12 = material_property['G12']
    Q=np.zeros((3, 3))
    #Q11
    Q[0][0] = E1 / (1 - v21 * v12)
    #Q12 =  Q12
    Q[0][1] = E2 * v12 / (1 - v21 * v12)
    Q[1][0] = Q[0][1]
    Q[2][0] = Q[0][2] = 0
    #Q22
    Q[1][1] = E2 / (1 - v21 * v12)
    Q[2][1] = Q[1][2] = 0
    #Q66
    Q[2][2] = G12
    return Q

def calc_lamina_stiffness_matriceQ_with_angle_theta(theta,material):
    matriceQ = calc_lamina_stiffness_matrix_Q(material)
    c = np.cos(theta)
    s = np.sin(theta)

    angle_matricQ = np.zeros((3,3)) 
    angle_matricQ[0][0] = matriceQ[0][0]*c*c*c*c + matriceQ[1][1]*s*s*s*s + \
                          2*(matriceQ[0][1]+2*matriceQ[2][2])*s*s*c*c

    angle_matricQ[0][1] = (matriceQ[0][0] + matriceQ[1][1] -                \
            4*matriceQ[2][2])*s*s*c*c + matriceQ[0][1] * (c*c*c*c + s*s*s*s)
    angle_matricQ[1][0] = angle_matricQ[0][1]

    angle_matricQ[1][1] = matriceQ[0][0]*s*s*s*s + matriceQ[1][1]*c*c*c*c + \
                          2*(matriceQ[0][1]+2*matriceQ[2][2])*s*s*c*c

    angle_matricQ[0][2] = (matriceQ[0][0]-matriceQ[0][1] - 2*matriceQ[2][2])* \
            c*c*c*s -(matriceQ[1][1] - matriceQ[0][1] - 2*matriceQ[2][2])*    \
            s*s*s*c
    angle_matricQ[2][0] = angle_matricQ[0][2]       

    angle_matricQ[1][2] = (matriceQ[0][0]-matriceQ[0][1] - 2*matriceQ[2][2])* \
            c*s*s*s - (matriceQ[1][1] - matriceQ[0][1] - 2*matriceQ[2][2])*   \
            c*c*c*s
    angle_matricQ[2][1] = angle_matricQ[1][2]
    
    angle_matricQ[2][2] = (matriceQ[0][0] + matriceQ[1][1]-2*matriceQ[0][1]- \
            2*matriceQ[2][2])*s*s*c*c + matriceQ[2][2]*(s*s*s*s + c*c*c*c) 
    return angle_matricQ

"""
argument height is a list
for example: height = [0.005, 0.005, 0.005]
"""
def get_height_coordinate_list(height):
    coordinate_list = []
    totalHeight=0
    for i in range(len(height)):
        totalHeight=totalHeight+height[i]

    low = -totalHeight/2
    coordinate_list.append(low)
    for i in range(len(height)):
        coordinate_list.append(coordinate_list[-1]+height[i])
    return coordinate_list

"""
argument height is a list
for example: height = [0.005, 0.005, 0.005]
"""
def get_height_coordinate_top_middle_bottom_list(height):
    coordinate_list = []
    totalHeight=0
    for i in range(len(height)):
        totalHeight=totalHeight+height[i]

    low = -totalHeight/2
    coordinate_list.append(low)
    coordinate_list.append(coordinate_list[-1] + 0.5 * height[i])
    coordinate_list.append(coordinate_list[-1] + 0.5 * height[i])
    for i in range(len(height)-1):
        coordinate_list.append(coordinate_list[-1])
        coordinate_list.append(coordinate_list[-1] + 0.5 * height[i+1])
        coordinate_list.append(coordinate_list[-1] + 0.5 * height[i+1])

    return coordinate_list

"""
parameters
angle = [0, np.pi/6, -np.pi/4]
height = [0.005, 0.005, 0.005]
material = [GLASS_EPOXY, GRAPHITE_EPOXY, GLASS_EPOXY]
"""
def calc_laminate_stiffness_matrice(angle, height, material):

    A = B = D = np.zeros((3, 3))
    # initiaize
    coordinate_list = get_height_coordinate_list(height)
    for i in range(len(angle)):
        angle_Q = \
            calc_lamina_stiffness_matriceQ_with_angle_theta(angle[i],material[i])
        A = A + (coordinate_list[i+1] - coordinate_list[i])*angle_Q

        B = B + 0.5*(coordinate_list[i+1] * coordinate_list[i+1] - \
                   coordinate_list[i] * coordinate_list[i])*angle_Q

        D = D + (1/3)*(coordinate_list[i+1]*coordinate_list[i+1]* \
                coordinate_list[i+1] - \
                coordinate_list[i]*coordinate_list[i]*coordinate_list[i])*angle_Q

    upper=np.hstack((A, B))
    down=np.hstack((B, D))
    stiffness_matrix=np.vstack((upper, down))
    return stiffness_matrix
"""
argu1 laminate stiffness_matrices
argu2  load Nx, Ny, Nxy, Mx, My, Mxy, for example: load=[1000,1000,0,0,0,0]
output midplane strains and curvatures
"""
def calc_midplane_strain_and_curvature(laminate_stiffness_matrice,load):
    compliance_matrice = np.linalg.inv(laminate_stiffness_matrice)
    strain_and_curvature = np.dot(compliance_matrice, load)
    return strain_and_curvature

# global and local stress and stain on each lamina
def get_lamina_global_strain(midplane_strain_and_curvature, \
                            coordinate_top_middle_bottom_list, index):
    temp_strain_list = []
    for i in range(3):
        # top middle bottom
        strain = list(np.add(midplane_strain_and_curvature[0:3], \
                        coordinate_top_middle_bottom_list[3*index+i] * \
                        midplane_strain_and_curvature[3:6]))
        temp_strain_list.append(strain)

    return temp_strain_list

def get_lamina_global_stress(angle_Q,strain_list):
    temp_stress_list = []
    for i in range(len(strain_list)):
        stress = list(np.dot(angle_Q,strain_list[i]))
        temp_stress_list.append(stress)
    return temp_stress_list

def get_transform_matrice(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    transform_matrice = np.zeros((3, 3))
    transform_matrice[0][0] = c*c
    transform_matrice[0][1] = s*s
    transform_matrice[0][2] = 2*s*c
    transform_matrice[1][0] = s*s
    transform_matrice[1][1] = c*c
    transform_matrice[1][2] = -2*s*c
    transform_matrice[2][0] = -s*c
    transform_matrice[2][1] = s*c
    transform_matrice[2][2] = c*c - s*s
    return transform_matrice

def get_lamina_local_strain(theta, global_strain_list):
    temp_strain_list = []
    transform_matrice = get_transform_matrice(theta)
    for i in range(len(global_strain_list)):
        local_strain = \
            list(np.dot(transform_matrice, [global_strain_list[i][0],global_strain_list[i][1],0.5*global_strain_list[i][2]]))
        local_strain[2] = 2*local_strain[2]
        temp_strain_list.append(local_strain)
    return temp_strain_list

def get_lamina_local_stress(theta,global_stress_list):
    temp_stress_list = []
    transform_matrice = get_transform_matrice(theta)
    for i in range(len(global_stress_list)):
        local_stress = list(np.dot(transform_matrice,global_stress_list[i]))
        temp_stress_list.append(local_stress)
    return temp_stress_list


"""
return a dictionay result = {'global_strain':[],'global_stress':[], \
                              'local_strain':[], 'local_stress':[]}
"""
def calc_each_lamina_stress_and_strain(midplane_strain_and_curvature, \
                                       angle_list, height_list,material_list):

    coordinate_top_middle_bottom_list = get_height_coordinate_top_middle_bottom_list(height_list)
    global_strain = [];global_stress = [];local_strain = [];local_stress = [];
    # for every lamina
    for i in range(len(angle_list)):
        angle_Q = \
            calc_lamina_stiffness_matriceQ_with_angle_theta(angle_list[i],material_list[i])

        # get global strain for every lamina
        temp_strain_list = get_lamina_global_strain( \
                           midplane_strain_and_curvature,coordinate_top_middle_bottom_list, i) 
        global_strain.append(temp_strain_list)

        # get global stress
        temp_stress_list = get_lamina_global_stress(angle_Q,temp_strain_list)
        global_stress.append(temp_stress_list)

        # get local strain
        temp_local_strain_list = get_lamina_local_strain(angle_list[i],temp_strain_list)
        local_strain.append(temp_local_strain_list)
        
        # get local stress
        temp_local_stress_list = \
                get_lamina_local_stress(angle_list[i],temp_stress_list)
        local_stress.append(temp_local_stress_list)

    result = {'global_strain':global_strain,'global_stress':global_stress, \
              'local_strain':local_strain, 'local_stress':local_stress}
    return result

"""
argument  dictionay result = {'global_strain':[],'global_stress':[], \
                              'local_strain':[], 'local_stress':[]}
stress and strain of every lamina
"""
def get_failure_lamina_SR_and_pos(lamina_stress_strain,material_list):
    min_strenght_ratio = 10000000000000 
    failure_lamina_pos  = 0
    max_strength_ratio = -10000000

    local_stress = lamina_stress_strain['local_stress']
    for i in range(len(local_stress)):
        for j in range(len(local_stress[i])):
            if(cv.FAILURE_CRITERIA == "max_stress"):
                SR = lf.maximum_stress_failure_theory(local_stress[i][j], material_list[i])
            if(cv.FAILURE_CRITERIA == "tsai_wu"):
                SR = lf.tsai_wu_failure_theory(local_stress[i][j],material_list[i])
            #print(SR)
            if(min_strenght_ratio > SR):
                min_strenght_ratio = SR
                failure_lamina_pos = i
            if(max_strength_ratio < SR):
                max_strength_ratio = SR
                max_strength_ratio_pos = i

    LPF_and_FPF = {"min_strenght_ratio":min_strenght_ratio, "failure_lamina_pos":failure_lamina_pos, \
                   "max_strength_ratio":max_strength_ratio}
    return LPF_and_FPF

"""
get first ply failure load and last ply failure load
"""
def get_FPF_and_LPF():
    angle = [np.pi/4,np.pi/4,np.pi/4,np.pi/4]
    angle = [np.pi/4, -np.pi/4, -np.pi/4, np.pi/4]
    angle = [0, np.pi/2, 0]
    angle = [0, np.pi/2, np.pi/2, 0]
    height=[0.005] * 4 
    load=[1,0,0,0,0,0]
    material=[GRAPHITE_EPOXY] * 4 

    laminate_stiffness = calc_laminate_stiffness_matrice(angle,height,material)
    midplane_strain_and_curvature = \
                 calc_midplane_strain_and_curvature(laminate_stiffness,load)
    stress_and_strain_of_every_lamina = calc_each_lamina_stress_and_strain(midplane_strain_and_curvature,angle, \
                            height,material)
    LPF_and_FPF = get_failure_lamina_SR_and_pos(stress_and_strain_of_every_lamina,material)

    FPF = LPF_and_FPF['min_strenght_ratio']
    while(LPF_and_FPF["max_strength_ratio"] > LPF_and_FPF["min_strenght_ratio"]):
        pos_1 = LPF_and_FPF['failure_lamina_pos']
        pos_2 = len(angle) - 1 - pos_1
        temp = []
        for i in range(len(angle)):
            if(i != pos_1 and i != pos_2):
                temp.append(angle[i])
        angle = temp
        height = [0.005]*len(angle)
        material=[GRAPHITE_EPOXY] * len(angle)
        laminate_stiffness = calc_laminate_stiffness_matrice(angle,height,material)
        midplane_strain_and_curvature = \
                     calc_midplane_strain_and_curvature(laminate_stiffness,load)
        stress_and_strain_of_every_lamina = calc_each_lamina_stress_and_strain(midplane_strain_and_curvature,angle, \
                                height,material)
        LPF_and_FPF = get_failure_lamina_SR_and_pos(stress_and_strain_of_every_lamina,material)

    LPF = LPF_and_FPF['min_strenght_ratio']
    laminate_efficiency = np.divide(FPF, LPF)
    print("laminate efficiency" + str(laminate_efficiency))

def get_strength_ratio(angle, height, material, load):
    for i in range(len(angle)):
        angle[i] = np.divide(angle[i]*np.pi, 180)

    laminate_stiffness = calc_laminate_stiffness_matrice(angle,height,material)
    midplane_strain_and_curvature = \
                 calc_midplane_strain_and_curvature(laminate_stiffness,load)
    stress_and_strain_of_every_lamina = calc_each_lamina_stress_and_strain(midplane_strain_and_curvature,angle, \
                            height,material)
    sr_and_pos = get_failure_lamina_SR_and_pos(stress_and_strain_of_every_lamina,material)
    min_strength_ratio = sr_and_pos['min_strenght_ratio']
    return min_strength_ratio



def get_symmetry_list(half_list):
    upper_half = copy.deepcopy(half_list)
    half_list.reverse()
    return upper_half + half_list

if __name__=='__main__':

    #angle =[37] * 27 + [-37] * 27  
    #angle = tool.get_symmetry_list(angle)
    #material =[cv.T300_5308] * 54    
    #material = tool.get_symmetry_list(material)

    angle =[-18] * 34 + [17] * 72  + [-18] * 34 
    height=[0.00127] * 140 
    material =[cv.T300_5308] * 140    
    load=[120,5,0,0,0,0]


    sr  = get_strength_ratio(angle,height,material,load)
    with open("train_data_composite_material.csv",'a') as basic_io:
        csv_writer = csv.writer(basic_io)
        csv_writer.writerow([sr])

    mass = lmac.get_laminate_mass(height,material)
    cost = lmac.get_laminate_cost(material)
    print("strenght ratio: " + str(sr))
    print("mass: " + str(mass))
    print("cost:" + str(cost))

