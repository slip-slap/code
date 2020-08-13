class Individual(object):

    def __init__(self, angle_list, height_list, material_list):
        self.angle_list  = angle_list
        self.height_list = height_list
        self.material_list = material_list
        self.fitness = -1

    def __str__(self):
        angle = str(self.angle_list)
        height = str(self.height_list)
        material = str(self.material_list)
        fitness = str(self.fitness)
        return "angle: "+angle+" height: "+height+" material: "+material+"fitness: "+fitness



if __name__ == "__main__":
    a = Individual(1,2,3)
    print(a)

    
