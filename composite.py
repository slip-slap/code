import numpy as np
# laminate stiffness matrices[A],[B], and[D]
# input argu1 lamiCons: lamination construction
# lamiCons{'angle':{45,30,45,90},'height':[3,2,1,2]}
# input argu2 elasCons: elastic constants
def calc_stiffness_matrices(lamiCons={'angle':np.zeros((1,3)),'height':np.zeros((1,3))},elasCons={"E1":1,"E2":2,"mu21":0.1,"G12":3}):
    angle=lamiCons['angle']
    height=lamiCons['height']
    Q=calc_stiffness_matrices_Q(elasCons)
    Q=np.array([[20,0.7,0],[0.7,2.0,0],[0,0,0.7]])
    coordList=height_encode(height)

    #extensional stiffness matrix
    A=np.zeros((3,3))
    #coupling stiffness matrix
    B=np.zeros((3,3))
    # bending stiffness matrix
    D=np.zeros((3,3))

    # calculate A
    for i in range(0,angle.size):
        inverse_T=calc_inverse_T(angle[0][i])
        temp_Q=np.dot(np.dot(inverse_T,Q),inverse_T.T)
        A=A+(coordList[i]-coordList[i+1])*temp_Q
        B=B+0.5*(coordList[i]*coordList[i]-coordList[i+1]*coordList[i+1])*temp_Q
        D=D+(1/3)*(coordList[i]*coordList[i]*coordList[i]-coordList[i+1]*coordList[i+1]*coordList[i+1])*temp_Q

    print(A)
    print(B)
    print(D)

def calc_stiffness_matrices_Q(elasCons={"E1":1,"E2":2,"mu21":0.1,"G12":3}):
    mu12=elasCons['E1']*elasCons['mu21']/elasCons['E2']
    Q=np.zeros((3,3))
    #Q11
    Q[0][0]=elasCons['E1']/(1-mu12*elasCons['mu21'])
    #Q12
    Q[0][1]=elasCons['E2']*mu12/(1-mu12*elasCons['mu21'])
    #Q16
    Q[0][2]=0
    #Q12
    Q[1][0]=Q[0][1]
    #Q22
    Q[1][1]=elasCons['E2']/(1-mu12*elasCons['mu21'])
    #Q26
    Q[1][2]=0
    #Q16
    Q[2][0]=Q[0][2]
    #Q26
    Q[2][1]=Q[1][2]
    #Q66
    Q[2][2]=elasCons['G12']
    return Q

# transform matrix
def calc_inverse_T(theta=np.pi/6):
    m=np.cos(theta)
    n=np.sin(theta)
    #transform matrix
    T=np.zeros((3,3))
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

# height encoding
def height_encode(height=np.array([[5,3,4,6,7,9]])):
    totalHeight=0
    for i in range(0,height.size):
        totalHeight=totalHeight+height[0][i]

    coordList=[totalHeight/2]
    tempCoord=totalHeight/2
    for i in range(0,height.size):
        tempCoord=tempCoord-height[0][i]
        coordList.append(tempCoord)

    return coordList


if __name__=='__main__':
    lamiCons={'angle':np.zeros((1,2)),'height':np.zeros((1,2))}
    lamiCons['angle']=np.array([[0,np.pi/4]])
    lamiCons['height']=np.array([[5,3]])
    elasCons={"E1":1,"E2":2,"mu21":0.1,"G12":3}
    calc_stiffness_matrices(lamiCons,elasCons)







