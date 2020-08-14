import numpy as np

GLASS_EPOXY= 'glass_epoxy'
GRAPHITE_EPOXY = "graphite_epoxy"
BORON_EPOXY = "boron_epoxy"


# SI System of Units
glass_properties = {
                'sigma_1_tensile':np.float64(1062),
                'sigma_1_compressive':np.float64(610),
                'sigma_2_tensile':31,
                'sigma_2_compressive':118,
                'tau_12':72
             }

boron_properties = {
                'sigma_1_tensile':np.float64(1260),
                'sigma_1_compressive':np.float64(2500),
                'sigma_2_tensile':61,
                'sigma_2_compressive':202,
                'tau_12':67
             }
graphite_properties = {
                'sigma_1_tensile':np.float64(1500),
                'sigma_1_compressive': np.float64(1500),
                'sigma_2_tensile':40,
                'sigma_2_compressive':246,
                'tau_12':68
             }

# SI System of Units
GLASS_EPOXY_PROPERTIES     = {"E1":38.6,  "E2":8.27, "v12":0.26,  "G12":4.14 }
BORON_EPOXY_PROPERTIES     = {"E1":204,  "E2":18.5, "v12":0.23,  "G12":5.59 }
GRAPHITE_EPOXY_PROPERTIES  = {"E1":181,  "E2":10.3, "v12":0.28,  "G12":7.17 }

#properties = graphite_properties

def maximum_strain_failure_theory(component, material):
    if(material == GLASS_EPOXY):
        #global properties
        #global four_elastic_property
        properties = glass_properties
        four_elastic_property = GLASS_EPOXY_PROPERTIES
    if(material == GRAPHITE_EPOXY):
        properties = graphite_properties
        four_elastic_property = GRAPHITE_EPOXY_PROPERTIES

    sigma_1_ten = np.divide(properties['sigma_1_tensile'], \
                            four_elastic_property['E1'])
    sigma_1_com = -np.divide(properties['sigma_1_compressive'], \
                            four_elastic_property['E1'])
    sigma_2_ten = np.divide(properties['sigma_2_tensile'], \
                            four_elastic_property['E2'])
    sigma_2_com = -np.divide(properties['sigma_2_compressive'], \
                            four_elastic_property['E2'])
    tau12 = np.divide(properties['tau_12'],four_elastic_property['G12'])

    sr_sigma_1_tensile     = np.divide(sigma_1_ten,component[0])
    sr_sigma_1_compressive = np.divide(sigma_1_com, component[0])
    sr_sigma_2_tensile     = np.divide(sigma_2_ten,component[1])
    sr_sigma_2_compressive = np.divide(sigma_2_com, component[1])
    sr_tau_12_tensile      = np.divide(tau12, component[2])
    sr_tau_12_compressive  = np.divide(-tau12, component[2])

    sr_list = [sr_sigma_1_tensile, sr_sigma_1_compressive, sr_sigma_2_tensile, \
            sr_sigma_2_compressive,sr_tau_12_tensile, sr_tau_12_compressive]

    temp = []
    for i in range(len(sr_list)):
        if(sr_list[i]>0):
            temp.append(sr_list[i])
    return min(temp)

"""
1. A mechanical structure takes external forces, which act upon a body as surface
faces and body forces. These forces result in internal forces inside the body.
stress: the intensify of the load per unit area

2. Similar to the need for the knowledge of forces inside a body, knowing the
deformations because of the external forces is also important.
Finding stresses in a body generally requires finding deformations. This is
because a stress state at a point has six components.

local stress sigma_1, sigma_2, tau_12
"""
def maximum_stress_failure_theory(component, material):

    if(material == GLASS_EPOXY):
        #global properties
        properties = glass_properties
    if(material == GRAPHITE_EPOXY):
        properties = graphite_properties

    # tensile
    sr_sigma_1_tensile = np.divide(properties['sigma_1_tensile'],component[0])
    sr_sigma_1_compressive = -np.divide(properties['sigma_1_compressive'], \
                                                                 component[0])
    sr_sigma_2_tensile = np.divide(properties['sigma_2_tensile'],component[1])
    sr_sigma_2_compressive = -np.divide(properties['sigma_2_compressive'], \
                                                                 component[1])
    sr_tau_12_tensile = np.divide(properties['tau_12'], component[2])
    sr_tau_12_compressive = -np.divide(properties['tau_12'], component[2])

    sr_list = [sr_sigma_1_tensile, sr_sigma_1_compressive, sr_sigma_2_tensile, \
            sr_sigma_2_compressive,sr_tau_12_tensile, sr_tau_12_compressive]

    temp = []
    for i in range(len(sr_list)):
        if(sr_list[i]>0):
            temp.append(sr_list[i])

    return min(temp)



