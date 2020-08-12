from __future__ import print_function
import math
import random
import composite
from simanneal import Annealer

FACTOR1 = -3
FACTOR2 = 5
FACTOR3 = 9

class Multiply(Annealer):

    """Test annealer with a travelling salesman problem.
    """
    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state):
        super(Multiply, self).__init__(state)  # important!

    def move(self):
        self.state[0] = self.state[0]+random.random()-0.5
        self.state[1] = self.state[1]+random.random()-0.5
        self.state[2] = self.state[2]+random.random()-0.5

    def energy(self):
        """Calculates the length of the route."""
        e=self.state[0]*FACTOR1+self.state[1]*FACTOR2+self.state[2]*FACTOR3
        e=composite.get_population_fitness()

        return e



if __name__ == '__main__':

    init_state=[random.random()-0.5,random.random()-0.5,random.random()-0.5]
    tsp = Multiply(init_state)
    tsp.steps = 10000000
    # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()
    print(state)


