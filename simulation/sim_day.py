import pandas as pd
from customer import Customer

class Supermarket:
    """
    Simulates an entire day of a store.
    """

    def __init__(self, no_customers) -> None:
        self.no_customers = no_customers

    def sim_day(self):

        cust_list = range(1, self.no_customers+1)

        df_full = pd.DataFrame()

        for cust in cust_list:
            customer_name = f'{cust}'
            customer_obj = Customer(customer_name)
            temp_df = customer_obj.next_state()
            df_full = pd.concat([df_full, temp_df])
        
        df_full.sort_values('time', inplace=True)
        df_full.set_index('time', inplace=True)

        return df_full