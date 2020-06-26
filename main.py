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

import generators
from data_cleaning import data_value_cleaining, data_cleaning, shorten_product_name
from load_data import load_data_from_pickle
from save_data import create_output_folder

#########################
# Data Analysis project #
# Project Course        #
# Doreen Ben-Zvi, PhD   #
# Jun 2020              #
#########################

'''
Data analysis project - of Industrial Pollution Database

Uses Israel ministry of environmental protection Pollutant Release and Transfer Register (PRTR).
It contains structured Data, with Quantitative and Categorical entries.

Purpose:
(1) Assess the reduction in which industries will have a great positive impact on pollution of various type.
(2) Infer whether accidents have a profound impact on pollution in certain industries.
(3) Identify Industrial geographical clusters which moving/reducing will have a significant difference on pollution in different areas in Israel.

Note - axis labels and tick labels are in Hebrew, labels are mirrored to allow for proper presentation. Some of them are shortened to an arbitrary length for display purposes. Others are shortened by dictionary. 
Note - subtables for pivot are either masked or by creating a separate new table for each value in a given column (when the values are categories).
'''


def main():
    '''
    (1) Data Cleaning. Uses a non-graphic UI. Cleaned data is then pickled. If a pickled data file exists UI will not be called.
    (1.1) Columns with low variability (less than two unique values) are removed.
    (1.2) Numeric columns description is displayed.
    (1.3) Non-numeric columns description is displayed.
    (1.4) All column names are displayed.
    (1.5) The type, unique value amount and a sample of of its values are displayed.
    (1.6) Dialog asks whether to convert the column to int, bool, date (d/m/Y format), category or to record its name for future decision.
    Column where conversion fails are also recorded for further exploration.
    (1.7) Columns containing NaNs are listed. These are not all with empty cells as empty strings are not identified.
    Specific column treatment: Comma removal from numeric values, accidental/non accidental/total emission calculated from data, non-dangerous waste column created.
    '''

    file_name = "MIFLAS_data.csv"
    pickel_name = "cleanData"
    output_folder_name = "Output_files"
    working_directory=os.getcwd()
    create_output_folder(foldername=output_folder_name)
    if os.path.isfile(
            os.getcwd() + "\\" + output_folder_name + "\\" + pickel_name + ".pkl"):  # check if pickle file exists.
        data_df = load_data_from_pickle(pickle_file_name=pickel_name, output_folder_name=output_folder_name)
    else:
        data_cleaning(file_to_load=file_name, pickel_name=pickel_name,
                      output_folder_name=output_folder_name)  # Removes columns and adjusts data types
        data_df = load_data_from_pickle(pickle_file_name=pickel_name, output_folder_name=output_folder_name)

    data_df = shorten_product_name(dataframe=data_df, product_col="TchumPeilutAtarSvivati")
    cleaned_df = data_value_cleaining(data_df)
    os.chdir(working_directory)

    ## Most polluting factories (waste)
    '''(2) Bar plots of 10 factories which produce the most waste, dangerous and non-dangerous.'''
    generators.waste(data=cleaned_df)
    print("Waste analysis Done")

    ## Industries with most accidents
    '''
    (3) Multi-feature scatter plot comparing accidental and non-accidental emission using altair. y axis is industry field, x axis is a sub division of industry fields. Circle size denotes emission amount. 
    Graphs saved as HTML file in subfolders of the output folder.
    A non-graphic UI is called to determine the number of high outlier removal - a number is selected, graphs are saved and results is confirmed or the process is repeated with a new entered number.'''

    ## Initial visualization of accidental and non accidental emissions- shotgun approach
    '''
    (4) Violin plots created for accidental and non-accidental emission in industry fields using seaborn.
    '''
    generators.accident_analysis_ui(data=cleaned_df)
    print("Accident analysis Done")

    ''' 
    Optional: Create bar plots of all possible options of emission type and destination, with and without log y axis. 
    Optional: Crate a bar plot comparing all possible options of emission type and destination, with logarithmic y axis. 
    Optional: Create on two-graph plot (2 subplots) demonstrating the effect of y log scale on inorganic emissions to water sources (by product). 
    Graphs saved as png files in the output folder.
    Note- all optimal plots render by visibly maximizing figure window, causing a flickering affect. 
    '''
    generators.accidents_non_accidents_shotgun(data=cleaned_df,x_val_col='SugPeilutAtarSvivati', is_log=False)
    generators.accidents_non_accidents_shotgun(data=cleaned_df,x_val_col='TchumPeilutAtarSvivati', is_log=False)
    generators.accidents_non_accidents_shotgun(data=cleaned_df,x_val_col='SugPeilutAtarSvivati', is_log=True)
    generators.accidents_non_accidents_shotgun(data=cleaned_df,x_val_col='TchumPeilutAtarSvivati', is_log=True)
    print("Shotgun accident graphs Done")

    ## Industial geographical clusters
    '''
    (5) Gepoy converts Hebrew city names to latitude and longitude. Geolocation data is pickled into output folder. If a pickled data geolocation file exists it will be used instead of accessing the geolocation server.
    (6) Number of factories in each field plotted on map using geoviews. bokeh provides interactivity. Circle size indicates number of factories in the city. Circle color changes between graphs. Graphs saved as HTML in a subfolder of the output folder.
    Optional: plotting using Folium, non-interactive map (no tooltips or different circle sizes). Circle color changes between graphs. Graphs saved as HTML in a subfolder of the output folder.
    '''
    os.chdir(working_directory)
    generators.industry_geoloc(data=cleaned_df, city_col="YeshuvAtarSvivatiMenifa", industry_col="AnafAtarSvivati",
                               pivot_by="YeshuvAtarSvivatiMenifa", values="AnafAtarSvivati")
    generators.industry_geoloc(data=cleaned_df, city_col="YeshuvAtarSvivatiMenifa",
                               industry_col="TchumPeilutAtarSvivati", pivot_by="YeshuvAtarSvivatiMenifa",
                               values="TchumPeilutAtarSvivati")

    print("Geographical analysis Done")
    print("Analysis Done!")


# Make sure main cannot be called from other functions
if __name__ == "__main__":
    main()
