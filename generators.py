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

import numpy as np
import pandas as pd

import visualize
from data_cleaning import data_value_cleaining, dataframe_by_column_value_separator
from data_cleaning import shorten_name
from geoloc_for_map import geoloc_loader


####################################
# Format data for graph formation #
####################################

# Pivot dataframe, then remove NaN and zeros, sort descending from pivot table and return it
def pivot_sort_clean(data, by, values):
    pv = pd.pivot_table(data=data, values=values, index=by, aggfunc=np.sum)
    pv.dropna(axis=0, how='any', inplace=True)
    pv = pv.loc[~(pv == 0).any(axis=1)]
    pv_sorted = pv.sort_values(by=pv.columns[0], ascending=False)
    return pv_sorted


# Pivot dataframe, then remove NaN and zeros from  pivot table and return it
def pivot_sort(data, by, values):
    pv = pd.pivot_table(data=data, values=values, index=by, aggfunc=np.sum)
    pv.dropna(axis=0, how='any', inplace=True)
    pv = pv.loc[~(pv == 0).any(axis=1)]
    return pv


# Prepare dataframe for comparing accidental and non accidental emissions by emission type in one graphs
def accident_non_acci_graph_generator(data, x_val_col, folder_name, is_log=True):
    try:
        data=shorten_name(dataframe=data, cols=x_val_col, how_short=40)
    except Exception as e:
        print("Error during name shortening - ")
        print(e)

    try:
        working_directory = os.getcwd()
        graph_folder_name = folder_name
        if not os.path.isdir(graph_folder_name):
            os.mkdir(graph_folder_name)
        os.chdir(working_directory+"\\"+graph_folder_name)

        cleaned_df = data_value_cleaining(data)  # Corrects Nans and specific emission column data
        emission_type_dfs, emission_type_dfs_val_list = dataframe_by_column_value_separator(dataframe=cleaned_df,
                                                                                            col="SugPlita", rename_df=True)
        for dataframe in emission_type_dfs:
            col_of = "KvutzatMezahamim"
            df=dataframe.copy(deep=True)
            df.name=dataframe.name
            df.dropna(axis=0, how='any', subset=[col_of], inplace=True)
            emission_polutent, emission_polutent_val_list = dataframe_by_column_value_separator(dataframe=df, col=col_of,
                                                                                                rename_df=False)

            for data_frame in emission_polutent:
                data_frame.reset_index(inplace=True)

            title_heb = "פליטה של {} בתאונות ובשגרה ל{} לפי {}"
            emission_polutent=shorten_name(dataframe=emission_polutent, cols=["SugPeilutAtarSvivati"], how_short=40)
            visualize.accidents_with_non_acci(col_by=x_val_col, col_of=col_of, dataframes=emission_polutent,
                                              title_template=title_heb,
                                              col_name="מוצר", output_folder_name ="", is_x_rtl=True, is_log=is_log)
            os.chdir(working_directory)
    except Exception as e:
        os.chdir(working_directory)
        print("Error during generating accidental and non accidental comparing visualization")
        print(e)





# Prepare dataframe for comparing accidental or non accidental emissions by emission type in two graph, one for accidents and one for non-accidents
def accidental_graph_generator(data, x_val_col, folder_name, is_log=False):
    try:
        working_direcotry = os.getcwd()
        if is_log:
            folder_name += " log"
        graph_folder_name = folder_name
        if not os.path.isdir(graph_folder_name):
            os.mkdir(graph_folder_name)
        os.chdir(graph_folder_name)

        cleaned_df = data_value_cleaining(data)  # Corrects Nans and specific emission column data
        emission_type_dfs, emission_type_dfs_val_list = dataframe_by_column_value_separator(dataframe=cleaned_df,
                                                                                            col="SugPlita", rename_df=True)
        for dataframe in emission_type_dfs:
            col_of = "KvutzatMezahamim"
            df=dataframe.copy(deep=True)
            df.name = dataframe.name
            df.dropna(axis=0, how='any', subset=[col_of], inplace=True)
            emission_polutent, emission_polutent_val_list = dataframe_by_column_value_separator(dataframe=df, col=col_of,
                                                                                                rename_df=False)

            for data_frame in emission_polutent:
                data_frame.reset_index(inplace=True)

            title_heb = "פליטה של {} בתאונות ל{} לפי {}"
            visualize.accidents_or_non_acci(dataframes=emission_polutent, col_by=x_val_col, col_of=col_of,
                                            title_template=title_heb, col_name="מוצר", data_series=['KamutPlitaBeTeunot'],
                                            is_x_rtl=True, is_log=is_log)
        os.chdir(working_direcotry)
    except Exception as e:
        os.chdir(working_direcotry)
        print("Error during generating accidental emmision visualization")
        print(e)

