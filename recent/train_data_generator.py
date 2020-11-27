"""
Maitain constant variable will be used in this program
"""
import numpy as np

import laminate_multiple_component as lmc
import constant_variable as cv 
import csv


cv.LOAD = [120, 5, 0, 0, 0 ,0]

cv.GLASS_EPOXY= 'glass_epoxy'
cv.GRAPHITE_EPOXY = "graphite_epoxy"
cv.CARBON_EPOXY = "carbon_epoxy"
cv.T300_5308 = "T300_5308"

cv.GLASS_EPOXY_PROPERTIES     = {"E1":38.6,  "E2":8.27, "v12":0.26,  "G12":4.14 }
cv.CARBON_EPOXY_PROPERTIES    = {"E1":116.6,  "E2":7.673, "v12":0.27,  "G12":4.173 }
cv.GRAPHITE_EPOXY_PROPERTIES  = {"E1":181,  "E2":10.3, "v12":0.28,  "G12":7.17 }
cv.T300_5308_PROPERTIES = {"E1":40.91,  "E2":9.88, "v12":0.292,  "G12":2.84 }

cv.LAYER_HEIGHT = 0.00127

angle1 = 10
angle2 = -10
layer = 8
height = 0.00127

glass_properties = {
                'sigma_1_tensile':np.float64(1062),
                'sigma_1_compressive':np.float64(610),
                'sigma_2_tensile':31,
                'sigma_2_compressive':118,
                'tau_12':72
             }

carbon_properties = {
                'sigma_1_tensile':np.float64(2062),
                'sigma_1_compressive':np.float64(1701),
                'sigma_2_tensile':70,
                'sigma_2_compressive':240,
                'tau_12':105
             }

graphite_properties = {
                'sigma_1_tensile':np.float64(1500),
                'sigma_1_compressive': np.float64(1500),
                'sigma_2_tensile':40,
                'sigma_2_compressive':246,
                'tau_12':68
             }

cv.GLASS_EPOXY_PROPERTIES     = {"E1":38.6,  "E2":8.27, "v12":0.26,  "G12":4.14 }
cv.CARBON_EPOXY_PROPERTIES    = {"E1":116.6,  "E2":7.673, "v12":0.27,  "G12":4.173 }
cv.GRAPHITE_EPOXY_PROPERTIES  = {"E1":181,  "E2":10.3, "v12":0.28,  "G12":7.17 }


def save_to_data(angle_list,material_list, height_list):
    cv.FAILURE_CRITERIA = "max_stress"
    max_stress_sr  = lmc.get_strength_ratio(angle_list,height_list,material_list,cv.LOAD)
    cv.FAILURE_CRITERIA = "tsai_wu"
    tsai_wu_sr  = lmc.get_strength_ratio(angle_list,height_list,material_list,cv.LOAD)
    print(max_stress_sr)
    print(tsai_wu_sr)

    with open("train_data_composite_material.csv",'a') as basic_io:
        csv_writer = csv.writer(basic_io)
        csv_writer.writerow([cv.LOAD[0],cv.LOAD[1], str(cv.LOAD[2]),
            '   ' + str(angle1), angle2, layer, str(height*1000), 
            '   ' + str(material_property['E1']), str(material_property['E2']), str(material_property['v12']), str(material_property['G12']),
            '   ' + str(failure_property['sigma_1_tensile']), str(failure_property['sigma_1_compressive']), 
            str(failure_property['sigma_2_tensile']), str(failure_property['sigma_2_compressive']),
            str(failure_property['tau_12']),
            '    ' + str(tsai_wu_sr), max_stress_sr])

for material in [ cv.GLASS_EPOXY, cv.GRAPHITE_EPOXY, cv.CARBON_EPOXY]:
    if(material == cv.GLASS_EPOXY):
        material_property = cv.GLASS_EPOXY_PROPERTIES
        failure_property = glass_properties
    if(material == cv.GRAPHITE_EPOXY):
        material_property= cv.GRAPHITE_EPOXY_PROPERTIES
        failure_property = graphite_properties
    if(material == cv.CARBON_EPOXY):
        material_property= cv.CARBON_EPOXY_PROPERTIES
        failure_property = carbon_properties 

    for angle in range(0,91,1):
        
        angle_list = [angle, -angle] * int(layer/2)
        material_list = [material] * layer
        height_list = [height] * layer
        for layer in range(2,200,2):
            save_to_data(angle_list, material_list, height_list)


