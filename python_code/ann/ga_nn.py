import numpy as np
import genetic_algorithm as ga
import individual  as ind
import plot as my_plot
import network_with_chromosome as train
import valuation as valuate
import data

my_data = data.data()
test_data= my_data.get_test_data()
test_data_input = test_data[:,0:13]
test_data_output = test_data[:,13].reshape(test_data_input.shape[0],1)

def binary_to_decimal(binary_number):
    """TODO: Docstring for binary_to_decimal.
    :returns: decimal value
    """
    decimal = 0
    for i in range(len(binary_number)):
        decimal = decimal + binary_number[i]*np.power(2,len(binary_number)-i-1)
    return int(decimal)

def activation_function_name(activation_function_code):
    if(activation_function_code == 0):
        return "sigmoid"
    if(activation_function_code == 1):
        return "relu"
    if(activation_function_code == 2):
        return "tanh"
    if(activation_function_code == 3):
        return "softmax"


def chromosome_to_gene_list(chromosome,unit_length):
    gene_number = len(chromosome)/unit_length
    gene_list= list()
    i = 0
    while(i<gene_number):
        temp = chromosome[i:i+unit_length]
        gene_list.append(temp)
        i=i+1
    return gene_list


class Individual_Child(ind.Individual):
    def __init__(self, node_number):
        self.node_number = node_number
        self.fitness = -1 
        self.activation_function_chromosome=None

    def calculate_individual_fitness(self):
        """TODO: Docstring for calculate_individual_fitness.
        self.fitness = int(np.random.randint(0,15,1))
        """
        if(self.fitness == -1):
            gene_list = chromosome_to_gene_list(self.chromosome,13)
            activation_function_list = \
            chromosome_to_gene_list(self.activation_function_chromosome,2)
            train.train_network(gene_list,activation_function_list)
            self.fitness = valuate.get_cell_result(test_data_input, \
                           test_data_output, \
                           meta_graph="./trained_model/chrosome/model.meta",\
                           checkpoint='./trained_model/chrosome')
        return self.fitness

def initilize_population(population_number=10,gene_length=13):
    """TODO: Docstring for initize_population.

    :arg1: TODO
    :returns: initilize population

    """
    individual_list = list()
    for i in range(population_number):
        node_number = np.random.randint(3,12,1)[0]
        chromosome_length = gene_length*node_number
        temp_individual = Individual_Child(node_number)
        chromosome = list(np.random.randint(0, 2, chromosome_length,int))
        temp_individual.set_individual_chromosome(chromosome)
        temp_individual.activation_function_chromosome = \
        list(np.random.randint(0,2,node_number*2,int))
        temp_individual.fitness = temp_individual.calculate_individual_fitness()
        individual_list.append(temp_individual)
    return individual_list

            
my_ga = ga.Genetic_Algorithm()
population = initilize_population()
population.sort(key = lambda c: c.fitness,reverse=True)

previous_fitness = 0 
current_fitness = population[0].fitness
print("current_fitness "+str(current_fitness))

while(current_fitness-previous_fitness>0.001):
    parents = my_ga.select_parents(population,4)
    offspring = my_ga.crossover(parents, 6)
    my_ga.mutation(offspring)
    for i in range(len(offspring)):
        offspring[i].fitness = offspring[i].calculate_individual_fitness()
    population[0:4] = parents
    population[6:] = offspring
    population.sort(key = lambda c: c.fitness,reverse=True)

    previous_fitness = current_fitness
    current_fitness = population[0].fitness

    # save top 3 parents in each generation
    for i in range(1):
        with open("network_train_result.txt","a") as train_handler:
            train_handler.write("chromosome length " \
                    +str(len(population[i].chromosome)))
            #train_handler.write("\n")
            gene_list = chromosome_to_gene_list(population[i].chromosome,13)
            transfer_function_list = \
            chromosome_to_gene_list(population[i].activation_function_chromosome,2)

            for k in range(len(gene_list)):
                train_handler.write("\n")
                train_handler.write(str(gene_list[k]))
                train_handler.write("  ")
                train_handler.write(str(transfer_function_list[k]))
                train_handler.write("  ")
                code_int = binary_to_decimal(transfer_function_list[k])
                train_handler.write(activation_function_name(code_int))

            train_handler.write("\n")
            train_handler.write("fitness: " +str(population[i].fitness))
            train_handler.write("\n")
            train_handler.write("node_number: " +str(population[i].node_number))
            train_handler.write("\n")
            train_handler.write("-------------------------------------") 
            train_handler.write("\n")
                    

#data_x = np.arange(0,1,0.01) 