# Creates and saves bar charts comparing industry type or products by their amount of accidents and non accidental emissions
def accidents_non_accidents_shotgun(data, x_val_col, is_log=False, output_folder="Output_files"):
    current_directory=os.getcwd()
    try:
        accident_non_acci_graph_generator(data=data, x_val_col=x_val_col,
                                          folder_name=output_folder+"\\accidents compare to non-accidents graphs Log")
    except Exception as e:
        print("Error during brut-force emission visualization - comparing accidents and non accidents")
        print(e)
    try:
        accidental_graph_generator(data=data, x_val_col=x_val_col, folder_name="accidents graphs", is_log=is_log)
    except Exception as e:
        print("Error during brut-force emission visualization - accident data")
        print(e)
    try:
        accidental_graph_generator(data=data, x_val_col=x_val_col, folder_name="non accidents graphs", is_log=is_log)
    except Exception as e:
        print("Error during brut-force emission visualization - non accident data")
        print(e)
    os.chdir(current_directory)


# Formates data of intustry types and products and generates dot leaf and violin plots
def accident_anaylsis(data, cutoff=0):
    try:
        accidents = pivot_sort_clean(data=data, by=['SugPeilutAtarSvivati', 'TchumPeilutAtarSvivati', 'AnafAtarSvivati'],
                                     values=['KamutPlitaBeTeunot'])
        accidents = accidents.reset_index()
        non_accidents = pivot_sort_clean(data=data,
                                         by=['SugPeilutAtarSvivati', 'TchumPeilutAtarSvivati', 'AnafAtarSvivati'],
                                         values=['KamutPlitaLoBeTeunot'])
        non_accidents = non_accidents.reset_index()

        visualize.multi_feat_scatter(data=accidents, filename="Accidental Emissionsv All Data",
                                     x_col='SugPeilutAtarSvivati', y_col='TchumPeilutAtarSvivati',
                                     size_col='KamutPlitaBeTeunot', color_col='AnafAtarSvivati')
        visualize.multi_feat_scatter(data=non_accidents, filename="Non Accidental Emissions All Data",
                                     x_col='SugPeilutAtarSvivati', y_col='TchumPeilutAtarSvivati',
                                     size_col='KamutPlitaLoBeTeunot', color_col='AnafAtarSvivati')

        visualize.violin_emissions(data=data, x_col='AnafAtarSvivati', y_col="KamutPlita", hue="Accidental", split=True,
                                   figure_name="Emissions" + "-" + "AnafAtarSvivati",
                                   fig_title="פליטה בתאונות ובשגרה לפי ענף תעשייתי", is_x_rtl=True)
        visualize.violin_emissions(data=data, x_col='TchumPeilutAtarSvivati', y_col="KamutPlita", hue="Accidental",
                                   split=True, figure_name="Emissions" + "-" + "TchumPeilutAtarSvivati",
                                   fig_title="פליטה בתאונות ובשגרה לפי תחום תעשייתי", is_x_rtl=True)
        visualize.violin_emissions(data=data, x_col='SugPeilutAtarSvivati', y_col="KamutPlita", hue="Accidental",
                                   split=True, figure_name="Emissions" + "-" + "SugPeilutAtarSvivati",
                                   fig_title="פליטה בתאונות ובשגרה לםי מוצר", is_x_rtl=True)

        visualize.multi_feat_scatter(data=accidents.iloc[cutoff:], filename="Accidental Emissions",
                                     x_col='SugPeilutAtarSvivati', y_col='TchumPeilutAtarSvivati',
                                     size_col='KamutPlitaBeTeunot', color_col='AnafAtarSvivati')
        visualize.multi_feat_scatter(data=non_accidents.iloc[cutoff:], filename="Non Accidental Emissions",
                                     x_col='SugPeilutAtarSvivati', y_col='TchumPeilutAtarSvivati',
                                     size_col='KamutPlitaLoBeTeunot', color_col='AnafAtarSvivati')

        if cutoff != 0:
            print("Accidental emissions: top "+str(cutoff)+" outliers removed were:")
            print(accidents.iloc[cutoff])
            print("Non-Accidental emissions: top" + str(cutoff) + " outliers removed were:")
            print(non_accidents.iloc[cutoff])
    except Exception as e:
        print("Error during emission violin-plot generation")
        print(e)


