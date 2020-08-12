import numpy as np
import lamina_failure as lf
import copy
# laminate stiffness matrices[A], [B],  and[D]
# input argu1 lamiCons: lamination construction
# lamiCons{'angle':{45, 30, 45, 90}, 'height':[3, 2, 1, 2]}
# input argu2 elasCons: elastic constants
ELASCONS = {"E1":26.25,  "E2":1.49, "v12":0.28,  "G12":1.04 }
ELASCONS = {"E1":5.6,  "E2":1.2, "v12":0.26,  "G12":0.60 }
ELASCONS = {"E1": 181,   "E2": 10.3,"v12": 0.28,  "G12":7.17}
ELASCONS = {"E1": 181*np.power(10,9),  "E2": 10.3*np.power(10,9),  \
           "v12": 0.28,  "G12":7.17*np.power(10,9) }

def calc_lamina_stiffness_matrix_Q():
    E1 = ELASCONS['E1']
    E2 = ELASCONS['E2']
    v12 = ELASCONS['v12']
    v21 = E2 * v12 / E1
    G12 = ELASCONS['G12']
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

def calc_lamina_stiffness_matriceQ_with_angle_theta(matriceQ,theta=0):
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
"""
def calc_laminate_stiffness_matrice(angle, height):

    A = B = D = np.zeros((3, 3))
    # initiaize
    Q = calc_lamina_stiffness_matrix_Q()
    coordinate_list = get_height_coordinate_list(height)
    for i in range(len(angle)):
        angle_Q = calc_lamina_stiffness_matriceQ_with_angle_theta(Q,angle[i])
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
                                       angle_list, height_list):

    Q = calc_lamina_stiffness_matrix_Q()
    coordinate_top_middle_bottom_list = get_height_coordinate_top_middle_bottom_list(height_list)
    global_strain = [];global_stress = [];local_strain = [];local_stress = [];
    # for every lamina
    for i in range(len(angle_list)):
        angle_Q = calc_lamina_stiffness_matriceQ_with_angle_theta(Q,angle_list[i])
        temp_strain_list = get_lamina_global_strain( \
                           midplane_strain_and_curvature,coordinate_top_middle_bottom_list, i) 
        global_strain.append(temp_strain_list)
        temp_stress_list = get_lamina_global_stress(angle_Q,temp_strain_list)
        global_stress.append(temp_stress_list)

        temp_local_strain_list = get_lamina_local_strain(angle_list[i],temp_strain_list)
        local_strain.append(temp_local_strain_list)
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
def get_failure_lamina(lamina_stress_strain):
    min_strenght_ratio = 10000000000000 
    failure_lamina_pos  = 0

    local_stress = lamina_stress_strain['local_stress']
    for i in range(len(local_stress)):
        for j in range(len(local_stress[i])):
            SR = lf.tsai_wu_failure_theory(local_stress[i][j])
            if(min_strenght_ratio > SR):
                min_strenght_ratio = SR
                failure_lamina_pos = i

    print(failure_lamina_pos)
    print(min_strenght_ratio)


# 0 1 2 correspond to 0 -45/45 90
def angle_decoder(population=np.random.randint(low=0, high=3, size=(24, 12))):
    population=population.astype(np.float)
    for i in range(0, population.shape[0]):
        for j in range(0, population[i, :].size):
            if population[i][j]==0:
                population[i][j]=0
            elif population[i][j]==2:
                population[i][j]=np.pi/2
            elif population[i][j]==1 and j%2==0 :
                population[i][j]=np.pi/4
            else:
                population[i][j]=-np.pi/4

    return population


#get population fitness
def get_population_fitness(population):
    lamiCons={'angle':np.zeros((1, 2)), 'height':np.zeros((1, 2))}
    lamiCons['height']=np.array([[0.30509, 0.30509, 0.30509, 0.30509, 0.30509, 0.30509, 0.30509, 0.30509, 0.30509, 0.30509, 0.30509, 0.30509]])
    fitList=[]
    afterDecodePopulation=angle_decoder(population)
    for i in range(0, afterDecodePopulation.shape[0]):
        lamiCons['angle']=afterDecodePopulation[i, :].reshape(1, -1)
        stiff=calc_stiffness_matrices(lamiCons)
        strain=calc_strain(np.array([[200, 50, 0, 0, 0, 0]]), stiff)
        eachLayerStressLTList=calc_each_layer_stress(lamiCons, strain[0:3])
        R=fitness(eachLayerStressLTList)
        fitList.append(1/R)
    result=np.array(fitList)
    return result

def get_possible_combination(basic_unit,repeat_times):
    temp = basic_unit * repeat_times
    symmetry_upper_part = copy.deepcopy(temp)
    temp.reverse()
    return symmetry_upper_part + temp


if __name__=='__main__':
    """
    population=np.random.randint(low=0, high=3, size=(1, 12))
    population[0, :]=[0, 1, 1, 2, 0, 1, 2, 0, 0, 0, 1, 1]
    population[1, :]=[1, 0, 0, 1, 1, 0, 2, 1, 0, 1, 0, 0]
    population[2, :]=[0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0]
    population[3, :]=[0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0]
    population[4, :]=[1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
    result=get_population_fitness(population)
    a=result[0]
    print(a)
    """
    #Q = calc_lamina_stiffness_matrix_Q()
    #angle_Q = calc_lamina_stiffness_matriceQ_with_angle_theta(Q,theta = -np.pi/4)

    angle = get_possible_combination([0,np.pi/2,np.pi/2],1)
    angle = get_possible_combination([np.pi/3, -np.pi/3],4)
    #angle = get_possible_combination([np.pi/3, -np.pi/3],5)
    #angle = get_possible_combination([np.pi/4, -np.pi/4,np.pi/4, -np.pi/4, \
    #    np.pi/3, -np.pi/3, np.pi/3, -np.pi/3,  np.pi/3, -np.pi/3, ],1)
    # angle = [0,np.pi/2,0]
    height=[0.005] * 16 
    load=[1,2,0,0,0,0]
    # calculate laminate stiffness
    laminate_stiffness = calc_laminate_stiffness_matrice(angle,height)
    # given load, calculate midplane stain and curvature
    midplane_strain_and_curvature = \
    calc_midplane_strain_and_curvature(laminate_stiffness,load)
    #coordinate_list = get_height_coordinate_list()
    stress_and_strain_of_every_lamina = calc_each_lamina_stress_and_strain(midplane_strain_and_curvature,angle, \
                            height)
    get_failure_lamina(stress_and_strain_of_every_lamina)







