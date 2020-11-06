def save_to_output(result_fitness, result_strength_ratio, my_best_individual):
    with open("seed_test.py","a") as result_handler:
        result_handler.write("##################################")
        result_handler.write("\n")
        result_handler.write(cv.prefix + "load=  " + str(cv.LOAD))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "material=  " + str(cv.MATERIAL))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "angle=  " + str(cv.ANGLE))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "fitness_ =  " + str(result_fitness))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "strength_ratio_= "+ str(result_strength_ratio))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "cost= "+ str(my_best_individual.cost))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "mass= "+ str(my_best_individual.mass))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "strength_raito= "+ str(my_best_individual.strength_raito))
        result_handler.write("\n")
        result_handler.write(cv.prefix + "number_of_layer= "+ str(len(my_best_individual.material_list)))
        result_handler.write("\n")

        stacking_sequence = []
        angle_list_copy = copy.deepcopy(my_best_individual.angle_list)
        for i in range(len(angle_list_copy)):
            angle_list_copy[i] = get_concerter_angle(angle_list_copy[i])
        for i in range(len(angle_list_copy)):
            stacking_sequence.append(angle_list_copy[i])
            stacking_sequence.append(my_best_individual.material_list[i])
        result_handler.write("#stacking sequence= "+ str(stacking_sequence))
        result_handler.write("\n")
        result_handler.write("##################################")
        result_handler.write("\n")
