'''
    Analysis of Israel Pollutant Release and Transfer Register (PRTR)
    Copyright (C) 2020  Doreen S. Ben-Zvi, PhD

    Full license is locates in License.txt at project root folder.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import os

import generators
from data_cleaning import data_value_cleaining, data_cleaning, shorten_product_name
from load_data import load_data_from_pickle
from save_data import create_output_folder


#########################
# Data Analysis project #
# Project Course        #
# Doreen Ben-Zvi PhD    #
# Jun 2020              #
#########################

def main():
    file_name = "MIFLAS_data.csv"
    pickel_name = "cleanData"
    output_folder_name = "Output_files"
    working_direcotry = os.getcwd()
    create_output_folder(foldername=output_folder_name)
    # check if pickle file exists.
    if os.path.isfile(os.getcwd() + "\\" + output_folder_name + "\\" + pickel_name + ".pkl"):
        data_df = load_data_from_pickle(pickle_file_name=pickel_name, output_folder_name=output_folder_name)
    else:

        data_cleaning(file_to_load=file_name, pickel_name=pickel_name,
                      output_folder_name=output_folder_name)  # Removes columns and adjusts data types
        data_df = load_data_from_pickle(pickle_file_name=pickel_name, output_folder_name=output_folder_name)

    data_df = shorten_product_name(dataframe=data_df, product_col="TchumPeilutAtarSvivati")
    cleaned_df = data_value_cleaining(data_df)

    os.chdir(output_folder_name)
    ##Most polluting factories (waste)
    generators.waste(data=cleaned_df)

    ## Initial visualization of accidental and non accidental emissions- shotgun approach
    # generators.accidents_non_accidents_shotgun(data=data_df,x_val_col='SugPeilutAtarSvivati', is_log=False)
    # generators.accidents_non_accidents_shotgun(data=data_df,x_val_col='TchumPeilutAtarSvivati', is_log=False)
    # generators.accidents_non_accidents_shotgun(data=data_df,x_val_col='SugPeilutAtarSvivati', is_log=True)
    # generators.accidents_non_accidents_shotgun(data=data_df,x_val_col='TchumPeilutAtarSvivati', is_log=True)

    ## Industries with most accidents
    generators.accident_analysis_ui(data=cleaned_df)

    os.chdir(working_direcotry)

    ## Industial geographical clusters
    generators.industry_geoloc(data=cleaned_df, city_col="YeshuvAtarSvivatiMenifa", industry_col="AnafAtarSvivati", pivot_by="YeshuvAtarSvivatiMenifa", values="AnafAtarSvivati")
    generators.industry_geoloc(data=cleaned_df, city_col="YeshuvAtarSvivatiMenifa",
                               industry_col="TchumPeilutAtarSvivati", pivot_by="YeshuvAtarSvivatiMenifa",
                               values="TchumPeilutAtarSvivati")

    print("Done")


# Make sure main cannot be called from other functions
if __name__ == "__main__":
    main()
