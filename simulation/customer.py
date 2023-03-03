"""Used for tracking one simulated customer's entire journey
inside a grocery store.

Returns:
    _DataFrame_: Has columns 'time' (in datetime format), 'id', and 
    'location'.
"""
import pandas as pd
import numpy as np

# Import time probabilities and manipulate time column
time_probs = pd.read_csv('../data/cust_times.csv')
time_probs['time'] = pd.to_datetime(time_probs['time'])
time_probs.set_index('time', inplace=True)

# Load in existing customer data
cust_probs = pd.read_csv('../data/probabilities.csv', index_col=0)

# Create a list of possible states that does not include
# entrance because no customer can return to the entrance.
states = cust_probs.drop('entrance').index

class Customer:
    """
    Creates a single customer that moves through the supermarket in a 
    MCMC simulation.
    """
    def __init__(self, name, state='entrance'):
        self.name = name
        self.state = state
        self.history = []
        self.time = np.random.choice(time_probs.index, p=time_probs.probability)
        self.times = [self.time]
        self.close_time = '21:51:00'


    def __repr__(self):
        return f'<Customer {self.name} in {self.state}>'

    def sim_day(self):
        """
        Simulates one customer's entire visit to the store.

        Returns:
            _DataFrame_: Contains 'time', 'id', and 'location'
        """

        while self.state != 'checkout':

            next_state = np.random.choice(states, p=cust_probs.loc[self.state])

            self.time += pd.Timedelta('1 minute')

            if str(self.time)[11:] == self.close_time:
                self.state = 'checkout'
                self.history.append(self.state)
                self.times.append(self.time)

            else:
                self.times.append(self.time)
                self.history.append(self.state)
                self.state = next_state

        self.state = 'checkout'
        self.history.append(self.state)
        self.times.append(self.time)

        df_times = pd.DataFrame(self.times)
        df_visited = pd.DataFrame(self.history)

        df_combined = pd.merge(df_times,
                               df_visited,
                               left_index=True,
                               right_index=True
                               )

        df_combined.columns = ['time','location']
        df_combined['id'] = self.name
        df_combined = df_combined[['time','id','location']]

        return df_combined

if __name__ == "__main__":
    print("\nHello and welcome! \n")

    cus_name = input("What is your name?\n")

    print("\nLet's see where you went today...:\n")

    cus_name = Customer(cus_name)
    print(cus_name.sim_day())
