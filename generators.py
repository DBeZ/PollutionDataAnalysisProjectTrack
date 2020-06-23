import visualize
from data_cleaning import data_value_cleaining, dataframe_by_column_value_separator
from geoloc_for_map import geoloc_loader
import os
import pandas as pd
import numpy as np



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
    working_direcotry = os.getcwd()
    graph_folder_name = folder_name
    if not os.path.isdir(graph_folder_name):
        os.mkdir(graph_folder_name)
    os.chdir(graph_folder_name)

    cleaned_df = data_value_cleaining(data)  # Corrects Nans and specific emission column data
    emission_type_dfs, emission_type_dfs_val_list = dataframe_by_column_value_separator(dataframe=cleaned_df,
                                                                                        col="SugPlita", rename_df=True)
    for df in emission_type_dfs:
        col_of = "KvutzatMezahamim"
        df.dropna(axis=0, how='any', subset=[col_of], inplace=True)
        emission_polutent, emission_polutent_val_list = dataframe_by_column_value_separator(dataframe=df, col=col_of,
                                                                                            rename_df=False)

        for data_frame in emission_polutent:
            data_frame.reset_index(inplace=True)

        title_heb = "פליטה של {} בתאונות ובשגרה ל{} לפי {}"
        visualize.accidents_with_non_acci(col_by=x_val_col, col_of=col_of, dataframes=emission_polutent,
                                          title_template=title_heb,
                                          col_name="מוצר", is_x_rtl=True, is_log=is_log)
    os.chdir(working_direcotry)


# Prepare dataframe for comparing accidental or non accidental emissions by emission type in two graph, one for accidents and one for non-accidents
def accidental_graph_generator(data, x_val_col, folder_name, is_log=False):
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
    for df in emission_type_dfs:
        col_of = "KvutzatMezahamim"
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


# Creates and saves bar charts comparing industry type or products by their amount of accidents and non accidental emissions
def accidents_non_accidents_shotgun(data, x_val_col, is_log=False):
    accident_non_acci_graph_generator(data=data, x_val_col=x_val_col,
                                      folder_name="accidents compare to non-accidents graphs Log")
    accidental_graph_generator(data=data, x_val_col=x_val_col, folder_name="accidents graphs", is_log=is_log)
    accidental_graph_generator(data=data, x_val_col=x_val_col, folder_name="non accidents graphs", is_log=is_log)


# Formates data of intustry types and products and generates dot leaf and violin plots
def accident_anaylsis(data, cutoff=0):
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


# User input whether cutoff of outlier removal was correct
def accident_cutoff_check_ui(data,cutoff_val):
    Flag = True
    while Flag:
        print("Is the cutoff of "+str(cutoff_val)+ " removing enough of the outliers? y/n")
        input_val = input()
        if input_val =="y":
            return cutoff_val
        elif input_val=="n":
            cutoff_val=accident_analysis_ui(data)
            return cutoff_val
        else:
            Flag=False
            print("Input should be y or n")

# Top outlayer removal by cutoff input and check
def accident_analysis_ui(data):
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
    accident_anaylsis(data=data, cutoff=input_val)
    cutoff_val=accident_cutoff_check_ui(data,cutoff_val=input_val)
    return cutoff_val

def industry_geoloc(data, city_col, industry_col, pivot_by, values):
    # Translate cities to geolocations
    geoloc =geoloc_loader(data=data, city_col=city_col)
    # Add geolocation column
    data_geoloc = pd.merge(data, geoloc, left_on=city_col, right_on="yeshuv", how='left')
    # Separates geolocation column into lat lon and alt
    data_geoloc[['latitude', 'longitude', 'altitude']] = pd.DataFrame(data_geoloc['point'].tolist(),
                                                                    index=data_geoloc.index)
    # Remove NaN as map ha trouble with it
    data_geoloc.dropna(axis=0, how='any', subset=['latitude', 'longitude'], inplace=True)

    category_df, category_dfs_val_list = dataframe_by_column_value_separator(dataframe=data_geoloc, col=industry_col, rename_df=True)

    # Leftover from attampt to plot each category with a different color on the same plot
    # values_all=data_geoloc[industry_col].unique()
    # masks = []
    # for value in values_all:
    #     mask = [data_geoloc[industry_col]==value]
    #     masks.append(mask)

    # visualize.industry_map(data_list=category_df, data_values_list=category_dfs_val_list, industry_col=industry_col)

    pivots=[]
    for df in category_df:
        df=df.sample(frac=1).drop_duplicates(['MisparTaagidShutfutMenifa'])
        pv =pd.pivot_table(data=df, values=values, index=[pivot_by, 'latitude', 'longitude'], aggfunc="count")
        pv=pv.reset_index()
        pivots.append(pv)

    visualize.industry_size_map(data_list=pivots, data_values_list=category_dfs_val_list,
                                industry_col=industry_col)






