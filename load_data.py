'''
    Analysis of Israel Pollutant Release and Transfer Register (PRTR)
    Copyright (C) 2020  Doreen S. Ben-Zvi, PhD

    Full license is locates in License.txt at project root folder.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import os

import pandas as pd


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
