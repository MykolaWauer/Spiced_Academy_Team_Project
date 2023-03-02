import pandas as pd
from customer import Customer

class Supermarket:
    """
    Simulates an entire day of a store.
    """

    def __init__(self, no_customers) -> None:
        self.no_customers = no_customers+1

    def sim_day(self):

        cust_list = range(1, self.no_customers)

        df_full = pd.DataFrame()

        for cust in cust_list:
            customer_name = f'{cust}'
            customer_obj = Customer(customer_name)
            temp_df = customer_obj.next_state()
            df_full = pd.concat([df_full, temp_df])
        
        df_full.sort_values('time', inplace=True)
        df_full.set_index('time', inplace=True)

        return df_full
    
if __name__ == "__main__":
    print("Let's simulate a day in your store! \n")
    store_name = input("What is the name of your store? ")
    cus_no = int(input("How many customers will visit your store? "))
    store = Supermarket(cus_no)
    print(f"\nToday at {store_name}, {cus_no} people visited the store and went around to these places.")
    
    with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
        print(store.sim_day())