import numpy as np
# laminate stiffness matrices[A], [B],  and[D]
# input argu1 lamiCons: lamination construction
# lamiCons{'angle':{45, 30, 45, 90}, 'height':[3, 2, 1, 2]}
# input argu2 elasCons: elastic constants
STRENGTHCONSTANT = {'Xt': 1722,  'Xc': 832,  'Yt': 60,  'Yc': 136,  'S': 113}
ELASCONS = {"E1": 141,  "E2": 9.7,  "mu21": 0.321,  "G12": 5}
def calc_stiffness_matrices(lamiCons = {'angle': np.zeros((1, 3)), 'height': np.zeros((1, 3))}):
    angle=lamiCons['angle']
    height=lamiCons['height']
    Q=calc_stiffness_matrices_Q()
    #Q=np.array([[20, 0.7, 0], [0.7, 2.0, 0], [0, 0, 0.7]])
    coordList=height_encode(height)

    #extensional stiffness matrix
    A=np.zeros((3, 3))
    #coupling stiffness matrix
    B=np.zeros((3, 3))
    # bending stiffness matrix
    D=np.zeros((3, 3))

    # calculate A
    for i in range(0, angle.size):
        inverse_T=calc_inverse_T(angle[0][i])
        temp_Q=np.dot(np.dot(inverse_T, Q), inverse_T.T)
        A=A+(coordList[i]-coordList[i+1])*temp_Q
        B=B+0.5*(coordList[i]*coordList[i]-coordList[i+1]*coordList[i+1])*temp_Q
        D=D+(1/3)*(coordList[i]*coordList[i]*coordList[i]-coordList[i+1]*coordList[i+1]*coordList[i+1])*temp_Q

    upper=np.hstack((A, B))
    down=np.hstack((B, D))
    stiffnessMatrix=np.vstack((upper, down))
    return stiffnessMatrix

def calc_stiffness_matrices_Q():
    mu12=ELASCONS['E1']*ELASCONS['mu21']/ELASCONS['E2']
    Q=np.zeros((3, 3))
    #Q11
    Q[0][0]=ELASCONS['E1']/(1-mu12*ELASCONS['mu21'])
    #Q12
    Q[0][1]=ELASCONS['E2']*mu12/(1-mu12*ELASCONS['mu21'])
    #Q16
    Q[0][2]=0
    #Q12
    Q[1][0]=Q[0][1]
    #Q22
    Q[1][1]=ELASCONS['E2']/(1-mu12*ELASCONS['mu21'])
    #Q26
    Q[1][2]=0
    #Q16
    Q[2][0]=Q[0][2]
    #Q26
    Q[2][1]=Q[1][2]
    #Q66
    Q[2][2]=ELASCONS['G12']
    return Q

# transform matrix
def calc_inverse_T(theta=np.pi/6):
    m=np.cos(theta)
    n=np.sin(theta)
    #transform matrix
    T=np.zeros((3, 3))
    T[0][0]=m*m
    T[0][1]=n*n
    T[0][2]=2*m*n
    T[1][0]=n*n
    T[1][1]=m*m
    T[1][2]=-2*m*n
    T[2][0]=-m*n
    T[2][1]=m*n
    T[2][2]=m*m-n*n
    # the inverse of T
    inverseT=np.linalg.inv(T)
    return inverseT

# strain transform matrix
def calc_strain_trans_matrix(theta=np.pi/6):
    m=np.cos(theta)
    n=np.sin(theta)
    #transform matrix
    strainT=np.zeros((3, 3))
    strainT[0][0]=m*m
    strainT[0][1]=n*n
    strainT[0][2]=m*n
    strainT[1][0]=n*n
    strainT[1][1]=m*m
    strainT[1][2]=-m*n
    strainT[2][0]=-2*m*n
    strainT[2][1]=2*m*n
    strainT[2][2]=m*m-n*n
    return strainT


