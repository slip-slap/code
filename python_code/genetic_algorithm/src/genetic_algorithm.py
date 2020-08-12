import numpy as np
import copy
import individual



class Genetic_Algorithm(object):

    """Docstring for Genetic_Algorithm. """

    def __init__(self):
        """TODO: to be defined. """
        pass

    def select_parents(self, population,  num_parents):
        """TODO: Docstring for select_parents.
        Parameters
        :population: the list of population must be sorted by fitness from up to
        down
        ----------
        Returns parents
        -------
        """
        parents = population[0:num_parents]
        return parents

    def crossover(self, parents, offspring_number):
        """TODO: Docstring for crossover.
        :returns: offspring
        """
        offspring = []
        chromosome_length = parents[0].get_chromosome_length()
        crossover_point = int(chromosome_length/2)

        for i in range(offspring_number):
            parent1_pos = int(np.random.randint(0, len(parents), 1))
            parent2_pos = int(np.random.randint(0, len(parents), 1))
            parent1_chromosome = parents[parent1_pos].get_individual_chromosome()
            parent2_chromosome = parents[parent2_pos].get_individual_chromosome()
            child_chromosome = list(np.empty(chromosome_length,int))
            child_chromosome[0:crossover_point] \
            = parent1_chromosome[0:crossover_point]
            child_chromosome[crossover_point:] \
            = parent2_chromosome[crossover_point:]

            child = copy.deepcopy(parents[0])

            child.set_individual_chromosome(child_chromosome)
            offspring.append(child)
        return offspring
            

    def mutation(self, offspring):
        """TODO: Docstring for mutation.
        :returns: None
        """
        chromosome_length = offspring[0].get_chromosome_length()
        for i in range(len(offspring)):
            mutation_pos = int(np.random.randint(0,chromosome_length,1))
            chromosome = offspring[i].get_individual_chromosome()
            chromosome[mutation_pos] = 1 - chromosome[mutation_pos]
            offspring[i].set_individual_chromosome(chromosome)


    def get_individual_fitness(self, object):
        """TODO: Docstring for get_individual_fitness.
        :returns: fitness value of individual

        """
        pass


