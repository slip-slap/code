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

        for i in range(offspring_number):
            parent1_pos = int(np.random.randint(0, len(parents), 1))
            parent2_pos = int(np.random.randint(0, len(parents), 1))
            parent1_chromosome = parents[parent1_pos].get_individual_chromosome()
            parent1_node_number = parents[parent1_pos].node_number
            parent2_chromosome = parents[parent2_pos].get_individual_chromosome()
            parent2_node_number = parents[parent2_pos].node_number

            child_node_number = \
                int(parent1_node_number/2)+int(parent2_node_number/2)
            child_chromosome = list(np.empty(child_node_number*13,int))


            crossover_point1 = (int(parent1_node_number/2))*13
            child_chromosome[0:] \
            = parent1_chromosome[0:crossover_point1]

            crossover_point2 = (int(parent2_node_number/2))*13
            child_chromosome[crossover_point1:] \
            = parent2_chromosome[0:crossover_point2]

            child_activation_function_chromosome = \
            list(np.empty(child_node_number*2,int))

            crossover_point1_flag=  (int(parent1_node_number/2))*2
            child_activation_function_chromosome[0:] = \
                    parents[parent1_pos].activation_function_chromosome[0:crossover_point1_flag]

            crossover_point2_flag=  (int(parent2_node_number/2))*2
            child_activation_function_chromosome[crossover_point1_flag:]\
                    =parents[parent2_pos].activation_function_chromosome[0:crossover_point2_flag]

            child = copy.deepcopy(parents[0])
            child.set_individual_chromosome(child_chromosome)
            child.activation_function_chromosome = \
            child_activation_function_chromosome
            child.node_number = child_node_number
            child.fitness = -1
            offspring.append(child)
        return offspring
            

    def mutation(self, offspring):
        """TODO: Docstring for mutation.
        :returns: None
        """
        for i in range(len(offspring)):
            chromosome_length = len(offspring[i].chromosome)
            mutation_pos = int(np.random.randint(0,chromosome_length,1))
            chromosome = offspring[i].get_individual_chromosome()
            chromosome[mutation_pos] = 1 - chromosome[mutation_pos]
            offspring[i].set_individual_chromosome(chromosome)


    def get_individual_fitness(self, object):
        """TODO: Docstring for get_individual_fitness.
        :returns: fitness value of individual

        """
        pass