# User input whether cutoff of outlier removal was correct
def accident_cutoff_check_ui(data,cutoff_val):
    try:
        Flag = True
        while Flag:
            print("Is the cutoff of "+str(cutoff_val)+ " removing enough of the outliers? y/n")
            input_val = input()
            if input_val =="y":
                Flag=False
                return cutoff_val
            elif input_val=="n":
                Flag=False
                cutoff_val=accident_analysis_ui(data)
                return cutoff_val
            else:
                print("Input should be y or n")
    except Exception as e:
        print("Error during outlier cutoff setting")
        print(e)

# Top outlier removal by cutoff input and check
def accident_analysis_ui(data):
    try:
        print("All Emissions Description:")
        emmisions_desc = data[['KamutPlita', 'KamutPlitaLoBeTeunot', 'KamutPlitaBeTeunot']].describe()
        print(emmisions_desc)

        Flag = True
        while Flag:
            try:
                print("Enter how many of the top out-layers to remove")
                input_val = int(input())
                if input_val > 0 and input_val < data.size:
                    Flag=False
                else: print("Input should be a number between 1 and "+str(data.size))
            except ValueError:
                print("Input should be a number between 1 and "+str(data.size))
        accident_anaylsis(data=data, cutoff=input_val)
        cutoff_val=accident_cutoff_check_ui(data,cutoff_val=input_val)
        return cutoff_val
    except Exception as e:
        print("Error in outlier cutoff dialog")
        print(e)

def industry_geoloc(data, city_col, industry_col, pivot_by, values, output_folder_name="Output_files"):
    current_folder=os.getcwd()
    os.chdir(output_folder_name)
    try:
        # Translate cities to geolocations
        geoloc =geoloc_loader(data=data, city_col=city_col)
    except Exception as e:
        print("Error during geolocation retrieval")
        print(e)

    try:
        # Add geolocation column
        data_geoloc = pd.merge(data, geoloc, left_on=city_col, right_on="yeshuv", how='left')
        # Separates geolocation column into lat lon and alt
        data_geoloc[['latitude', 'longitude', 'altitude']] = pd.DataFrame(data_geoloc['point'].tolist(),
                                                                        index=data_geoloc.index)
        # Remove NaN as map ha trouble with it
        data_geoloc.dropna(axis=0, how='any', subset=['latitude', 'longitude'], inplace=True)

        category_df, category_dfs_val_list = dataframe_by_column_value_separator(dataframe=data_geoloc, col=industry_col, rename_df=True)

    except Exception as e:
        print("Error during geoloc data addition to main data")
        print(e)

    # try:
    #     visualize.industry_map(data_list=category_df, data_values_list=category_dfs_val_list, industry_col=industry_col)
    # except Exception as e:
    #     print("Error during map visualization with dots (folium)")
    #     print(e)

    try:
        pivots=[]
        for df in category_df:
            df=df.sample(frac=1).drop_duplicates(['MisparTaagidShutfutMenifa'])
            pv =pd.pivot_table(data=df, values=values, index=[pivot_by, 'latitude', 'longitude'], aggfunc="count")
            pv=pv.reset_index()
            pivots.append(pv)

        visualize.industry_size_map(data_list=pivots, data_values_list=category_dfs_val_list,
                                    industry_col=industry_col)
    except Exception as e:
        print("Error during map visualization with circles (bokeh)")
        print(e)
    os.chdir(current_folder)

# Subset dataframe to plot waste production during last year
def waste(data):
    try:
        data["total_dangerous_waste"]=data["SachTipulPsoletLoMesukenet"]+data["SachSilukPsoletLoMesukenet"]
        data["total_non_dangerous_waste"] = data["SachTipulPsoletLoMesukenet"] + data["SachSilukPsoletLoMesukenet"]
        data["total_waste"]=data["total_dangerous_waste"]+ data["total_non_dangerous_waste"]
        last_year=data["ShnatDivuach"].max()
        mask=data["ShnatDivuach"]==last_year
        data_last_year=data.mask(mask)
        visualize.waste_graph(data_last_year)
    except Exception as e:
        print("Error during waste visualization generation")
        print(e)





