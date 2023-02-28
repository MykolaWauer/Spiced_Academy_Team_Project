import pandas as pd
from datetime import (datetime,
                      timedelta)

import os

def create_dt(df_, column='timestamp'):
    
    df_[column] = pd.to_datetime(df_[column])
    
    df_['day'] = df_[column].dt.day
    
    return df_

def make_checkout(df_):
    check_out = df_.loc[df_.location=='checkout']['customer_no'].unique()
    
    no_check_out = df_[~df_['customer_no'].isin(check_out)]['customer_no'].unique()
    
    day = df_.loc[df_.index == 0]['day'].values[0]
    
    new_list = []
    
    for customer in no_check_out:
        new_row = {'timestamp':f'2019-09-{day} 21:51:00',
                   'customer_no':customer,
                   'location':'checkout',
                   'day':day
                  }
    
        new_obs = pd.DataFrame(new_row, index=[1])
        new_list.append(new_obs)
        
    
    test_df = pd.concat(new_list) 
    
    test_df['timestamp'] = pd.to_datetime(test_df['timestamp'])
    
    df_ = pd.concat([df_,test_df], ignore_index=True, axis=0)
    
    return df_

def entrance(df_):
    df_test = (df_
               .groupby('new_id')[['timestamp']]
               .first()
               .transform(lambda x: x - timedelta(minutes=1))
               .reset_index())
    
    df_test['location'] = 'entrance'
    
    df_combined = pd.concat([df_[['new_id','timestamp','location']], df_test], ignore_index=True)
    
    df_combined.sort_values(['new_id','timestamp'])
    
    return df_combined



def resample(df_):
    grouped = df_.groupby('new_id')
    
    resample_function = lambda x: x.set_index('timestamp').resample('1T').ffill().reset_index()
    
    resampled_df = pd.concat([resample_function(group) for name, group in grouped])
    
    df_ = resampled_df
    
    df_['shifted'] = df_.groupby('new_id')['location'].shift(-1).fillna('checkout')
    
    return df_

def load_and_combining(files, file_type="csv"):
    """This function implements automatization for loading the csv files into dataframes and 
    combines all of them into one 
    
    Args:
    files (list): a list of all file present in this directory
    file_type (str, default value): the file 
    
    Return:
    df_combined (dataframe): a concated df of all year
    """
    

    # Define an empty list
    all_df = []
    
    
    # Iterate trough the list FILES
    for file in files:
        # Pick only the file ending with csv 
        if file.endswith(file_type):
            
            print(file)
            
            # load this file into a dataframe
            df = pd.read_csv(file, sep=';')
            
            df = create_dt(df)
            
            df = make_checkout(df)
            
            df['new_id'] = (df['day']).astype(str) + "_" + (df['customer_no']).astype(str)
            
            df = entrance(df)
            
            df = resample(df)
            
            all_df.append(df)
    
    
    # Combine all_df
            
    df_combined = pd.concat(all_df, axis=0, ignore_index=True)
    df_combined = df_combined.sort_values(['timestamp', 'new_id']).reset_index(drop=True)
    
    df_resampled = resample(df_combined)
    
    return df_resampled