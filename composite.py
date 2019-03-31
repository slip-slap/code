import numpy as np
# laminate stiffness matrices[A],[B], and[D]
# input argu1 lamiCons: lamination construction
# lamiCons{'angle':{45,30,45,90},'height':[3,2,1,2]}
# input argu2 elasCons: elastic constants
def calc_stiffness_matrices(lamiCons={'angle':np.zeros((1,3)),'height':np.zeros((1,3))}),elasCons={"E1":1,"E2":2,"mu21":0.1,"G12":3}:
    angle=lamiCons['angle']
    height=lamiCons['height']
    Q=calc_stiffness_matrices_Q(elasCons)
    # 最终刚度为A
    ？？？？？？？？？？？？？？？？？？
    # calculate A
    for i in range(0,angle.size):
        inverse_T=calc_inverse_T(angle[0][i])
        Q=np.dot(np.dot(inverseT,Q),inverseT.T)
        A=height[0][i]*Q
        # print stiffness A
        print("stiffness A is ")
        print(A)


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



if __name__=='__main__':
    #cons={"E1":3.9e4,"E2":1.3e4,'mu21':0.25,'G12':0.42e4}
    #calc_stiffness_matrices(cons)
    #laminate_angle()
    lamiCons={'angle':np.zeros((1,3)),'height':np.zeros((1,3))})
    elasCons={"E1":1,"E2":2,"mu21":0.1,"G12":3}:
    calc_stiffness_matrices(lamiCons,elasCons)