def tsai_hill_failure_theory():
    G1 = 0.5 * ( (np.divide(2,np.power(properties['sigma_2_tensile'],2))) - \
              (np.divide(1,np.power(properties['sigma_1_tensile'],2))) )
    G2 = 0.5 * np.divide(1,np.power(properties['sigma_1_tensile'],2))
    G3 = 0.5 * np.divide(1,np.power(properties['sigma_1_tensile'],2))
    G6 = 0.5 * np.divide(1, np.power(properties['tau_12'], 2))



"""
argument: sigma1 = 1.714S,sigma2 = -2.714S tau_12 = -4.165S
component=[1.714, -2.714, -4.165]
"""
def tsai_wu_failure_theory(component,material):

    #global properties
    if(material == GLASS_EPOXY):
        properties = glass_properties
    if(material == GRAPHITE_EPOXY):
        properties = graphite_properties
    if(material == BORON_EPOXY):
        properties = boron_properties

    h1 = np.divide(1, properties['sigma_1_tensile']) - \
         np.divide(1, properties['sigma_1_compressive'])
    h11 = np.divide(1, properties['sigma_1_tensile'] * \
                       properties['sigma_1_compressive'])
    h2 = np.divide(1, properties['sigma_2_tensile']) - \
         np.divide(1, properties['sigma_2_compressive'])
    h22 = np.divide(1, properties['sigma_2_tensile'] * \
                       properties['sigma_2_compressive'])
    h6 = 0
    h66 = np.divide(1,np.power(properties['tau_12'],2))
    temp = properties['sigma_1_tensile'] * properties['sigma_1_compressive']* \
           properties['sigma_2_tensile'] * properties['sigma_2_compressive']
    h12 = -0.5 * (np.divide(1, temp)**0.5)
    # H1*sigma1 + H2*sigma2 + H6*tau12 + 
    # H11*sigma1*sigma1 + H22*sigma2*sigma2 + H66*tau12*tau12
    # 2*H12*sigma1*sigma2 < 1 
    a0 = component[0];
    b0 = component[1];
    c0 = component[2];
    a = h11*a0*a0 + h22*b0*b0 + h66*c0*c0 + 2*h12*a0*b0
    b = h1*a0 + h2*b0 + h6 * c0
    c = -1
    determinant = np.power(b*b - 4*a*c,0.5)
    x1 = np.divide(-b + determinant, 2*a)
    #x2 = np.divide(-b - determinant, 2*a)
    #print(x1)
    return x1
    

if __name__ == "__main__":
    #tsai_wu_failure_theory([1.714, -2.714, -4.165],GRAPHITE_EPOXY)
    sr = maximum_stress_failure_theory([1.714, -2.714, -4.165],GRAPHITE_EPOXY)
    sr = maximum_strain_failure_theory([0.1369,-2.662,-5.809], GRAPHITE_EPOXY)
    print(sr)








# USCS System of Units
"""
glass_properties = {
                'sigma_1_tensile':np.float64(154.03),
                'sigma_1_compressive':np.float64(88.47),
                'sigma_2_tensile':4.496,
                'sigma_2_compressive':17.12,
                'tau_12':10.44
             }

boron_properties = {
                'sigma_1_tensile':np.float64(182.75),
                'sigma_1_compressive':np.float64(362.6),
                'sigma_2_tensile':8.847,
                'sigma_2_compressive':29.30,
                'tau_12':9.718
             }
graphite_properties = {
                'sigma_1_tensile':np.float64(217.56),
                'sigma_1_compressive': np.float64(217.56),
                'sigma_2_tensile':5.802,
                'sigma_2_compressive':35.68,
                'tau_12':9.863 
             }
"""
