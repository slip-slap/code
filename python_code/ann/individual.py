class Individual(object):

    """Docstring for Individual. """
    def __init__(self):
        self.fitness = None 
        self.chromosome = None
        self.chromosome_length = None

    def __str__(self):
        """TODO: Docstring for __str__.
        :returns: 

        """
        fitness = str(self.fitness)
        chromosome = str(self.chromosome)
        return "fitness is " + fitness + "; chromosome is " + chromosome

    def get_individual_fitness(self):
        """TODO: Docstring for get_individual_fitness.
        :returns: fitness of individual
        """
        return self.fitness

    def set_individual_fitness(self, fitness):
        """TODO: Docstring for set_individual_fitness.
        :returns: void
        """
        self.fitness = fitness


    def get_individual_chromosome(self):
        """TODO: Docstring for get_individual_chromosome.
        :returns: void
        """
        return  self.chromosome

    def set_individual_chromosome(self, chromosome):
        """TODO: Docstring for set_individual_chromosome.
        :returns: void
        """
        self.chromosome = chromosome

    def get_chromosome_length(self):
        """TODO: Docstring for get_chromosome_length.
        :returns: chromosome length

        """
        return len(self.chromosome)