# height encoding
def height_encode(height=np.array([[5, 3, 4, 6, 7, 9]])):
    totalHeight=0
    for i in range(0, height.size):
        totalHeight=totalHeight+height[0][i]

    coordList=[totalHeight/2]
    tempCoord=totalHeight/2
    for i in range(0, height.size):
        tempCoord=tempCoord-height[0][i]
        coordList.append(tempCoord)

    return coordList

# calculate epislon based on in-plane forces
# argu1  force Nx, Ny, Nxy, Mx, My, Mxy
# argu1 laminate stiffness_matrices
def calc_strain(force=np.array((1, 6)), stiffness=np.zeros((6, 6))):
    inverseStiffness=np.linalg.inv(stiffness)
    strain=np.dot(inverseStiffness, force.T)*1e-3
    return strain

# calcuate each layer stress
# argu1 lamiCons constructure
def calc_each_layer_stress(lamiCons={'angle':np.zeros((1, 3))}, strain=np.array((1, 3))):
    angle=lamiCons['angle']
    Q=calc_stiffness_matrices_Q()
    #Q=np.array([[20, 0.7, 0], [0.7, 2.0, 0], [0, 0, 0.7]])
    stressMatrice=[]
    for i in range(0, angle.size):
        inverse_T=calc_inverse_T(angle[0][i])
        temp_Q=np.dot(np.dot(inverse_T, Q), inverse_T.T)
        # calculate stress
        stress=np.dot(temp_Q, strain)
        # calculate sigma L, sigma T, tau LT
        stressLT=np.dot(np.linalg.inv(inverse_T), stress)
        stressMatrice.append(stressLT)

        # calculate epislon L, epislon T, gamma LT
        #strain_transform_matrix=calc_strain_trans_matrix(angle[0][i])
        #strainLT=np.dot(strain_transform_matrix, strain)

    return stressMatrice



# based on Tsai-Wu princinple
# argu1 strengthConstant strengthConstant={Xt:0, Xc:0, Yt:0, Yc:0, S:0}
# argu2 stress stress={'sigma1':0, 'sigma2':0, 'tau12':0}
def fitness(eachLayerStressLTList):
    # calculate F11, F12, F22, F66, F1, F2
    F1=1/STRENGTHCONSTANT['Xt']-1/STRENGTHCONSTANT['Xc']
    F11=1/(STRENGTHCONSTANT['Xt']*STRENGTHCONSTANT['Xc'])
    F2=1/STRENGTHCONSTANT['Yt']-1/STRENGTHCONSTANT['Yc']
    F22=1/(STRENGTHCONSTANT['Yt']*STRENGTHCONSTANT['Yc'])
    F66=1/(STRENGTHCONSTANT['S']*STRENGTHCONSTANT['S'])
    F12=-0.5*np.sqrt(1/(STRENGTHCONSTANT['Xt']*STRENGTHCONSTANT['Xc']*STRENGTHCONSTANT['Yt']*STRENGTHCONSTANT['Yc']))

    # fit value list
    fitList=[]
    for i in  eachLayerStressLTList:
        # calcuate AR2+BR-1=0 A and B
        A=F11*i[0][0]*i[0][0]+F22*i[1][0]*i[1][0]+2*F12*i[0][0]*i[1][0]+F66*i[2][0]*i[2][0]
        B=F1*i[0][0]+F2*i[1][0]
        R=(-B+np.sqrt(B*B+4*A))/(2*A)
        fitList.append(R)

    return min(fitList)

# translate integer into angle which based on the encoding rule
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

if __name__=='__main__':
    population=np.random.randint(low=0, high=3, size=(1, 12))
    """
    population[0, :]=[0, 1, 1, 2, 0, 1, 2, 0, 0, 0, 1, 1]
    population[1, :]=[1, 0, 0, 1, 1, 0, 2, 1, 0, 1, 0, 0]
    population[2, :]=[0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0]
    population[3, :]=[0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0]
    population[4, :]=[1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
    """
    result=get_population_fitness(population)
    a=result[0]
    print(a)











