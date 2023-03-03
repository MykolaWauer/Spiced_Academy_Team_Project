"""Creates a DataFrame and a CSV file which tracks customer behavior
inside a fake grocery store, using probabilities which can be changed.

Returns:
    _DataFrame_: A DataFrame with 'time','id', and 'location' columns.
"""
import pandas as pd
from customer import Customer

class Supermarket:
    """
    Simulates an entire day of a store.
    """

    def __init__(self, no_customers) -> None:
        self.no_customers = no_customers+1

    def sim_day(self):
        """Simulates a full day of customer behavior.

        Returns:
            _DataFrame_: Contains 'time', 'id', and 'location'
        """

        cust_list = range(1, self.no_customers)

        df_full = pd.DataFrame()

        for cust in cust_list:
            customer_name = f'{cust}'
            customer_obj = Customer(customer_name)
            temp_df = customer_obj.sim_day()
            df_full = pd.concat([df_full, temp_df])

        df_full.sort_values('time', inplace=True)
        df_full.set_index('time', inplace=True)

        return df_full

    def make_csv(self, df_full):
        """Creates a CSV file

        Args:
            df_full (_DataFrame_): A DataFrame to save.
        """

        df_full.to_csv(f'../data/{store_name}.csv')


if __name__ == "__main__":
    print("\nLet's simulate a day in your store! \n")

    store_name = input("What is the name of your store?\n")
    cus_no = int(input("How many customers will visit your store?\n"))
    printing = input("Would you like to print? [y/n]\n")

    store = Supermarket(cus_no)

    df = store.sim_day()
    store.make_csv(df)

    if printing in ('y', 'yes'):

        print(f"\nToday at {store_name}, {cus_no} people visited these places:")
        with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                        'display.precision', 3,
                        ):
            print(df)
