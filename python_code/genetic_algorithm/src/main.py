import numpy as np
from genetic_algorithm import *
from individual import *
from plot import *


class Individual_Child(Individual):
    def get_individual_fitness(self):
        """TODO: Docstring for get_individual_fitness.
        :arg1: TODO
        :returns: TODO
        """
        decimal_value = self.binary_to_decimal()
        decimal_normalization_value = self.decimal_normalize(decimal_value)
        temp = np.cos(5.1*np.pi*decimal_normalization_value+0.5)
        fitness = np.power(temp,6)
        return fitness

    def binary_to_decimal(self):
        """TODO: Docstring for binary_to_decimal.
        :returns: decimal value
        """
        decimal = 0
        length = self.get_chromosome_length()
        for i in range(length):
            decimal = decimal + self.chromosome[i]*np.power(2,length-i-1)
        return decimal

    def decimal_normalize(self, decimal_value):
        return (1+decimal_value)/np.power(2,self.get_chromosome_length())


def initilize_population(population_number=10,chromosome_length=16):
    """TODO: Docstring for initize_population.

    :arg1: TODO
    :returns: initilize population

    """
    individual_list = [Individual_Child() for i in range(population_number)]
    for i in range(population_number):
        chromosome = list(np.random.randint(0, 2, chromosome_length,int))
        individual_list[i].set_individual_chromosome(chromosome)
        fitness = individual_list[i].get_individual_fitness()
        individual_list[i].set_individual_fitness(fitness)
    return individual_list

POPULATION_NUMBER = 10
CHROMOSOME_LENGTH = 16
            
ga = Genetic_Algorithm()
population = initilize_population(POPULATION_NUMBER, CHROMOSOME_LENGTH)
population.sort(key = lambda c: c.get_individual_fitness(),reverse=True)

for i in range(10):
    parents = ga.select_parents(population,4)
    offspring = ga.crossover(parents, 6)
    ga.mutation(offspring)

    population[0:4] = parents
    population[4:] = offspring
    population.sort(key = lambda c: c.get_individual_fitness(),reverse=True)
    for i in range(len(population)):
        print(population[i].get_individual_fitness())
        

data_x = np.arange(0,1,0.01) 


