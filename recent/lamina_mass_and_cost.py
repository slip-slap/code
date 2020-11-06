import numpy as np
import constant_variable as cv

LAMINATE_LENGTH = 1
LAMINATE_WIDTH =  1


def get_lamina_mass(volume,material):
    fiber = material.split('_')[0]
    matrice = material.split('_')[1]
    if(fiber == "glass"):
        density = cv.GLASS_EPOXY_DENSITY
    if(fiber == "graphite"):
        density = cv.GRAPHITE_EPOXY_DENSITY
    if(fiber == "carbon"):
        density = cv.CARBON_EPOXY_DENSITY
    else:
        density = 1

    return volume*density/1000



def get_laminate_mass(height,material):
    mass = 0
    for i in range(len(height)):
        volume = LAMINATE_WIDTH * LAMINATE_LENGTH * height[i]*100
        lamina_mass = get_lamina_mass(volume,material[i])
        mass = mass + lamina_mass
    return mass


def get_laminate_cost(material):
    cost = 0
    for i in range(len(material)):
        if(material[i] == 'glass_epoxy'):
            cost = cost + cv.GLASS_EPOXY_COST
        if(material[i] == 'graphite_epoxy'):
            cost = cost + cv.GRAPHITE_EPOXY_COST
        if(material[i] == 'carbon_epoxy'):
            cost = cost + cv.CARBON_EPOXY_COST
    return cost




if __name__ == "__main__":
    #volume = 4*100*20*0.5
    #mass = get_lamina_mass(volume,'glass_epoxy')
    #mass = get_lamina_mass(volume,'graphite_epoxy')
    #mass = get_lamina_mass(volume,'glass_epoxy')
    mass = get_laminate_mass([0.005]*4,["graphite_epoxy"]*4)
    print(mass)
    mass = get_laminate_mass([0.005]*4,["glass_epoxy"]*4)
    print(mass)
    print(get_laminate_cost(['graphite_epoxy']*9))

"""
def get_lamina_mass(volume,material):
    fiber = material.split('_')[0]
    matrice = material.split('_')[1]
    if(fiber == "glass"):
        fiber_volume_fraction = FIBER_VOLUME_FRACTION_GLASS_EPOXY
        fiber_specific_gravity = FIBER_SPECIFIC_GRAVITY_GLASS
    if(fiber == "graphite"):
        fiber_volume_fraction = FIBER_VOLUME_FRACTION_GRAPHITE_EPOXY
        fiber_specific_gravity = FIBER_SPECIFIC_GRAVITY_GRAPHITE
    if(fiber == "boron"):
        fiber_volume_fraction = FIBER_VOLUME_FRACTION_BORON_EPOXY
        fiber_specific_gravity = FIBER_SPECIFIC_GRAVITY_BORON

    if(matrice == 'epoxy'):
        matric_specific_gravity = MATRIC_SPECIFIC_GRAVITY_EPOXY

    
    density = fiber_specific_gravity * fiber_volume_fraction + \
            matric_specific_gravity *  (1 -  fiber_volume_fraction)
    return volume * density/1000
"""
