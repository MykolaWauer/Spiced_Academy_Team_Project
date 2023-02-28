"""
This script gets 

"""

import pandas as pd
import os 
from utils import *



# List all file in the current directory
FILES = os.listdir(path=".")

data_all = load_and_combining(FILES, file_type="csv")
print(data_all)