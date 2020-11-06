class Individual(object):

    def __init__(self, angle_list, height_list, material_list):
        self.angle_list  = angle_list
        self.height_list = height_list
        self.material_list = material_list
        self.length = len(angle_list)
        self.strength_raito = -1
        self.mass = -1
        self.cost = -1
        self.fitness = -1

    def __str__(self):
        angle = str(self.angle_list)
        height = str(self.height_list)
        material = str(self.material_list)
        strength_raito = str(self.strength_raito)
        mass = str(self.mass)
        cost = str(self.cost)
        fitness = str(self.fitness)

        #return "angle: "+angle+" height: "+height+" material: "+material+"fitness: "+fitness
        return "SR " + strength_raito[0:6] + " mass: " + mass[0:6] + \
                " fitness: " + fitness[0:6] + " height: " + str(len(self.height_list))[0:6] + \
                " cost: " + cost
        #return "fitness: "+fitness



if __name__ == "__main__":
    a = Individual([1],[2],[3])
    print(a)

    
