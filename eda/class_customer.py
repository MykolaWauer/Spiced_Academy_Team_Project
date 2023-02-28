# Create class for customer


import pandas as pd
import numpy as np
from numpy.random import choice

# Load in data that informs our functions which probability to use.
probabs = pd.read_csv('../probabilities.csv', index_col=0)
probabs.insert(3, 'entrance', 0.0)
print(probabs)




#States of Markov chain
STATES = ['checkout', 'dairy', 'drinks', 'entrance', 'fruit', 'spices']

class Customer:
    """
    A single customer that moves 
    through the supermarket in a MCMC simulation
    """
    
    def __init__(self, name, state='entrance', probabs = probabs):
        self.name = name
        self.state = state
        self.probabs = probabs
        self.history = ['entrance']


    def __repr__(self):
        return f'<Customer {self.name} in {self.state}>'
    
    def next_state(self):
        """
        Propagates the customer to the next state.
        Returns nothing.
        """
        
        while self.state != 'checkout':
            
            
            next_state = np.random.choice(STATES, p=probabs.loc[self.state].values)
            self.state = next_state
            print(f'curent state is {self.state}')




cust1 = Customer('Mykola')
print(cust1.next_state())


