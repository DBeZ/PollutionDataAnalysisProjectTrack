import pandas as pd
import os

################
# Loading data #
################

# Load dataframe from csv
def load_data_from_csv(csv_file_name):
    data_loaded = pd.read_csv(csv_file_name, index_col=None, na_values=['NA'], low_memory=False)
    return data_loaded


# load dataframe from pickle
def load_data_from_pickle(pickle_file_name, output_folder_name=os.getcwd()):
    working_direcotry = os.getcwd()
    os.chdir(output_folder_name)
    pickled_data = pd.read_pickle(pickle_file_name + ".pkl")
    os.chdir(working_direcotry)
    return pickled_data



